import streamlit as st
import pandas as pd
import os
from src.data.loader import load_data
from src.utils.validators import validate_institution_data, validate_adjacency_matrix
from src.core.systemic_risk import SystemicRiskCalculator
from src.visualization.network_viz import create_network_graph
from src.utils.exporters import export_to_excel
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Matrix Metrics: Systemic Risk Scoring",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- App Title and Description ---
st.title("Matrix Metrics: Network-Based Systemic Risk Scoring")
st.markdown("""
    This application implements the **Matrix Metrics** framework for measuring and visualizing 
    systemic risk in financial networks, based on the work of Das (2016).
""")

# --- Sidebar Navigation ---
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Go to",
        ("About", "Data Upload", "Network Construction", "Results Dashboard", "Scenario Analysis", "Compare Scenarios", "Export Results")
    )
    st.markdown("---")
    with st.expander("📖 Quick Help"):
        st.markdown("""
        **Navigation:**
        - Start at **About** to understand the app
        - Upload data or load sample
        - Validate your data
        - View Results Dashboard
        - Run scenarios to test
        
        **Need Help?**
        Visit the **About** page for detailed documentation.
        """)
    st.markdown("---")
    st.info("Built with Streamlit and Python.")

# --- Session State Initialization ---
if 'institution_df' not in st.session_state:
    st.session_state.institution_df = None
if 'adjacency_df' not in st.session_state:
    st.session_state.adjacency_df = None
if 'systemic_risk_score' not in st.session_state:
    st.session_state.systemic_risk_score = None
if 'risk_decomposition' not in st.session_state:
    st.session_state.risk_decomposition = None
if 'centrality' not in st.session_state:
    st.session_state.centrality = None
if 'criticality' not in st.session_state:
    st.session_state.criticality = None
if 'fragility' not in st.session_state:
    st.session_state.fragility = None
if 'normalized_score' not in st.session_state:
    st.session_state.normalized_score = None
if 'cross_risk_matrix' not in st.session_state:
    st.session_state.cross_risk_matrix = None
if 'risk_increment' not in st.session_state:
    st.session_state.risk_increment = None
if 'node_degrees' not in st.session_state:
    st.session_state.node_degrees = None
if 'saved_scenarios' not in st.session_state:
    st.session_state.saved_scenarios = {}
if 'current_scenario_name' not in st.session_state:
    st.session_state.current_scenario_name = None
if 'scenario_modifications' not in st.session_state:
    st.session_state.scenario_modifications = {
        'modified_compromise': None,
        'modified_adjacency': None,
        'removed_institutions': []
    }

# --- Page Content ---
if page == "About":
    st.header("📚 About Matrix Metrics")
    
    # Application Overview
    st.markdown("""
    ### What is Matrix Metrics?
    
    **Matrix Metrics** is a comprehensive framework for measuring and analyzing systemic risk in financial networks. 
    This application helps you:
    - 🔍 **Identify** systemically important institutions
    - 📊 **Quantify** interconnected risks across networks
    - 🎯 **Simulate** stress scenarios and policy interventions
    - 📈 **Visualize** risk propagation patterns
    
    ### Who Might Find This Useful
    
    - **Researchers and practitioners** interested in network-based measures of concentration and contagion risk
    - **Credit risk and portfolio analytics teams** exploring connected-clients effects beyond single-name exposure limits
    - **Regulators and quants** experimenting with explainable systemic or concentration risk metrics
    - **Students and learners** studying financial networks, contagion, and risk decomposition methods
    """)
    
    st.markdown("---")
    
    # Theoretical Foundation
    with st.expander("🎓 Theoretical Foundation", expanded=False):
        st.markdown("""
        ### Network-Based Systemic Risk
        
        This application implements a network-based approach to systemic risk measurement, inspired by the work 
        of Das (2016). The framework combines:
        
        - **Individual Institution Stress:** Compromise scores representing vulnerability
        - **Network Structure:** Interconnections captured in an adjacency matrix
        - **Risk Propagation:** How stress spreads through network connections
        
        ### Why This Approach Matters
        
        Traditional risk metrics focus on individual institutions in isolation. However, the 2008 financial crisis 
        demonstrated that interconnectedness amplifies risk. A single institution's failure can cascade through 
        the network, causing systemic collapse.
        
        **Matrix Metrics addresses this by:**
        1. Explicitly modeling network connections
        2. Measuring risk contribution of each institution
        3. Quantifying spillover effects between institutions
        4. Identifying structural vulnerabilities
        """)
    
    st.markdown("---")
    
    # Quick Start Guide
    with st.expander("🚀 Quick Start Guide", expanded=True):
        st.markdown("""
        ### Step-by-Step Workflow
        
        1. **Data Upload (Page 2)**
           - Load the sample dataset OR upload your own data
           - Required: Institution data with compromise scores + Adjacency matrix
           - Validate your data to ensure proper format
        
        2. **Network Construction (Page 3)**
           - Review the network structure
           - Visualize connections between institutions
           - Examine network statistics
        
        3. **Results Dashboard (Page 4)**
           - View calculated systemic risk metrics
           - Analyze risk decomposition by institution
           - Explore criticality and fragility measures
        
        4. **Scenario Analysis (Page 5)**
           - Test sensitivity to compromise score changes
           - Simulate institution removal (stress testing)
           - Modify network connections (policy scenarios)
        
        5. **Compare Scenarios (Page 6)**
           - Save multiple scenario results
           - Compare metrics side-by-side
           - Track changes across scenarios
        
        6. **Export Results (Page 7)**
           - Download data as Excel/JSON
           - Generate PDF reports
           - Export charts and visualizations
        
        ### Sample Data Walkthrough
        
        The included sample dataset represents a simple financial network with 5 institutions. 
        Use this to familiarize yourself with the application before uploading your own data.
        """)
    
    st.markdown("---")
    
    # Metrics Reference
    st.subheader("📊 Metrics Reference")
    
    with st.expander("**Systemic Risk Score (S) & Normalized Risk Score (S̄)**"):
        st.markdown("""
        ### Systemic Risk Score (S)
        
        **What it is:** The aggregate measure of total systemic risk in the network.
        
        **Formula:** `S = √(C'EC)` where C is the compromise vector and E is the adjacency matrix.
        
        **What it measures:** Combines individual institution stress (compromise scores) with network structure 
        (connections) to produce an overall risk score. Higher values indicate greater systemic vulnerability.
        
        **Interpretation:**
        - Higher S = Greater systemic risk
        - Increases when institutions become more stressed OR connections strengthen
        - Scale depends on your data (compare across scenarios)
        
        **Use case:** Track systemic risk evolution over time or compare different network configurations.
        
        ---
        
        ### Normalized Risk Score (S̄)
        
        **What it is:** Isolates the network effect on systemic risk by normalizing S.
        
        **Formula:** `S̄ = S / √(C'C)` (systemic risk score divided by Euclidean norm of compromise vector).
        
        **What it measures:** The ratio of actual systemic risk to what it would be without network effects. 
        Values greater than 1 indicate network amplification; less than 1 indicate network dampening.
        
        **Interpretation:**
        - S̄ > 1: Network amplifies risk (connections worsen the situation)
        - S̄ = 1: Network has neutral effect
        - S̄ < 1: Network dampens risk (diversification benefit)
        
        **Use case:** Compare systemic risk across networks of different sizes or stress levels. Assess 
        whether network structure is amplifying or mitigating individual institution stress.
        
        ---
        
        **Relationship:** S̄ is derived from S and helps you understand whether your network's connections 
        are making things better (S̄ < 1) or worse (S̄ > 1) compared to isolated institutions.
        """)
    
    with st.expander("**Risk Decomposition (Di)**"):
        st.markdown("""
        **What it is:** Breaks down the total systemic risk score into individual institution contributions.
        
        **Formula:** `Di = Ci × (∂S/∂Ci)` where Ci is institution i's compromise score.
        
        **What it measures:** Each Di represents how much one institution contributes to the total systemic 
        risk. The decomposition satisfies the property that the sum of all Di equals S.
        
        **Interpretation:**
        - Higher Di = Greater contribution to systemic risk
        - Institutions with high Di are systemically important
        - Sum of all Di equals total S (perfect decomposition)
        
        **Use case:** Identify which institutions pose the greatest risk to the system. Prioritize monitoring 
        and regulatory oversight accordingly.
        """)
    
    with st.expander("**Centrality**"):
        st.markdown("""
        **What it is:** Measures an institution's importance in the network structure.
        
        **Formula:** Based on the institution's connections (node degree in the network).
        
        **What it measures:** How connected an institution is within the network. Highly central institutions 
        have many connections and can act as conduits for risk transmission.
        
        **Interpretation:**
        - Higher centrality = More connected institution
        - Central institutions can amplify or absorb shocks
        - Pure structural measure (independent of compromise scores)
        
        **Use case:** Identify network hubs that could spread or contain contagion.
        """)
    
    with st.expander("**Criticality**"):
        st.markdown("""
        **What it is:** Risk-weighted measure of an institution's importance.
        
        **Formula:** Combines centrality with compromise score to produce a risk-weighted importance metric.
        
        **What it measures:** How critical an institution is when considering both its network position AND 
        its current stress level. An institution can be highly critical by being very connected, very stressed, 
        or both.
        
        **Interpretation:**
        - Higher criticality = Greater importance considering risk and structure
        - Identifies institutions that are both vulnerable and interconnected
        - More actionable than centrality alone
        
        **Use case:** Prioritize intervention targets - institutions that are both stressed and structurally important.
        """)
    
    with st.expander("**Fragility (R)**"):
        st.markdown("""
        **What it is:** Measures network concentration and structural vulnerability.
        
        **Formula:** `R = Σ(ki/K)²` where ki is node i's degree and K is total degree sum.
        
        **What it measures:** How concentrated the network is. Higher fragility means risk is concentrated 
        in fewer institutions. A fragile network is vulnerable to targeted shocks.
        
        **Interpretation:**
        - Higher R = More concentrated, fragile network
        - Lower R = More distributed, resilient network
        - Range: 1/N (perfectly distributed) to 1 (maximally concentrated)
        
        **Use case:** Assess structural resilience. High fragility suggests the network is vulnerable to 
        failure of key nodes.
        """)
    
    with st.expander("**Cross-Risk Matrix (Δij)**"):
        st.markdown("""
        **What it is:** Quantifies spillover effects between institutions.
        
        **Formula:** `Δij = (∂²S)/(∂Ci∂Cj)` - the cross-partial derivative of S.
        
        **What it measures:** How a change in institution i's stress affects the marginal risk contribution 
        of institution j. Captures risk amplification through network connections.
        
        **Interpretation:**
        - Δij > 0: Institutions i and j amplify each other's risk
        - Diagonal elements (Δii): Self-amplification (own risk sensitivity)
        - Off-diagonal elements: Cross-institution spillover effects
        
        **Use case:** Identify which institution pairs have the strongest risk linkages. Useful for 
        understanding contagion pathways.
        """)
    
    with st.expander("**Risk Increment (I)**"):
        st.markdown("""
        **What it is:** Measures how much an institution increases systemic risk relative to its own stress.
        
        **Formula:** `Ii = Di / Ci` (risk decomposition divided by compromise score).
        
        **What it measures:** The leverage or amplification factor - how much systemic impact an institution 
        has per unit of its own stress. High increment means the institution's stress is amplified by network effects.
        
        **Interpretation:**
        - Higher I = Greater risk amplification through network
        - Institutions with high I are risk multipliers
        - Undefined when Ci = 0
        
        **Use case:** Identify institutions whose stress has outsized systemic impact due to network position.
        """)
    
    st.markdown("---")
    
    # Input Requirements
    with st.expander("📋 Input Data Requirements", expanded=False):
        st.markdown("""
        ### Institution Data
        
        A CSV or Excel file with the following columns:
        - **InstitutionID**: Unique identifier for each institution (integer or string)
        - **Name**: Human-readable name of the institution
        - **CompromiseScore**: Numeric measure of institution stress/vulnerability
        
        **Compromise Score Guidance:**
        - Represents vulnerability, stress level, or probability of default
        - Values typically range from 0 (no stress) to higher values (high stress)
        - Can be based on financial ratios, credit ratings, market indicators, etc.
        - Should be non-negative
        - Higher values = greater vulnerability
        
        ### Adjacency Matrix
        
        A CSV or Excel file representing network connections:
        - **Format:** Square matrix with institutions as both rows and columns
        - **Values:** Connection strengths (e.g., exposure amounts, lending volumes)
        - **Interpretation:** Element (i,j) represents the connection from institution i to institution j
        - **Diagonal:** Usually zero (no self-loops) but can contain values
        - **Symmetry:** Matrix can be symmetric (undirected) or asymmetric (directed)
        
        ### Data Validation Rules
        
        The application will check:
        - ✅ Required columns are present
        - ✅ No missing values in critical fields
        - ✅ Compromise scores are non-negative
        - ✅ Adjacency matrix is square
        - ✅ Institution IDs match between datasets
        - ✅ Data types are correct
        
        **Tip:** Use the "Validate Data" button on the Data Upload page to check your data before proceeding.
        """)
    
    st.markdown("---")
    
    st.info("""
    💡 **Ready to get started?** Click on **Data Upload** in the navigation sidebar to load data and begin your analysis.
    """)

elif page == "Data Upload":
    st.header("📤 Data Upload and Validation")
    
    st.info("💡 **Getting Started:** Upload your institution data and network adjacency matrix, or load the sample dataset to explore the app's capabilities.")

    st.subheader("Load Sample Dataset")
    st.markdown("Click the button below to automatically load the sample test case with 5 institutions.")
    if st.button("Load Sample Data"):
        try:
            # Construct paths relative to the app's script location
            base_path = os.path.dirname(__file__)
            inst_path = os.path.join(base_path, 'data', 'sample_data', 'das_2016_institutions.csv')
            adj_path = os.path.join(base_path, 'data', 'sample_data', 'das_2016_adjacency.csv')

            st.session_state.institution_df = pd.read_csv(inst_path)
            st.session_state.adjacency_df = pd.read_csv(adj_path, index_col=0)
            st.success("Sample data loaded successfully! You can now validate it below or proceed to the Results Dashboard.")
        except FileNotFoundError:
            st.error("Sample data files not found. Make sure the 'data/sample_data' directory exists.")
        except Exception as e:
            st.error(f"An error occurred while loading the sample data: {e}")
    
    st.markdown("---")
    st.subheader("Or, Upload Your Own Data")
    
    with st.expander("📋 What data do I need?", expanded=False):
        st.markdown("""
        You need two files:
        
        **1. Institution Data (CSV/Excel)**
        - Required columns: `InstitutionID`, `Name`, `CompromiseScore`
        - CompromiseScore: measures stress/vulnerability (0 = no stress, higher = more stress)
        
        **2. Adjacency Matrix (CSV/Excel)**
        - Square matrix with institutions as rows and columns
        - Values represent connection strengths (e.g., exposures, lending amounts)
        - Element (i,j) = connection from institution i to institution j
        
        💡 **Tip:** Check the **About** page for detailed format specifications.
        """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Institution Data")
        st.caption("CSV/Excel with InstitutionID, Name, and CompromiseScore columns")
        institution_file = st.file_uploader(
            "Upload Institution Data (CSV or Excel)", 
            type=['csv', 'xlsx', 'xls'], 
            key='institution_uploader'
        )
        if institution_file:
            st.session_state.institution_df = load_data(institution_file, has_index_col=False)
        
        with st.expander("ℹ️ What is a Compromise Score?"):
            st.markdown("""
            A **compromise score** represents the vulnerability or stress level of an institution.
            
            **Common interpretations:**
            - Financial distress indicator (e.g., based on capital ratios)
            - Probability of default
            - Credit rating score
            - Market-based risk measure
            
            **Guidelines:**
            - Values should be non-negative
            - Higher values = greater vulnerability
            - Zero means no stress/vulnerability
            - Can be normalized or in original units
            """)

    with col2:
        st.subheader("Adjacency Matrix")
        st.caption("Square matrix representing network connections")
        adjacency_file = st.file_uploader(
            "Upload Adjacency Matrix (CSV or Excel)", 
            type=['csv', 'xlsx', 'xls'], 
            key='adjacency_uploader'
        )
        if adjacency_file:
            st.session_state.adjacency_df = load_data(adjacency_file, has_index_col=True)
        
        with st.expander("ℹ️ What is an Adjacency Matrix?"):
            st.markdown("""
            An **adjacency matrix** represents connections between institutions in the network.
            
            **Structure:**
            - Rows and columns = institutions (same order)
            - Element (i,j) = strength of connection from i to j
            - Can be symmetric (undirected) or asymmetric (directed)
            
            **Connection values can represent:**
            - Lending/borrowing amounts
            - Exposure sizes
            - Transaction volumes
            - Any measure of financial interconnection
            
            **Note:** Diagonal elements are typically zero (no self-connections).
            """)


    st.markdown("---")
    
    st.subheader("Validate Your Data")
    st.caption("Check that your data meets all requirements before proceeding")

    if st.button("Validate Data"):
        if st.session_state.institution_df is not None:
            is_valid, errors = validate_institution_data(st.session_state.institution_df)
            if is_valid:
                st.success("✅ Institution data is valid.")
            else:
                for error in errors:
                    st.error(f"❌ Institution Data Error: {error}")
        else:
            st.warning("⚠️ No institution data loaded yet.")
        
        if st.session_state.adjacency_df is not None:
            is_valid, errors = validate_adjacency_matrix(st.session_state.adjacency_df)
            if is_valid:
                st.success("✅ Adjacency matrix is valid.")
            else:
                for error in errors:
                    st.error(f"❌ Adjacency Matrix Error: {error}")
        else:
            st.warning("⚠️ No adjacency matrix loaded yet.")

    st.subheader("Data Preview")
    if st.session_state.institution_df is not None:
        st.write("Institution Data:")
        st.dataframe(st.session_state.institution_df.head())
    
    if st.session_state.adjacency_df is not None:
        st.write("Adjacency Matrix:")
        st.dataframe(st.session_state.adjacency_df.head())


elif page == "Network Construction":
    st.header("2. Network Construction")
    st.write("Construct or upload your network adjacency matrix.")
    
    if st.session_state.get('adjacency_df') is not None and st.session_state.get('institution_df') is not None:
        adj_df = st.session_state.adjacency_df
        inst_df = st.session_state.institution_df
        
        # Network Graph Visualization
        st.subheader("Network Graph Visualization")
        st.write("##### Interactive Network Topology")
        
        # Create two columns: one for the graph, one for the legend table
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Use compromise scores for initial visualization
            node_size_metric = inst_df['CompromiseScore'].values
            node_color_metric = inst_df['CompromiseScore'].values
            
            fig_network = create_network_graph(
                adjacency_df=adj_df,
                institution_names=inst_df['Name'],
                node_size_metric=pd.Series(node_size_metric),
                node_color_metric=pd.Series(node_color_metric),
                size_label="Compromise Score",
                color_label="Compromise Score"
            )
            st.plotly_chart(fig_network, use_container_width=True)
            st.info("📊 **Note:** Node sizes are scaled proportionally to their compromise scores. Larger nodes indicate higher compromise scores.")
        
        with col2:
            st.write("##### Node Legend")
            # Create a table with node numbers and compromise scores
            legend_data = pd.DataFrame({
                'Node': [i+1 for i in range(len(inst_df))],
                'Name': inst_df['Name'].values,
                'Score': inst_df['CompromiseScore'].values
            })
            st.dataframe(
                legend_data.style.format({'Score': '{:.2f}'}),
                hide_index=True,
                height=400
            )
        
        st.markdown("---")
        
        # Adjacency Matrix Heatmap
        st.subheader("Adjacency Matrix Heatmap")
        
        # Create two columns: one for the heatmap, one for the table
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_heatmap = px.imshow(
                adj_df,
                labels=dict(x="Institution", y="Institution", color="Connection Strength"),
                x=adj_df.columns,
                y=adj_df.index,
                color_continuous_scale='Greys'
            )
            fig_heatmap.update_layout(title="Adjacency Matrix Heatmap")
            st.plotly_chart(fig_heatmap, use_container_width=True)
            st.info("This heatmap shows the connection strengths from your uploaded adjacency matrix.")
        
        with col2:
            st.write("##### Adjacency Matrix Data")
            st.dataframe(
                adj_df.style.format("{:.0f}"),
                height=500
            )
    else:
        st.warning("No data uploaded. Please upload both Institution Data and Adjacency Matrix on the 'Data Upload' page.")


elif page == "Results Dashboard":
    st.header("📊 Results Dashboard")
    st.info("💡 **Tip:** Calculate metrics to see detailed risk analysis. Hover over metrics for quick explanations, or expand sections below charts for detailed interpretations.")

    if st.session_state.institution_df is not None and st.session_state.adjacency_df is not None:
        if st.button("Calculate All Metrics"):
            try:
                # Prepare inputs
                compromise_vector = st.session_state.institution_df['CompromiseScore']
                adjacency_matrix = st.session_state.adjacency_df
                
                # Initialize calculator and compute all metrics
                calculator = SystemicRiskCalculator(compromise_vector, adjacency_matrix)
                st.session_state.systemic_risk_score = calculator.S
                st.session_state.risk_decomposition = calculator.calculate_risk_decomposition()
                st.session_state.centrality = calculator.calculate_centrality()
                st.session_state.criticality = calculator.calculate_criticality()
                st.session_state.fragility = calculator.calculate_fragility()
                st.session_state.normalized_score = calculator.calculate_normalized_score()
                st.session_state.cross_risk_matrix = calculator.calculate_cross_risk()
                st.session_state.risk_increment = calculator.calculate_risk_increment()
                st.session_state.node_degrees = calculator.calculate_node_degrees()
                
                st.success("All metrics calculated successfully!")

            except (ValueError, RuntimeError) as e:
                st.error(f"Error during calculation: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

        # --- Display Metrics ---
        if st.session_state.get('systemic_risk_score') is not None:
            try:
                st.subheader("Key Risk Indicators")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        label="Systemic Risk Score (S)",
                        value=f"{st.session_state.systemic_risk_score:.4f}",
                        help="S = √(C'EC). Aggregate systemic risk combining individual stress and network structure. Higher values = greater systemic risk."
                    )
                with col2:
                    st.metric(
                        label="Network Fragility (R)",
                        value=f"{st.session_state.fragility:.4f}",
                        help="R = Σ(ki/K)². Measures connection concentration. Higher values indicate a more fragile, concentrated network structure."
                    )
                with col3:
                    st.metric(
                        label="Normalized Risk Score (S̄)",
                        value=f"{st.session_state.normalized_score:.4f}",
                        help="S̄ = S/√(C'C). Isolates the network effect. S̄ > 1 means network amplifies risk; S̄ < 1 means network dampens risk."
                    )
                
                st.markdown("---")
                
                # --- Display Plots ---
                st.subheader("Detailed Analysis Plots")

                # Risk Decomposition - Ordered from high to low
                st.write("##### Risk Decomposition (Di)")
                decomp_df = pd.DataFrame({
                    'Institution': st.session_state.institution_df['InstitutionID'],
                    'Risk Contribution': st.session_state.risk_decomposition
                }).sort_values('Risk Contribution', ascending=False)
                
                fig_decomp = px.bar(
                    decomp_df,
                    x='Institution',
                    y='Risk Contribution',
                    title='Risk Decomposition by Institution (Ordered High to Low)',
                    color='Risk Contribution',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig_decomp, use_container_width=True)
                
                with st.expander("📚 Understanding Risk Decomposition"):
                    st.markdown("""
                    **Formula:** `Di = Ci × (∂S/∂Ci)`
                    
                    **What it shows:** How much each institution contributes to the total systemic risk score (S).
                    
                    **Key insights:**
                    - Institutions with high Di are systemically important
                    - The sum of all Di equals S (perfect decomposition property)
                    - High contribution can come from high compromise score, strategic network position, or both
                    
                    **Use this to:** Identify which institutions to prioritize for monitoring, stress testing, or regulatory intervention.
                    """)
                
                # Centrality - Ordered from high to low
                st.write("##### Centrality")
                centrality_df = pd.DataFrame({
                    'Institution': st.session_state.institution_df['InstitutionID'],
                    'Centrality': st.session_state.centrality
                }).sort_values('Centrality', ascending=False)
                
                fig_centrality = px.bar(
                    centrality_df,
                    x='Institution',
                    y='Centrality',
                    title='Network Centrality by Institution (Ordered High to Low)',
                    color='Centrality',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_centrality, use_container_width=True)
                
                with st.expander("📚 Understanding Centrality"):
                    st.markdown("""
                    **Formula:** Based on node degree (sum of connections)
                    
                    **What it shows:** How connected each institution is within the network structure.
                    
                    **Key insights:**
                    - High centrality = many or strong connections to other institutions
                    - Central institutions act as hubs in the network
                    - Purely structural measure (independent of compromise scores)
                    - Central institutions can amplify or absorb shocks
                    
                    **Use this to:** Identify network hubs that could spread or contain contagion, regardless of current stress levels.
                    """)
                
                # Criticality - Ordered from high to low
                st.write("##### Criticality")
                criticality_df = pd.DataFrame({
                    'Institution': st.session_state.institution_df['InstitutionID'],
                    'Criticality': st.session_state.criticality
                }).sort_values('Criticality', ascending=False)
                
                fig_criticality = px.bar(
                    criticality_df,
                    x='Institution',
                    y='Criticality',
                    title='Network Criticality by Institution (Ordered High to Low)',
                    color='Criticality',
                    color_continuous_scale='Oranges'
                )
                st.plotly_chart(fig_criticality, use_container_width=True)
                
                with st.expander("📚 Understanding Criticality"):
                    st.markdown("""
                    **Formula:** Combines centrality with compromise score
                    
                    **What it shows:** Risk-weighted importance of each institution.
                    
                    **Key insights:**
                    - High criticality = institution is both connected AND stressed
                    - More actionable than centrality alone
                    - Identifies institutions that pose the greatest immediate systemic threat
                    - An institution can be critical due to high stress, strategic position, or both
                    
                    **Use this to:** Prioritize intervention targets - focus on institutions that are both vulnerable and structurally important.
                    """)
                
                # Risk Increment - Ordered from high to low
                if st.session_state.get('risk_increment') is not None:
                    st.write("##### Risk Increment (Ii)")
                    risk_increment_df = pd.DataFrame({
                        'Institution': st.session_state.institution_df['InstitutionID'],
                        'Risk Increment': st.session_state.risk_increment
                    }).sort_values('Risk Increment', ascending=False)
                    
                    # Display the data table to verify values
                    with st.expander("View Risk Increment Data"):
                        st.dataframe(risk_increment_df.style.format({'Risk Increment': '{:.6f}'}))
                    
                    fig_risk_increment = px.bar(
                        risk_increment_df,
                        x='Institution',
                        y='Risk Increment',
                        title='Risk Increment by Institution (Ordered High to Low)',
                        color='Risk Increment',
                        color_continuous_scale='Purples'
                    )
                    st.plotly_chart(fig_risk_increment, use_container_width=True)
                    
                    with st.expander("📚 Understanding Risk Increment"):
                        st.markdown("""
                        **Formula:** `Ii = Di / Ci` (risk decomposition divided by compromise score)
                        
                        **What it shows:** How much systemic impact an institution has per unit of its own stress.
                        
                        **Key insights:**
                        - High increment = risk amplification through network effects
                        - Institutions with high I are risk multipliers
                        - Shows network leverage: a small increase in stress causes large systemic impact
                        - Undefined when Ci = 0
                        
                        **Use this to:** Identify institutions whose stress has outsized systemic consequences due to their network position.
                        """)
                
                # Node Degrees (related to Fragility) - Ordered from high to low
                if st.session_state.get('node_degrees') is not None:
                    st.write("##### Node Degrees (Network Connectivity)")
                    node_degrees_df = pd.DataFrame({
                        'Institution': st.session_state.institution_df['InstitutionID'],
                        'Node Degree': st.session_state.node_degrees
                    }).sort_values('Node Degree', ascending=False)
                    
                    # Display the data table to verify values
                    with st.expander("View Node Degree Data"):
                        st.dataframe(node_degrees_df.style.format({'Node Degree': '{:.2f}'}))
                    
                    fig_node_degrees = px.bar(
                        node_degrees_df,
                        x='Institution',
                        y='Node Degree',
                        title='Node Degrees by Institution (Ordered High to Low)',
                        color='Node Degree',
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig_node_degrees, use_container_width=True)
                    
                    with st.expander("📚 Understanding Node Degrees & Fragility"):
                        st.markdown(f"""
                        **Formula:** Node Degree = sum of all connections (incoming + outgoing)
                        
                        **What it shows:** Total connection strength for each institution.
                        
                        **Relationship to Fragility:**
                        - Current Network Fragility (R) = {st.session_state.fragility:.4f}
                        - Fragility formula: `R = Σ(ki/K)²` where ki is node i's degree
                        - Higher fragility = connections concentrated in fewer nodes
                        - Lower fragility = connections distributed across many nodes
                        
                        **Key insights:**
                        - Institutions with high node degrees dominate the network structure
                        - Concentrated connections (high R) make the network vulnerable to targeted shocks
                        - Distributed connections (low R) indicate structural resilience
                        
                        **Use this to:** Assess structural vulnerability and identify concentration risk in network topology.
                        """)

                st.markdown("---")
                
                # --- Display Network Visualizations ---
                st.subheader("Network Visualizations")
                
                # Interactive Network Graph
                st.write("##### Interactive Network Graph")
                available_metrics = {
                    "Risk Contribution": st.session_state.risk_decomposition,
                    "Centrality": st.session_state.centrality,
                    "Criticality": st.session_state.criticality,
                    "Compromise Score": st.session_state.institution_df['CompromiseScore'].values
                }
                col1, col2 = st.columns(2)
                with col1:
                    size_metric_label = st.selectbox("Select Node Size Metric:", options=list(available_metrics.keys()))
                with col2:
                    color_metric_label = st.selectbox("Select Node Color Metric:", options=list(available_metrics.keys()), index=1)
                
                fig_network = create_network_graph(
                    adjacency_df=st.session_state.adjacency_df,
                    institution_names=st.session_state.institution_df['Name'],
                    node_size_metric=pd.Series(available_metrics[size_metric_label]),
                    node_color_metric=pd.Series(available_metrics[color_metric_label]),
                    size_label=size_metric_label,
                    color_label=color_metric_label
                )
                st.plotly_chart(fig_network, use_container_width=True)

                # Cross-Risk Heatmap
                st.write("##### Cross-Risk Spillover Matrix (Δij)")
                cross_risk_df = st.session_state.cross_risk_matrix
                
                # Reverse the y-axis so institution 1 is at the top (origin)
                cross_risk_df_display = cross_risk_df.iloc[::-1]
                
                fig_heatmap = px.imshow(
                    cross_risk_df_display,
                    labels=dict(x="Influenced Institution (j) →", y="↓ Influencing Institution (i)", color="Spillover Effect"),
                    x=cross_risk_df.columns,
                    y=cross_risk_df_display.index,
                    color_continuous_scale='Reds',
                    aspect='auto'
                )
                fig_heatmap.update_layout(
                    title="Cross-Risk Spillover Matrix (Δij = ∂Di/∂Cj)<br><sub>Shows how changes in institution j's compromise affect institution i's risk</sub>",
                    xaxis_title="Influenced Institution (j)",
                    yaxis_title="Influencing Institution (i)"
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
                
                with st.expander("📚 Understanding Cross-Risk Spillover Matrix"):
                    st.markdown("""
                    **Formula:** `Δij = ∂²S/(∂Ci∂Cj)` - the cross-partial derivative of systemic risk
                    
                    **What it shows:** How changes in one institution's stress affect another's risk contribution.
                    
                    **How to read the matrix:**
                    - Rows (i): Influencing institution
                    - Columns (j): Influenced institution
                    - Cell (i,j): How much institution i's risk changes when j's stress increases
                    - Diagonal (Δii): Self-amplification effect
                    - Off-diagonal: Cross-institution spillover effects
                    
                    **Key insights:**
                    - High Δij = strong risk linkage between institutions i and j
                    - Positive values indicate risk amplification
                    - Identifies contagion pathways in the network
                    - Asymmetric matrix shows directional spillover effects
                    
                    **Use this to:** Understand risk propagation channels and identify which institution pairs have the strongest risk interdependencies.
                    """)
            except Exception as e:
                st.error(f"An error occurred while displaying the results. This might be due to a calculation error. Please review the error messages above. Details: {e}")
        else:
            st.info("Click 'Calculate All Metrics' to generate the dashboard.")
    else:
        st.warning("Please upload and validate both Institution Data and Adjacency Matrix on the 'Data Upload' page first.")

elif page == "Scenario Analysis":
    st.header("🔬 Scenario Analysis")
    st.info("💡 **Tip:** Use these tools to test different scenarios and understand how changes affect systemic risk. Each tab offers different types of analysis.")
    
    if st.session_state.institution_df is not None and st.session_state.adjacency_df is not None:
        
        # Create tabs for different scenario types
        scenario_tab1, scenario_tab2, scenario_tab3 = st.tabs([
            "📊 Sensitivity to Compromise Scores", 
            "🏦 Institution Removal", 
            "🔗 Network Modification"
        ])
        
        # --- Sensitivity to Compromise Scores Tab ---
        with scenario_tab1:
            st.subheader("Sensitivity Analysis: Adjust Compromise Scores")
            st.info("""
            ℹ️ **What this does:** Test how sensitive the system is to changes in individual institution stress levels. 
            Adjust compromise scores to simulate stress scenarios (increase scores) or recovery paths (decrease scores).
            
            **Use cases:** Stress testing, recovery planning, identifying systemic sensitivities.
            """)
            
            # Get original data
            original_compromise = st.session_state.institution_df['CompromiseScore'].copy()
            original_adjacency = st.session_state.adjacency_df.copy()
            
            # Initialize modified compromise if not exists
            if st.session_state.scenario_modifications['modified_compromise'] is None:
                st.session_state.scenario_modifications['modified_compromise'] = original_compromise.copy()
            
            st.write("##### Adjust Individual Institution Scores")
            
            # Create two columns for before/after comparison
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Original Scores**")
                original_df = pd.DataFrame({
                    'Institution': st.session_state.institution_df['Name'],
                    'Original Score': original_compromise
                })
                st.dataframe(original_df, height=300)
            
            with col2:
                st.write("**Modified Scores**")
                modified_scores = st.session_state.scenario_modifications['modified_compromise'].copy()
                
                # Sliders for each institution
                for idx, (inst_id, inst_name) in enumerate(zip(
                    st.session_state.institution_df['InstitutionID'],
                    st.session_state.institution_df['Name']
                )):
                    original_val = float(original_compromise.iloc[idx])
                    modified_scores.iloc[idx] = st.slider(
                        f"{inst_name} (Original: {original_val:.2f})",
                        min_value=0.0,
                        max_value=max(10.0, original_val * 2),
                        value=float(modified_scores.iloc[idx]),
                        step=0.1,
                        key=f"whatif_slider_{idx}",
                        help=f"Adjust the compromise score for {inst_name}. Higher values = greater stress/vulnerability."
                    )
                
                st.session_state.scenario_modifications['modified_compromise'] = modified_scores
            
            # Reset button
            if st.button("Reset to Original Scores", key="reset_whatif"):
                st.session_state.scenario_modifications['modified_compromise'] = original_compromise.copy()
                st.rerun()
            
            st.markdown("---")
            
            # Calculate and compare metrics
            if st.button("Calculate Impact", type="primary"):
                try:
                    # Original metrics
                    calc_original = SystemicRiskCalculator(original_compromise, original_adjacency)
                    original_S = calc_original.S
                    original_decomp = calc_original.calculate_risk_decomposition()
                    original_criticality = calc_original.calculate_criticality()
                    original_cross_risk = calc_original.calculate_cross_risk()
                    
                    # Modified metrics
                    calc_modified = SystemicRiskCalculator(modified_scores, original_adjacency)
                    modified_S = calc_modified.S
                    modified_decomp = calc_modified.calculate_risk_decomposition()
                    modified_criticality = calc_modified.calculate_criticality()
                    modified_cross_risk = calc_modified.calculate_cross_risk()
                    
                    st.success("Impact calculated successfully!")
                    
                    # Display comparison
                    st.subheader("Impact Analysis")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            "Original Systemic Risk (S)",
                            f"{original_S:.4f}"
                        )
                    with col2:
                        st.metric(
                            "Modified Systemic Risk (S)",
                            f"{modified_S:.4f}",
                            delta=f"{modified_S - original_S:.4f}"
                        )
                    with col3:
                        change_pct = ((modified_S - original_S) / original_S * 100) if original_S != 0 else 0
                        st.metric(
                            "Change (%)",
                            f"{change_pct:.2f}%"
                        )
                    
                    # Risk decomposition comparison
                    st.write("##### Risk Decomposition Comparison")
                    comparison_df = pd.DataFrame({
                        'Institution': st.session_state.institution_df['Name'],
                        'Original Risk': original_decomp,
                        'Modified Risk': modified_decomp,
                        'Difference': modified_decomp - original_decomp
                    }).sort_values('Difference', ascending=False)
                    
                    fig_comparison = px.bar(
                        comparison_df,
                        x='Institution',
                        y=['Original Risk', 'Modified Risk'],
                        title='Risk Decomposition: Original vs Modified',
                        barmode='group',
                        color_discrete_sequence=['#636EFA', '#EF553B']
                    )
                    st.plotly_chart(fig_comparison, use_container_width=True, key="sensitivity_risk_decomp")
                    
                    st.dataframe(comparison_df.style.format({
                        'Original Risk': '{:.4f}',
                        'Modified Risk': '{:.4f}',
                        'Difference': '{:.4f}'
                    }))
                    
                    st.markdown("---")
                    
                    # Criticality comparison
                    st.write("##### Criticality Comparison")
                    criticality_df = pd.DataFrame({
                        'Institution': st.session_state.institution_df['Name'],
                        'Original Criticality': original_criticality,
                        'Modified Criticality': modified_criticality,
                        'Difference': modified_criticality - original_criticality
                    }).sort_values('Difference', ascending=False)
                    
                    fig_criticality = px.bar(
                        criticality_df,
                        x='Institution',
                        y=['Original Criticality', 'Modified Criticality'],
                        title='Criticality: Original vs Modified',
                        barmode='group',
                        color_discrete_sequence=['#FFA15A', '#19D3F3']
                    )
                    st.plotly_chart(fig_criticality, use_container_width=True, key="sensitivity_criticality")
                    
                    st.dataframe(criticality_df.style.format({
                        'Original Criticality': '{:.4f}',
                        'Modified Criticality': '{:.4f}',
                        'Difference': '{:.4f}'
                    }))
                    
                    st.markdown("---")
                    
                    # Cross-Risk Analysis
                    st.write("##### Cross-Risk Spillover Matrix Comparison")
                    st.write("Shows how changes in one institution's compromise score affect others' risk contributions.")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Original Cross-Risk Matrix**")
                        # Reverse y-axis for proper display
                        original_cross_risk_display = pd.DataFrame(
                            original_cross_risk,
                            index=original_adjacency.index,
                            columns=original_adjacency.columns
                        ).iloc[::-1]
                        
                        fig_cross_orig = px.imshow(
                            original_cross_risk_display,
                            labels=dict(x="Influenced Institution (j)", y="Influencing Institution (i)", color="Spillover"),
                            color_continuous_scale='Reds',
                            aspect='auto'
                        )
                        fig_cross_orig.update_layout(title="Original Cross-Risk")
                        st.plotly_chart(fig_cross_orig, use_container_width=True, key="sensitivity_cross_risk_orig")
                    
                    with col2:
                        st.write("**Modified Cross-Risk Matrix**")
                        modified_cross_risk_display = pd.DataFrame(
                            modified_cross_risk,
                            index=original_adjacency.index,
                            columns=original_adjacency.columns
                        ).iloc[::-1]
                        
                        fig_cross_mod = px.imshow(
                            modified_cross_risk_display,
                            labels=dict(x="Influenced Institution (j)", y="Influencing Institution (i)", color="Spillover"),
                            color_continuous_scale='Reds',
                            aspect='auto'
                        )
                        fig_cross_mod.update_layout(title="Modified Cross-Risk")
                        st.plotly_chart(fig_cross_mod, use_container_width=True, key="sensitivity_cross_risk_mod")
                    
                    # Cross-risk difference heatmap
                    st.write("**Cross-Risk Change Matrix (Modified - Original)**")
                    cross_risk_diff = modified_cross_risk - original_cross_risk
                    cross_risk_diff_display = pd.DataFrame(
                        cross_risk_diff,
                        index=original_adjacency.index,
                        columns=original_adjacency.columns
                    ).iloc[::-1]
                    
                    fig_cross_diff = px.imshow(
                        cross_risk_diff_display,
                        labels=dict(x="Influenced Institution (j)", y="Influencing Institution (i)", color="Change"),
                        color_continuous_scale='RdBu_r',
                        aspect='auto'
                    )
                    fig_cross_diff.update_layout(title="Cross-Risk Change (Red = Increase, Blue = Decrease)")
                    st.plotly_chart(fig_cross_diff, use_container_width=True, key="sensitivity_cross_risk_diff")
                    
                    st.info("💡 The cross-risk matrix shows ∂Di/∂Cj: how much institution i's risk contribution changes when institution j's compromise score changes.")
                    
                except Exception as e:
                    st.error(f"Error calculating impact: {e}")
        
        # --- Institution Removal Tab ---
        with scenario_tab2:
            st.subheader("Institution Removal Simulation")
            st.info("""
            ℹ️ **What this does:** Simulate the removal of one or more institutions to assess contagion risk and network resilience.
            
            **Use cases:** Identifying systemically important institutions (SIFIs), stress testing network resilience, 
            evaluating the impact of defaults or exits.
            
            **Note:** Removing an institution with zero compromise score may not change systemic risk S, but will affect fragility R.
            """)
            
            # Institution selection
            available_institutions = st.session_state.institution_df['Name'].tolist()
            
            selected_to_remove = st.multiselect(
                "Select institutions to remove:",
                options=available_institutions,
                default=st.session_state.scenario_modifications.get('removed_institutions', []),
                key="remove_institutions",
                help="Choose one or more institutions to simulate their removal from the network. This helps identify systemically important institutions."
            )
            
            st.session_state.scenario_modifications['removed_institutions'] = selected_to_remove
            
            if st.button("Simulate Removal", type="primary", key="simulate_removal"):
                if not selected_to_remove:
                    st.warning("Please select at least one institution to remove.")
                else:
                    try:
                        # Get indices to remove
                        indices_to_remove = [
                            i for i, name in enumerate(st.session_state.institution_df['Name'])
                            if name in selected_to_remove
                        ]
                        
                        # Create mask for remaining institutions
                        mask = [i not in indices_to_remove for i in range(len(st.session_state.institution_df))]
                        
                        # Original metrics
                        calc_original = SystemicRiskCalculator(
                            st.session_state.institution_df['CompromiseScore'],
                            st.session_state.adjacency_df
                        )
                        original_S = calc_original.S
                        original_fragility = calc_original.calculate_fragility()
                        
                        # Modified data (after removal)
                        modified_compromise = st.session_state.institution_df['CompromiseScore'].iloc[mask]
                        modified_adjacency = st.session_state.adjacency_df.iloc[mask, mask]
                        
                        # Modified metrics
                        calc_modified = SystemicRiskCalculator(modified_compromise, modified_adjacency)
                        modified_S = calc_modified.S
                        modified_fragility = calc_modified.calculate_fragility()
                        
                        st.success(f"Simulation complete! Removed {len(selected_to_remove)} institution(s).")
                        
                        # Display results
                        st.subheader("Removal Impact Analysis")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                "Original Network Size",
                                f"{len(st.session_state.institution_df)} institutions"
                            )
                            st.metric(
                                "Original Systemic Risk (S)",
                                f"{original_S:.4f}"
                            )
                            st.metric(
                                "Original Fragility (R)",
                                f"{original_fragility:.4f}"
                            )
                        
                        with col2:
                            st.metric(
                                "Modified Network Size",
                                f"{len(modified_compromise)} institutions",
                                delta=f"-{len(selected_to_remove)}"
                            )
                            st.metric(
                                "Modified Systemic Risk (S)",
                                f"{modified_S:.4f}",
                                delta=f"{modified_S - original_S:.4f}"
                            )
                            st.metric(
                                "Modified Fragility (R)",
                                f"{modified_fragility:.4f}",
                                delta=f"{modified_fragility - original_fragility:.4f}"
                            )
                        
                        # Show removed institutions
                        st.write("##### Removed Institutions:")
                        removed_df = st.session_state.institution_df[
                            st.session_state.institution_df['Name'].isin(selected_to_remove)
                        ][['Name', 'CompromiseScore']]
                        st.dataframe(removed_df)
                        
                        # Network visualization comparison
                        st.write("##### Network Visualization")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Original Network**")
                            fig_original = create_network_graph(
                                adjacency_df=st.session_state.adjacency_df,
                                institution_names=st.session_state.institution_df['Name'],
                                node_size_metric=st.session_state.institution_df['CompromiseScore'],
                                node_color_metric=st.session_state.institution_df['CompromiseScore'],
                                size_label="Compromise Score",
                                color_label="Compromise Score"
                            )
                            st.plotly_chart(fig_original, use_container_width=True)
                        
                        with col2:
                            st.write("**After Removal**")
                            remaining_names = st.session_state.institution_df['Name'].iloc[mask]
                            fig_modified = create_network_graph(
                                adjacency_df=modified_adjacency,
                                institution_names=remaining_names,
                                node_size_metric=pd.Series(modified_compromise.values),
                                node_color_metric=pd.Series(modified_compromise.values),
                                size_label="Compromise Score",
                                color_label="Compromise Score"
                            )
                            st.plotly_chart(fig_modified, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"Error simulating removal: {e}")
        
        # --- Network Modification Tab ---
        with scenario_tab3:
            st.subheader("Network Connection Modification")
            st.info("""
            ℹ️ **What this does:** Test how changes to connection strengths affect systemic risk. 
            Adjust network connections to simulate policy interventions like lending restrictions or new partnerships.
            
            **Use cases:** Evaluating regulatory interventions, testing network restructuring, assessing impact of 
            new connections or exposure limits.
            
            **Tip:** Use the sliders to modify connection weights, then calculate the impact to see changes in systemic risk and fragility.
            """)
            
            # Initialize modified adjacency if not exists
            if st.session_state.scenario_modifications['modified_adjacency'] is None:
                st.session_state.scenario_modifications['modified_adjacency'] = st.session_state.adjacency_df.copy()
            
            modified_adj = st.session_state.scenario_modifications['modified_adjacency'].copy()
            
            st.write("##### Modify Network Connections")
            
            # Show current adjacency matrix with editing capability
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write("**Select Connection to Modify**")
                
                institutions = st.session_state.institution_df['Name'].tolist()
                
                from_inst = st.selectbox(
                    "From Institution:",
                    options=institutions,
                    key="network_mod_from",
                    help="Select the source institution for the connection you want to modify."
                )
                
                to_inst = st.selectbox(
                    "To Institution:",
                    options=institutions,
                    key="network_mod_to",
                    help="Select the target institution for the connection you want to modify."
                )
                
                from_idx = institutions.index(from_inst)
                to_idx = institutions.index(to_inst)
                
                current_value = float(modified_adj.iloc[from_idx, to_idx])
                
                new_value = st.slider(
                    f"Connection strength from {from_inst} to {to_inst}:",
                    min_value=0.0,
                    max_value=1.0,
                    value=current_value,
                    step=0.05,
                    key="connection_strength",
                    help=f"Current value: {current_value:.2f}. Adjust to modify the connection strength. 0 = no connection, 1 = maximum connection."
                )
                
                if st.button("Update Connection", key="update_connection"):
                    modified_adj.iloc[from_idx, to_idx] = new_value
                    st.session_state.scenario_modifications['modified_adjacency'] = modified_adj
                    st.success(f"Updated connection from {from_inst} to {to_inst}")
                    st.rerun()
                
                if st.button("Reset Network to Original", key="reset_network"):
                    st.session_state.scenario_modifications['modified_adjacency'] = st.session_state.adjacency_df.copy()
                    st.rerun()
            
            with col2:
                st.write("**Current Adjacency Matrix**")
                st.dataframe(modified_adj.style.format("{:.2f}"), height=400)
            
            st.markdown("---")
            
            # Calculate impact
            if st.button("Calculate Network Modification Impact", type="primary", key="calc_network_impact"):
                try:
                    # Original metrics
                    calc_original = SystemicRiskCalculator(
                        st.session_state.institution_df['CompromiseScore'],
                        st.session_state.adjacency_df
                    )
                    original_S = calc_original.S
                    original_normalized = calc_original.calculate_normalized_score()
                    original_fragility = calc_original.calculate_fragility()
                    original_cross_risk = calc_original.calculate_cross_risk()
                    
                    # Modified metrics
                    calc_modified = SystemicRiskCalculator(
                        st.session_state.institution_df['CompromiseScore'],
                        modified_adj
                    )
                    modified_S = calc_modified.S
                    modified_normalized = calc_modified.calculate_normalized_score()
                    modified_fragility = calc_modified.calculate_fragility()
                    modified_cross_risk = calc_modified.calculate_cross_risk()
                    
                    st.success("Network modification impact calculated!")
                    
                    # Display comparison
                    st.subheader("Network Modification Impact")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(
                            "Original Systemic Risk (S)",
                            f"{original_S:.4f}"
                        )
                    with col2:
                        st.metric(
                            "Modified Systemic Risk (S)",
                            f"{modified_S:.4f}",
                            delta=f"{modified_S - original_S:.4f}"
                        )
                    with col3:
                        st.metric(
                            "Original Fragility (R)",
                            f"{original_fragility:.4f}"
                        )
                    with col4:
                        st.metric(
                            "Modified Fragility (R)",
                            f"{modified_fragility:.4f}",
                            delta=f"{modified_fragility - original_fragility:.4f}"
                        )
                    
                    # Second row of metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "Original Normalized Score",
                            f"{original_normalized:.4f}"
                        )
                    with col2:
                        st.metric(
                            "Modified Normalized Score",
                            f"{modified_normalized:.4f}",
                            delta=f"{modified_normalized - original_normalized:.4f}"
                        )
                    
                    st.markdown("---")
                    
                    # Heatmap comparison
                    st.write("##### Adjacency Matrix Comparison")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Original Network Structure**")
                        fig_orig = px.imshow(
                            st.session_state.adjacency_df,
                            color_continuous_scale='Greys',
                            aspect='auto',
                            labels=dict(color="Connection Strength")
                        )
                        fig_orig.update_layout(title="Original Adjacency Matrix")
                        st.plotly_chart(fig_orig, use_container_width=True, key="network_mod_orig_heatmap")
                    
                    with col2:
                        st.write("**Modified Network Structure**")
                        fig_mod = px.imshow(
                            modified_adj,
                            color_continuous_scale='Greys',
                            aspect='auto',
                            labels=dict(color="Connection Strength")
                        )
                        fig_mod.update_layout(title="Modified Adjacency Matrix")
                        st.plotly_chart(fig_mod, use_container_width=True, key="network_mod_modified_heatmap")
                    
                    st.markdown("---")
                    
                    # Cross-Risk Spillover Analysis
                    st.write("##### Cross-Risk Spillover Impact")
                    st.write("Network structure changes affect how risks propagate between institutions.")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Original Cross-Risk Matrix**")
                        original_cross_risk_display = pd.DataFrame(
                            original_cross_risk,
                            index=st.session_state.adjacency_df.index,
                            columns=st.session_state.adjacency_df.columns
                        ).iloc[::-1]
                        
                        fig_cross_orig = px.imshow(
                            original_cross_risk_display,
                            labels=dict(x="Influenced Institution (j)", y="Influencing Institution (i)", color="Spillover"),
                            color_continuous_scale='Oranges',
                            aspect='auto'
                        )
                        fig_cross_orig.update_layout(title="Original Cross-Risk")
                        st.plotly_chart(fig_cross_orig, use_container_width=True, key="network_mod_cross_orig")
                    
                    with col2:
                        st.write("**Modified Cross-Risk Matrix**")
                        modified_cross_risk_display = pd.DataFrame(
                            modified_cross_risk,
                            index=modified_adj.index,
                            columns=modified_adj.columns
                        ).iloc[::-1]
                        
                        fig_cross_mod = px.imshow(
                            modified_cross_risk_display,
                            labels=dict(x="Influenced Institution (j)", y="Influencing Institution (i)", color="Spillover"),
                            color_continuous_scale='Oranges',
                            aspect='auto'
                        )
                        fig_cross_mod.update_layout(title="Modified Cross-Risk")
                        st.plotly_chart(fig_cross_mod, use_container_width=True, key="network_mod_cross_mod")
                    
                    # Cross-risk difference
                    st.write("**Cross-Risk Change (Modified - Original)**")
                    cross_risk_diff = modified_cross_risk - original_cross_risk
                    cross_risk_diff_display = pd.DataFrame(
                        cross_risk_diff,
                        index=st.session_state.adjacency_df.index,
                        columns=st.session_state.adjacency_df.columns
                    ).iloc[::-1]
                    
                    fig_cross_diff = px.imshow(
                        cross_risk_diff_display,
                        labels=dict(x="Influenced Institution (j)", y="Influencing Institution (i)", color="Change"),
                        color_continuous_scale='RdBu_r',
                        aspect='auto'
                    )
                    fig_cross_diff.update_layout(title="Network Structure Impact on Cross-Risk (Red = Increase, Blue = Decrease)")
                    st.plotly_chart(fig_cross_diff, use_container_width=True, key="network_mod_cross_diff")
                    
                    st.info("💡 Modifying network connections changes how risks spill over between institutions. Stronger connections generally increase spillover effects.")
                    
                except Exception as e:
                    st.error(f"Error calculating network modification impact: {e}")
        
        # Save scenario button
        st.markdown("---")
        st.subheader("💾 Save Current Scenario")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            scenario_name = st.text_input(
                "Scenario Name:",
                placeholder="e.g., 'High Stress Test', 'Bank A Removal'",
                key="save_scenario_name"
            )
        with col2:
            if st.button("Save Scenario", type="primary"):
                if scenario_name:
                    # Save current state
                    st.session_state.saved_scenarios[scenario_name] = {
                        'institution_df': st.session_state.institution_df.copy(),
                        'adjacency_df': st.session_state.adjacency_df.copy(),
                        'modifications': {
                            'modified_compromise': st.session_state.scenario_modifications['modified_compromise'].copy() 
                                if st.session_state.scenario_modifications['modified_compromise'] is not None else None,
                            'modified_adjacency': st.session_state.scenario_modifications['modified_adjacency'].copy()
                                if st.session_state.scenario_modifications['modified_adjacency'] is not None else None,
                            'removed_institutions': st.session_state.scenario_modifications['removed_institutions'].copy()
                        },
                        'timestamp': pd.Timestamp.now()
                    }
                    st.success(f"Scenario '{scenario_name}' saved successfully!")
                else:
                    st.warning("Please enter a scenario name.")
        
        # List saved scenarios
        if st.session_state.saved_scenarios:
            st.write(f"**Saved Scenarios:** {len(st.session_state.saved_scenarios)}")
            scenario_list = pd.DataFrame([
                {'Name': name, 'Saved At': data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
                for name, data in st.session_state.saved_scenarios.items()
            ])
            st.dataframe(scenario_list, hide_index=True)
    else:
        st.warning("Please upload and validate both Institution Data and Adjacency Matrix on the 'Data Upload' page first.")

elif page == "Compare Scenarios":
    st.header("5. Compare Scenarios")
    st.write("Load and compare up to 4 saved scenarios side-by-side.")
    
    if not st.session_state.saved_scenarios:
        st.warning("No saved scenarios found. Please create and save scenarios in the 'Scenario Analysis' page first.")
    else:
        st.subheader("Select Scenarios to Compare")
        
        available_scenarios = list(st.session_state.saved_scenarios.keys())
        
        # Select up to 4 scenarios
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            scenario_1 = st.selectbox("Scenario 1:", ["None"] + available_scenarios, key="compare_1")
        with col2:
            scenario_2 = st.selectbox("Scenario 2:", ["None"] + available_scenarios, key="compare_2")
        with col3:
            scenario_3 = st.selectbox("Scenario 3:", ["None"] + available_scenarios, key="compare_3")
        with col4:
            scenario_4 = st.selectbox("Scenario 4:", ["None"] + available_scenarios, key="compare_4")
        
        selected_scenarios = [s for s in [scenario_1, scenario_2, scenario_3, scenario_4] if s != "None"]
        
        if st.button("Compare Scenarios", type="primary") and len(selected_scenarios) >= 2:
            try:
                # Calculate metrics for each scenario
                comparison_data = []
                
                for scenario_name in selected_scenarios:
                    scenario = st.session_state.saved_scenarios[scenario_name]
                    
                    # Determine which data to use
                    if scenario['modifications']['modified_compromise'] is not None:
                        compromise = scenario['modifications']['modified_compromise']
                    else:
                        compromise = scenario['institution_df']['CompromiseScore']
                    
                    if scenario['modifications']['modified_adjacency'] is not None:
                        adjacency = scenario['modifications']['modified_adjacency']
                    else:
                        adjacency = scenario['adjacency_df']
                    
                    # Calculate metrics
                    calc = SystemicRiskCalculator(compromise, adjacency)
                    
                    comparison_data.append({
                        'Scenario': scenario_name,
                        'Systemic Risk (S)': calc.S,
                        'Normalized Score': calc.calculate_normalized_score(),
                        'Fragility (R)': calc.calculate_fragility(),
                        'Num Institutions': len(compromise),
                        'Avg Compromise': float(compromise.mean())
                    })
                
                comparison_df = pd.DataFrame(comparison_data)
                
                st.success(f"Comparing {len(selected_scenarios)} scenarios")
                
                # Display comparison table
                st.subheader("Scenario Metrics Comparison")
                st.dataframe(
                    comparison_df.style.format({
                        'Systemic Risk (S)': '{:.4f}',
                        'Normalized Score': '{:.4f}',
                        'Fragility (R)': '{:.4f}',
                        'Avg Compromise': '{:.4f}'
                    }),
                    hide_index=True
                )
                
                # Visualizations
                st.subheader("Visual Comparisons")
                
                # Systemic Risk Comparison
                fig_s = px.bar(
                    comparison_df,
                    x='Scenario',
                    y='Systemic Risk (S)',
                    title='Systemic Risk Score Comparison',
                    color='Systemic Risk (S)',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig_s, use_container_width=True)
                
                # Multi-metric comparison
                metrics_to_plot = ['Systemic Risk (S)', 'Normalized Score', 'Fragility (R)']
                
                # Normalize for radar chart
                comparison_normalized = comparison_df.copy()
                for metric in metrics_to_plot:
                    max_val = comparison_normalized[metric].max()
                    if max_val > 0:
                        comparison_normalized[f'{metric}_norm'] = comparison_normalized[metric] / max_val
                
                # Create grouped bar chart
                fig_multi = px.bar(
                    comparison_df.melt(id_vars='Scenario', value_vars=metrics_to_plot),
                    x='Scenario',
                    y='value',
                    color='variable',
                    title='Multi-Metric Comparison',
                    barmode='group',
                    labels={'value': 'Metric Value', 'variable': 'Metric'}
                )
                st.plotly_chart(fig_multi, use_container_width=True)
                
                # Detailed comparison for each scenario
                st.subheader("Detailed Scenario Analysis")
                
                for scenario_name in selected_scenarios:
                    with st.expander(f"📊 {scenario_name} Details"):
                        scenario = st.session_state.saved_scenarios[scenario_name]
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Scenario Information**")
                            st.write(f"- Saved: {scenario['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                            st.write(f"- Institutions: {len(scenario['institution_df'])}")
                            
                            if scenario['modifications']['removed_institutions']:
                                st.write(f"- Removed: {', '.join(scenario['modifications']['removed_institutions'])}")
                        
                        with col2:
                            st.write("**Key Metrics**")
                            scenario_metrics = comparison_df[comparison_df['Scenario'] == scenario_name].iloc[0]
                            st.metric("Systemic Risk", f"{scenario_metrics['Systemic Risk (S)']:.4f}")
                            st.metric("Fragility", f"{scenario_metrics['Fragility (R)']:.4f}")
                
                # Export comparison
                st.markdown("---")
                st.subheader("Export Comparison")
                
                if st.button("Download Comparison as CSV"):
                    csv = comparison_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"scenario_comparison_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
            except Exception as e:
                st.error(f"Error comparing scenarios: {e}")
        
        elif len(selected_scenarios) < 2:
            st.info("Please select at least 2 scenarios to compare.")
        
        # Scenario Management
        st.markdown("---")
        st.subheader("Scenario Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Delete Scenario**")
            scenario_to_delete = st.selectbox(
                "Select scenario to delete:",
                options=available_scenarios,
                key="delete_scenario_select"
            )
            if st.button("Delete", key="delete_scenario_btn"):
                del st.session_state.saved_scenarios[scenario_to_delete]
                st.success(f"Deleted scenario '{scenario_to_delete}'")
                st.rerun()
        
        with col2:
            st.write("**Clear All Scenarios**")
            st.write(f"Total scenarios: {len(available_scenarios)}")
            if st.button("Clear All Scenarios", key="clear_all"):
                st.session_state.saved_scenarios = {}
                st.success("All scenarios cleared")
                st.rerun()

elif page == "Export Results":
    st.header("6. Export Results")
    st.write("Download your analysis and reports in various formats.")

    if st.session_state.get('systemic_risk_score') is not None:
        
        # Create tabs for different export types
        export_tab1, export_tab2, export_tab3, export_tab4 = st.tabs([
            "📊 Excel Export", 
            "📄 PDF Report", 
            "🔢 JSON Data",
            "📈 Chart Exports"
        ])
        
        # --- Excel Export Tab ---
        with export_tab1:
            st.subheader("Export All Data to Excel")
            st.write("Download a comprehensive Excel workbook with all metrics and data.")
            
            # Create a dictionary of all relevant data in the session state
            export_data = {key: st.session_state[key] for key in st.session_state if st.session_state[key] is not None}
            
            # Generate the Excel file in-memory
            excel_data = export_to_excel(export_data)
            
            st.download_button(
                label="📥 Download Excel Report",
                data=excel_data,
                file_name=f"matrix_metrics_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            
            st.info("📋 The Excel file includes: Institution data, Adjacency matrix, All calculated metrics, and Summary statistics.")
        
        # --- PDF Report Tab ---
        with export_tab2:
            st.subheader("Generate PDF Report")
            st.write("Create a comprehensive PDF report with executive summary, metrics, and visualizations.")
            
            # Report options
            include_charts = st.checkbox("Include Visualizations", value=True, key="pdf_charts")
            include_raw_data = st.checkbox("Include Raw Data Tables", value=False, key="pdf_raw")
            
            st.markdown("---")
            st.write("**Report Contents:**")
            st.write("✓ Executive Summary with key metrics")
            st.write("✓ Risk decomposition analysis")
            st.write("✓ Network statistics")
            if include_charts:
                st.write("✓ Key visualizations (charts and heatmaps)")
            if include_raw_data:
                st.write("✓ Complete data tables")
            
            if st.button("Generate PDF Report", type="primary", key="generate_pdf"):
                try:
                    from io import BytesIO
                    from datetime import datetime
                    
                    # Create PDF content as HTML (for simple PDF generation)
                    html_content = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; margin: 40px; }}
                            h1 {{ color: #1f77b4; }}
                            h2 {{ color: #333; border-bottom: 2px solid #1f77b4; padding-bottom: 5px; }}
                            .metric {{ background-color: #f0f2f6; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                            th {{ background-color: #1f77b4; color: white; padding: 10px; text-align: left; }}
                            td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
                            .timestamp {{ color: #666; font-size: 12px; }}
                        </style>
                    </head>
                    <body>
                        <h1>Matrix Metrics - Systemic Risk Analysis Report</h1>
                        <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        
                        <h2>Executive Summary</h2>
                        <div class="metric">
                            <p><strong>Systemic Risk Score (S):</strong> {st.session_state.systemic_risk_score:.4f}</p>
                            <p><strong>Normalized Risk Score (S̄):</strong> {st.session_state.normalized_score:.4f}</p>
                            <p><strong>Network Fragility (R):</strong> {st.session_state.fragility:.4f}</p>
                            <p><strong>Number of Institutions:</strong> {len(st.session_state.institution_df)}</p>
                        </div>
                        
                        <h2>Risk Decomposition Analysis</h2>
                        <table>
                            <tr>
                                <th>Institution</th>
                                <th>Compromise Score</th>
                                <th>Risk Contribution (Di)</th>
                                <th>Centrality</th>
                                <th>Criticality</th>
                            </tr>
                    """
                    
                    # Add institution data
                    for idx in range(len(st.session_state.institution_df)):
                        html_content += f"""
                            <tr>
                                <td>{st.session_state.institution_df.iloc[idx]['Name']}</td>
                                <td>{st.session_state.institution_df.iloc[idx]['CompromiseScore']:.4f}</td>
                                <td>{st.session_state.risk_decomposition[idx]:.4f}</td>
                                <td>{st.session_state.centrality[idx]:.4f}</td>
                                <td>{st.session_state.criticality[idx]:.4f}</td>
                            </tr>
                        """
                    
                    html_content += """
                        </table>
                        
                        <h2>Network Statistics</h2>
                        <div class="metric">
                    """
                    
                    # Add network statistics
                    if st.session_state.get('node_degrees') is not None:
                        avg_degree = float(st.session_state.node_degrees.mean())
                        html_content += f"<p><strong>Average Node Degree:</strong> {avg_degree:.2f}</p>"
                    
                    html_content += f"""
                            <p><strong>Network Density:</strong> {(st.session_state.adjacency_df.sum().sum() - len(st.session_state.adjacency_df)) / (len(st.session_state.adjacency_df) * (len(st.session_state.adjacency_df) - 1)):.4f}</p>
                        </div>
                        
                        <h2>Interpretation</h2>
                        <p>A normalized risk score (S̄) greater than 1.0 indicates that the network amplifies systemic risk beyond individual institution risks.</p>
                        <p>Higher fragility values suggest more concentrated connections, making the network more vulnerable to shocks.</p>
                        
                        <hr>
                        <p class="timestamp">Report generated by Matrix Metrics - Network-Based Systemic Risk Scoring</p>
                    </body>
                    </html>
                    """
                    
                    # For actual PDF, you'd use a library like reportlab or weasyprint
                    # For now, we'll provide the HTML version
                    st.success("PDF report content generated!")
                    
                    st.download_button(
                        label="📥 Download Report (HTML)",
                        data=html_content,
                        file_name=f"matrix_metrics_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html"
                    )
                    
                    st.info("💡 Tip: Open the HTML file in your browser and use 'Print to PDF' for a formatted PDF report.")
                    
                except Exception as e:
                    st.error(f"Error generating PDF report: {e}")
        
        # --- JSON Export Tab ---
        with export_tab3:
            st.subheader("Export Data as JSON")
            st.write("Download all metrics and data in JSON format for API integration or programmatic use.")
            
            import json
            
            # Prepare JSON data
            json_data = {
                'metadata': {
                    'export_timestamp': pd.Timestamp.now().isoformat(),
                    'num_institutions': len(st.session_state.institution_df),
                    'application': 'Matrix Metrics - Systemic Risk Scoring'
                },
                'summary_metrics': {
                    'systemic_risk_score': float(st.session_state.systemic_risk_score),
                    'normalized_score': float(st.session_state.normalized_score),
                    'fragility': float(st.session_state.fragility)
                },
                'institutions': st.session_state.institution_df.to_dict('records'),
                'risk_metrics': {
                    'risk_decomposition': st.session_state.risk_decomposition.tolist(),
                    'centrality': st.session_state.centrality.tolist(),
                    'criticality': st.session_state.criticality.tolist(),
                    'risk_increment': st.session_state.risk_increment.tolist() if st.session_state.get('risk_increment') is not None else []
                },
                'adjacency_matrix': st.session_state.adjacency_df.to_dict('split')
            }
            
            # Add cross-risk if available
            if st.session_state.get('cross_risk_matrix') is not None:
                json_data['cross_risk_matrix'] = st.session_state.cross_risk_matrix.to_dict('split')
            
            json_string = json.dumps(json_data, indent=2)
            
            st.download_button(
                label="📥 Download JSON Data",
                data=json_string,
                file_name=f"matrix_metrics_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            # Preview JSON structure
            with st.expander("Preview JSON Structure"):
                st.json(json_data)
        
        # --- Chart Exports Tab ---
        with export_tab4:
            st.subheader("Export Individual Charts")
            st.write("Download visualizations as high-resolution images.")
            
            st.write("##### Available Charts:")
            
            # Risk Decomposition Chart
            st.write("**1. Risk Decomposition Bar Chart**")
            decomp_df = pd.DataFrame({
                'Institution': st.session_state.institution_df['InstitutionID'],
                'Risk Contribution': st.session_state.risk_decomposition
            }).sort_values('Risk Contribution', ascending=False)
            
            fig_decomp = px.bar(
                decomp_df,
                x='Institution',
                y='Risk Contribution',
                title='Risk Decomposition by Institution',
                color='Risk Contribution',
                color_continuous_scale='Reds'
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.plotly_chart(fig_decomp, use_container_width=True)
            with col2:
                st.write("")
                st.write("")
                # Plotly charts can be downloaded directly from the interface
                st.info("📸 Use the camera icon in the chart toolbar to download as PNG")
            
            st.markdown("---")
            
            # Centrality Chart
            st.write("**2. Centrality Bar Chart**")
            centrality_df = pd.DataFrame({
                'Institution': st.session_state.institution_df['InstitutionID'],
                'Centrality': st.session_state.centrality
            }).sort_values('Centrality', ascending=False)
            
            fig_centrality = px.bar(
                centrality_df,
                x='Institution',
                y='Centrality',
                title='Network Centrality by Institution',
                color='Centrality',
                color_continuous_scale='Blues'
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.plotly_chart(fig_centrality, use_container_width=True)
            with col2:
                st.write("")
                st.write("")
                st.info("📸 Use the camera icon in the chart toolbar to download as PNG")
            
            st.markdown("---")
            
            # Network Graph
            st.write("**3. Network Visualization**")
            fig_network = create_network_graph(
                adjacency_df=st.session_state.adjacency_df,
                institution_names=st.session_state.institution_df['Name'],
                node_size_metric=pd.Series(st.session_state.risk_decomposition),
                node_color_metric=pd.Series(st.session_state.centrality),
                size_label="Risk Contribution",
                color_label="Centrality"
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.plotly_chart(fig_network, use_container_width=True)
            with col2:
                st.write("")
                st.write("")
                st.info("📸 Use the camera icon in the chart toolbar to download as PNG")
            
            st.markdown("---")
            
            # Cross-Risk Heatmap
            if st.session_state.get('cross_risk_matrix') is not None:
                st.write("**4. Cross-Risk Spillover Matrix**")
                cross_risk_df = st.session_state.cross_risk_matrix
                cross_risk_df_display = cross_risk_df.iloc[::-1]
                
                fig_heatmap = px.imshow(
                    cross_risk_df_display,
                    labels=dict(x="Influenced Institution (j)", y="Influencing Institution (i)", color="Spillover Effect"),
                    x=cross_risk_df.columns,
                    y=cross_risk_df_display.index,
                    color_continuous_scale='Reds',
                    aspect='auto'
                )
                fig_heatmap.update_layout(title="Cross-Risk Spillover Matrix")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                with col2:
                    st.write("")
                    st.write("")
                    st.info("📸 Use the camera icon in the chart toolbar to download as PNG")
            
            st.markdown("---")
            st.info("💡 **Tip:** All Plotly charts have a built-in toolbar (appears on hover) that allows you to:\n- Download as PNG\n- Zoom and pan\n- Reset axes\n- Toggle legend items")
    
    else:
        st.warning("Please calculate metrics on the 'Results Dashboard' page before exporting.")

# To run the app, use the command:
# streamlit run matrix_metrics_app/app.py
