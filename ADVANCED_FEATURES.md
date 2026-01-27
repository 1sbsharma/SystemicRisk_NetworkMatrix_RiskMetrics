# Advanced Features Implementation Guide

## Overview
This document describes the advanced features implemented in Matrix Metrics v2.0, as specified in PRD section 3.4.

## New Pages Added

### 1. Scenario Analysis (Page 4)
**Purpose:** Perform what-if analyses, test institution removal, and modify network connections.

#### 1.1 What-If Analysis Tab
- **Interactive Score Adjustment:** Modify individual institution compromise scores using sliders
- **Real-Time Comparison:** View original vs modified scores side-by-side
- **Impact Calculation:** Calculate and display changes to systemic risk score (S)
- **Visual Comparison:** Bar charts showing risk decomposition before and after modifications

**Use Cases:**
- Stress testing: Increase compromise scores to simulate financial distress
- Recovery scenarios: Decrease scores to model improved conditions
- Sensitivity analysis: Test how changes in specific institutions affect overall risk

#### 1.2 Institution Removal Simulation Tab
- **Multi-Institution Selection:** Remove one or more institutions from the network
- **Network Recalculation:** Automatically recalculates all metrics for the remaining network
- **Before/After Comparison:** 
  - Network size
  - Systemic Risk (S)
  - Fragility (R)
- **Visual Network Comparison:** Side-by-side network graphs showing original vs modified topology

**Use Cases:**
- Contagion testing: Assess impact of institution failure
- Regulatory analysis: Evaluate effects of removing systemically important institutions
- Network resilience: Test how the network adapts to node removal

#### 1.3 Network Modification Tab
- **Connection Editor:** Modify individual connection strengths in the adjacency matrix
- **Interactive Selection:** Choose from/to institutions and adjust weights with sliders
- **Matrix Visualization:** View current adjacency matrix with all modifications
- **Impact Analysis:** Calculate effects of network structure changes on systemic risk

**Use Cases:**
- Policy testing: Simulate effects of restricting interbank lending
- Network optimization: Test if reducing certain connections improves stability
- Scenario modeling: Create hypothetical network structures

#### 1.4 Scenario Saving
- **Save Current State:** Preserve any modifications made in the three tabs above
- **Naming System:** Give scenarios descriptive names for easy identification
- **Timestamp Tracking:** Automatic timestamp recording for each saved scenario
- **Scenario List:** View all saved scenarios with metadata

### 2. Compare Scenarios (Page 5)
**Purpose:** Load and compare up to 4 saved scenarios side-by-side.

#### 2.1 Scenario Selection
- **Multi-Select Interface:** Choose 2-4 scenarios to compare simultaneously
- **Flexible Comparison:** Works with any saved scenarios from the Scenario Analysis page

#### 2.2 Comparison Metrics
- Systemic Risk Score (S)
- Normalized Score (S̄)
- Fragility (R)
- Number of Institutions
- Average Compromise Score

#### 2.3 Visual Comparisons
- **Bar Charts:** Compare systemic risk across scenarios
- **Multi-Metric Visualization:** Grouped bar chart showing all key metrics
- **Detailed Breakdowns:** Expandable sections for each scenario's full details

#### 2.4 Scenario Management
- **Export Comparison:** Download comparison results as CSV
- **Delete Scenarios:** Remove individual scenarios
- **Clear All:** Reset all saved scenarios
- **Scenario Count:** Track how many scenarios are stored

**Use Cases:**
- Policy evaluation: Compare multiple regulatory approaches
- Best-case/worst-case analysis: Examine extreme scenarios
- Strategic planning: Evaluate different strategic options

### 3. Enhanced Export Results (Page 6)

#### 3.1 Excel Export (Enhanced)
- Multi-sheet workbook with all metrics
- Timestamped filenames
- Comprehensive data tables
- Summary statistics

#### 3.2 PDF Report (New)
- Executive summary with key metrics
- Detailed risk decomposition tables
- Network statistics
- Professional HTML format (can be printed to PDF)
- Optional chart inclusion
- Optional raw data tables

**Report Sections:**
1. Executive Summary
2. Risk Decomposition Analysis
3. Network Statistics
4. Interpretation Guidelines

#### 3.3 JSON Data Export (New)
- **Structured Format:** Complete metrics in JSON for API integration
- **Metadata Included:** Export timestamp, application info
- **Nested Structure:**
  - Summary metrics
  - Institution details
  - Risk metrics arrays
  - Adjacency matrix
  - Cross-risk matrix (if calculated)
- **Preview Available:** View JSON structure before download

**Use Cases:**
- API Integration: Feed data into other systems
- Programmatic Analysis: Process data with custom scripts
- Data Archival: Store results in structured format

#### 3.4 Chart Exports (Enhanced)
- **Individual Chart Downloads:** Export each visualization separately
- **High-Resolution PNG:** Use built-in Plotly toolbar
- **Interactive Toolbar:** Zoom, pan, reset, download
- **Available Charts:**
  1. Risk Decomposition Bar Chart
  2. Centrality Bar Chart
  3. Network Visualization
  4. Cross-Risk Spillover Matrix

## Session State Management

### New Session State Variables
```python
st.session_state.saved_scenarios = {}  # Stores all saved scenarios
st.session_state.current_scenario_name = None  # Current scenario identifier
st.session_state.scenario_modifications = {
    'modified_compromise': None,  # Modified compromise scores
    'modified_adjacency': None,   # Modified adjacency matrix
    'removed_institutions': []    # List of removed institution names
}
```

## Navigation Updates
Previous: Data Upload → Network Construction → Results Dashboard → Export Results

**New Navigation:**
1. Data Upload
2. Network Construction
3. Results Dashboard
4. **Scenario Analysis** (NEW)
5. **Compare Scenarios** (NEW)
6. Export Results (Enhanced)

## Technical Implementation Details

### Data Flow
```
1. Load Base Data (Pages 1-2)
   ↓
2. Calculate Base Metrics (Page 3)
   ↓
3. Create Scenarios (Page 4)
   → Modify scores/network/institutions
   → Save scenario with modifications
   ↓
4. Compare Scenarios (Page 5)
   → Load multiple saved scenarios
   → Calculate metrics for each
   → Display side-by-side comparison
   ↓
5. Export Results (Page 6)
   → Excel, PDF, JSON, or Charts
```

### Scenario Data Structure
```python
{
    'scenario_name': {
        'institution_df': DataFrame,      # Original institution data
        'adjacency_df': DataFrame,        # Original adjacency matrix
        'modifications': {
            'modified_compromise': Series,  # Modified scores (or None)
            'modified_adjacency': DataFrame,  # Modified matrix (or None)
            'removed_institutions': List   # Removed institution names
        },
        'timestamp': Timestamp            # When scenario was saved
    }
}
```

## Usage Workflow Examples

### Example 1: Stress Test Analysis
1. Load sample data
2. Calculate baseline metrics
3. Go to Scenario Analysis → What-If Analysis
4. Increase compromise scores for top 3 institutions by 50%
5. Calculate impact
6. Save as "High Stress Scenario"
7. Go to Compare Scenarios
8. Compare baseline vs stress scenario
9. Export comparison as CSV

### Example 2: Contagion Assessment
1. Load network data
2. Go to Scenario Analysis → Institution Removal
3. Remove the most central institution
4. Simulate removal
5. Save as "Bank A Failure"
6. Repeat for other critical institutions
7. Go to Compare Scenarios
8. Compare all failure scenarios
9. Export PDF report

### Example 3: Network Optimization
1. Load data and calculate metrics
2. Go to Scenario Analysis → Network Modification
3. Reduce connections between highly connected nodes
4. Calculate impact
5. Save as "Reduced Interconnection"
6. Test multiple connection patterns
7. Compare all network configurations
8. Export JSON for further analysis

## Key Features Summary

✅ **Scenario Analysis**
- Interactive what-if testing
- Institution removal simulation
- Network connection modification
- Real-time metric recalculation
- Scenario saving with timestamps

✅ **Comparative Analysis**
- Multi-scenario comparison (up to 4)
- Side-by-side visualizations
- Metric comparison tables
- Scenario management (delete/clear)
- CSV export of comparisons

✅ **Enhanced Exports**
- Excel workbooks (timestamped)
- PDF/HTML reports (professional format)
- JSON data (API-ready)
- Individual chart exports (high-res PNG)
- Built-in Plotly download tools

## Future Enhancements (Not Implemented)
- Monte Carlo simulation capabilities
- Time-series scenario analysis
- Automated stress testing templates
- Machine learning-based risk prediction
- Real-time data integration
- Multi-user collaboration features

## Notes
- All calculations use the existing `SystemicRiskCalculator` class
- No changes to core calculation logic
- Backward compatible with existing data
- Scenarios persist only in session state (not saved to disk)
- For production use, consider adding database storage for scenarios
