import networkx as nx
import numpy as np
import pandas as pd

def calculate_eigenvector_centrality(adjacency_matrix: pd.DataFrame) -> np.ndarray:
    """
    Calculates the eigenvector centrality for each node in the network.

    Parameters:
    adjacency_matrix (pd.DataFrame): The network's adjacency matrix.

    Returns:
    np.ndarray: An array of eigenvector centrality scores for each node.
    """
    try:
        # Create a graph from the adjacency matrix
        G = nx.from_pandas_adjacency(adjacency_matrix)
        
        # Calculate eigenvector centrality
        # Note: networkx returns a dictionary {node: centrality}
        centrality_dict = nx.eigenvector_centrality(G, max_iter=1000, tol=1.0e-6, weight='weight')
        
        # Convert the dictionary to a numpy array, ensuring correct order by using the original index
        centrality = np.array([centrality_dict[node] for node in adjacency_matrix.index])
        
        return centrality

    except nx.PowerIterationFailedConvergence:
        raise RuntimeError(
            "Power iteration failed to converge when calculating eigenvector centrality. "
            "Try increasing max_iter or changing the tolerance."
        )
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during centrality calculation: {e}")
