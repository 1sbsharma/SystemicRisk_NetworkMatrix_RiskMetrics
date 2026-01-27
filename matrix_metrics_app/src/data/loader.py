import pandas as pd
import streamlit as st
from io import StringIO, BytesIO

def load_data(uploaded_file, has_index_col: bool = False):
    """
    Load data from an uploaded file (CSV or Excel) into a pandas DataFrame.

    Parameters:
    - uploaded_file: An uploaded file object from Streamlit's file_uploader.
    - has_index_col: Boolean indicating if the first column should be treated as the index.

    Returns:
    pandas.DataFrame or None: The loaded DataFrame, or None if the file is invalid.
    """
    if uploaded_file is None:
        return None

    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            # To read csv, we can use StringIO to treat the string as a file
            string_data = StringIO(uploaded_file.getvalue().decode('utf-8'))
            df = pd.read_csv(string_data, index_col=0 if has_index_col else None)
        elif file_extension in ['xlsx', 'xls']:
            # To read excel, we use BytesIO
            bytes_data = BytesIO(uploaded_file.getvalue())
            df = pd.read_excel(bytes_data, index_col=0 if has_index_col else None)
        else:
            st.error(f"Unsupported file format: .{file_extension}. Please upload a CSV or Excel file.")
            return None
            
        return df
        
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        return None
