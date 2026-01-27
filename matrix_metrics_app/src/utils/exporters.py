import pandas as pd
from io import BytesIO

def export_to_excel(session_data: dict) -> BytesIO:
    """
    Exports all relevant data from the session into a single multi-sheet Excel file.

    Parameters:
    - session_data: A dictionary containing DataFrames and metrics from st.session_state.

    Returns:
    - BytesIO: A byte stream of the generated Excel file, ready for download.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Input Data
        if session_data.get('institution_df') is not None:
            session_data['institution_df'].to_excel(writer, sheet_name='Institution_Data', index=False)
        if session_data.get('adjacency_df') is not None:
            session_data['adjacency_df'].to_excel(writer, sheet_name='Adjacency_Matrix')

        # Sheet 2: Core Metrics Summary
        summary_data = {
            "Metric": ["Systemic Risk Score (S)", "Network Fragility (R)", "Normalized Risk Score (S̄)"],
            "Value": [
                session_data.get('systemic_risk_score'),
                session_data.get('fragility'),
                session_data.get('normalized_score')
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Metrics_Summary', index=False)

        # Sheet 3: Detailed Per-Institution Metrics
        if session_data.get('institution_df') is not None:
            detailed_metrics = session_data['institution_df'][['InstitutionID', 'Name']].copy()
            if session_data.get('risk_decomposition') is not None:
                detailed_metrics['Risk_Contribution'] = session_data['risk_decomposition']
            if session_data.get('centrality') is not None:
                detailed_metrics['Centrality'] = session_data['centrality']
            if session_data.get('criticality') is not None:
                detailed_metrics['Criticality'] = session_data['criticality']
            detailed_metrics.to_excel(writer, sheet_name='Detailed_Metrics', index=False)

        # Sheet 4: Cross-Risk Matrix
        if session_data.get('cross_risk_matrix') is not None:
            session_data['cross_risk_matrix'].to_excel(writer, sheet_name='Cross_Risk_Matrix')
    
    output.seek(0)
    return output
