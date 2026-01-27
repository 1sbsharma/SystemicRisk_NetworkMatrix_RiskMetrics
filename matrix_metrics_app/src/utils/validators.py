import pandas as pd
import numpy as np

def validate_institution_data(df: pd.DataFrame) -> (bool, list):
    """
    Validates the institution data DataFrame.

    Checks for:
    - Required columns: ['InstitutionID', 'Name', 'CompromiseScore']
    - Non-negative 'CompromiseScore'.

    Returns:
    (bool, list): A tuple containing a boolean for validity and a list of error messages.
    """
    errors = []
    required_columns = ['InstitutionID', 'Name', 'CompromiseScore']
    
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")

    # Check for non-negative compromise scores
    if 'CompromiseScore' in df.columns and (df['CompromiseScore'] < 0).any():
        errors.append("CompromiseScore column contains negative values.")

    return not errors, errors


def validate_adjacency_matrix(df: pd.DataFrame) -> (bool, list):
    """
    Validates the adjacency matrix DataFrame.

    Checks for:
    - Square matrix (rows == columns).
    - Diagonal elements are all 1.
    - All values are non-negative.
    - All values are numeric.

    Returns:
    (bool, list): A tuple containing a boolean for validity and a list of error messages.
    """
    errors = []
    
    # Check if square
    if df.shape[0] != df.shape[1]:
        errors.append(f"Adjacency matrix is not square ({df.shape[0]}x{df.shape[1]}).")
        return False, errors # Short-circuit if not square

    # Convert to numpy for easier checks
    matrix = df.to_numpy()

    # Check if all values are numeric
    if not np.issubdtype(matrix.dtype, np.number):
         errors.append("Matrix contains non-numeric values.")

    # Check for non-negative values
    if (matrix < 0).any():
        errors.append("Matrix contains negative values.")
        
    # Check for diagonal of 1s
    if not np.all(np.diag(matrix) == 1):
        errors.append("Diagonal elements of the matrix are not all 1.")

    return not errors, errors
