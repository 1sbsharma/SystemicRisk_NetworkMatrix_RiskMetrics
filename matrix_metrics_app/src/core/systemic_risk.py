import numpy as np
import pandas as pd
from .network_utils import calculate_eigenvector_centrality

class SystemicRiskCalculator:
    """
    A class to calculate systemic risk metrics based on the Matrix Metrics framework.
    """
    def __init__(self, compromise_vector: pd.Series, adjacency_matrix: pd.DataFrame):
        """
        Initializes the calculator with validated data.

        Parameters:
        compromise_vector (pd.Series): A pandas Series of compromise scores for each institution.
        adjacency_matrix (pd.DataFrame): A pandas DataFrame representing the network adjacency matrix.
        """
        self.C = np.array(compromise_vector)
        self.E = np.array(adjacency_matrix)
        self.E_df = adjacency_matrix  # Keep original DataFrame for networkx
        self.n = len(self.C)
        self._s_score = None  # Cache for the S score
        self._centrality = None # Cache for centrality
        self._gradient_s = None # Cache for the gradient of S
        self.validate_inputs()

    def validate_inputs(self):
        """
        Validates the dimensions and values of the input vectors and matrices.
        """
        if self.C.ndim != 1:
            raise ValueError("Compromise vector must be a 1D array.")
        if self.E.ndim != 2 or self.E.shape[0] != self.E.shape[1]:
            raise ValueError("Adjacency matrix must be a 2D square matrix.")
        if self.n != self.E.shape[0]:
            raise ValueError("Dimensions of compromise vector and adjacency matrix do not match.")
        # Additional checks can be added here if needed

    @property
    def S(self) -> float:
        """
        Calculates and returns the cached primary systemic risk score (S).
        """
        if self._s_score is None:
            self._s_score = self.calculate_S()
        return self._s_score

    def _get_gradient(self):
        """Helper method to calculate and cache the gradient of S."""
        if self._gradient_s is None:
            if self.S == 0:
                self._gradient_s = np.zeros(self.n)
            else:
                # Gradient ∂S/∂C = (E + E')C / 2S
                self._gradient_s = (self.E + self.E.T) @ self.C / (2 * self.S)
        return self._gradient_s

    def calculate_S(self) -> float:
        """
        Calculates the primary systemic risk score (S).
        S = sqrt(C' * E * C)
        
        Returns:
        float: The systemic risk score.
        """
        try:
            # Ensure C is a column vector for matrix multiplication
            c_col = self.C.reshape(-1, 1)
            # S^2 = C' * E * C
            s_squared = c_col.T @ self.E @ c_col
            return np.sqrt(s_squared.item())
        except np.linalg.LinAlgError as e:
            raise ValueError(f"Linear algebra error during S calculation: {e}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred during S calculation: {e}")

    # --- Placeholder for future metric calculations ---

    def calculate_risk_decomposition(self) -> np.ndarray:
        """
        Calculates the risk decomposition for each institution (Di).
        Di = Ci * (∂S/∂Ci)
        The gradient ∂S/∂C is (E + E')C / 2S.
        
        Returns:
        np.ndarray: An array of risk decomposition values for each institution.
        """
        gradient_s = self._get_gradient()
        # Element-wise product of C and the gradient
        decomposition = self.C * gradient_s
        return decomposition
        
    def calculate_centrality(self) -> np.ndarray:
        """
        Calculates and returns the cached eigenvector centrality.
        """
        if self._centrality is None:
            self._centrality = calculate_eigenvector_centrality(self.E_df)
        return self._centrality

    def calculate_criticality(self) -> np.ndarray:
        """
        Calculates the criticality for each institution.
        Criticality = CompromiseScore * EigenvectorCentrality
        
        Returns:
        np.ndarray: An array of criticality scores.
        """
        centrality = self.calculate_centrality()
        criticality = self.C * centrality
        return criticality

    def calculate_risk_increment(self) -> np.ndarray:
        """
        Calculate risk increment Ii = ∂S/∂Ci for each institution.
        This measures the sensitivity of the systemic risk score to changes 
        in each institution's compromise score.
        
        Ii = ∂S/∂Ci = (1/2S) * [(E + E')C]_i
        
        The risk increment shows how much the overall systemic risk score would 
        change if an individual institution's compromise score increased by one unit.
        
        Returns:
        np.ndarray: An array of risk increment values for each institution.
        """
        # The risk increment is the gradient of S with respect to C
        risk_increment = self._get_gradient()
        return risk_increment
        
    def calculate_fragility(self) -> float:
        """
        Calculates the network fragility (R).
        R = E(d^2) / E(d), where d is the node degree vector.
        This measures the concentration of connections in the network.
        
        Returns:
        float: The network fragility score.
        """
        # Node degree is the sum of connections for each node
        degrees = np.sum(self.E, axis=1)
        
        mean_degree = np.mean(degrees)
        if mean_degree == 0:
            return 0.0
            
        mean_squared_degree = np.mean(degrees**2)
        
        fragility = mean_squared_degree / mean_degree
        return fragility
    
    def calculate_node_degrees(self) -> np.ndarray:
        """
        Calculates the degree (number of connections) for each node.
        The degree includes self-connections (diagonal elements).
        
        This is useful for understanding network fragility, as fragility 
        measures the concentration of connections across nodes.
        
        Returns:
        np.ndarray: An array of degree values for each institution.
        """
        degrees = np.sum(self.E, axis=1)
        return degrees
        
    def calculate_normalized_score(self) -> float:
        """
        Calculates the normalized risk score (S̄).
        This isolates the network effect by comparing S to the risk in a network
        with no connections (i.e., E is the identity matrix).
        S̄ = S / S_baseline, where S_baseline = sqrt(C'C).
        
        Returns:
        float: The normalized risk score.
        """
        # S_baseline is the risk with no network effects (E=I)
        s_baseline = np.linalg.norm(self.C)
        
        if s_baseline == 0:
            return 0.0
            
        normalized_score = self.S / s_baseline
        return normalized_score
        
    def calculate_cross_risk(self) -> pd.DataFrame:
        """
        Calculates the cross-risk matrix (ΔDij), representing spillover effects.
        Δij = ∂Dj/∂Ci = δij * gj + Cj * Hij
        where g is the gradient and H is the Hessian of S.

        Returns:
        pd.DataFrame: An n x n matrix of cross-risk values.
        """
        if self.S == 0:
            return pd.DataFrame(np.zeros((self.n, self.n)), index=self.E_df.index, columns=self.E_df.columns)

        g = self._get_gradient()
        
        # Calculate Hessian H = (A/S) - (g*g'/S), where A is the symmetric part of E
        A = (self.E + self.E.T) / 2
        g_outer = np.outer(g, g)
        H = (A - g_outer) / self.S
        
        # Calculate cross-risk matrix: Δ = diag(g) + H @ diag(C)
        delta_matrix = np.diag(g) + H @ np.diag(self.C)

        return pd.DataFrame(delta_matrix, index=self.E_df.index, columns=self.E_df.columns)
