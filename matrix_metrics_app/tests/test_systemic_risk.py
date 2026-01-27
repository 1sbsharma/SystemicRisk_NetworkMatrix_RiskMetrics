import unittest
import pandas as pd
import numpy as np
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.systemic_risk import SystemicRiskCalculator

class TestSystemicRiskCalculator(unittest.TestCase):

    def setUp(self):
        """Set up test data."""
        # Get the absolute path to the data files
        base_path = os.path.dirname(__file__)
        inst_path = os.path.join(base_path, '..', 'data', 'sample_data', 'das_2016_institutions.csv')
        adj_path = os.path.join(base_path, '..', 'data', 'sample_data', 'das_2016_adjacency.csv')

        # Load the data
        self.institution_df = pd.read_csv(inst_path)
        self.adjacency_df = pd.read_csv(adj_path, index_col=0)

        # Extract compromise vector and adjacency matrix
        self.compromise_vector = self.institution_df['CompromiseScore']
        
        # Initialize the calculator
        self.calculator = SystemicRiskCalculator(self.compromise_vector, self.adjacency_df)

    def test_calculate_S(self):
        """Test the primary systemic risk score (S) calculation."""
        # The expected value for the sample data.
        expected_s_score = 12.0
        calculated_s_score = self.calculator.calculate_S()
        self.assertAlmostEqual(calculated_s_score, expected_s_score, places=4, 
                             msg="Calculated S score does not match the expected value.")

    def test_risk_decomposition(self):
        """Test the risk decomposition (Di) calculation."""
        # This is a placeholder test. 
        # The actual expected values would need to be calculated.
        risk_decomposition = self.calculator.calculate_risk_decomposition()
        
        # Check if the sum of Di equals the total risk S
        # By definition, sum(Di) should be equal to S
        self.assertAlmostEqual(np.sum(risk_decomposition), self.calculator.S, places=4,
                             msg="The sum of risk decomposition (Di) should equal the total systemic risk score (S).")

if __name__ == '__main__':
    unittest.main()
