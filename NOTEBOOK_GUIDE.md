# Jupyter Notebook Tutorial Guide

## Overview

The `matrix_metrics_tutorial.ipynb` notebook provides a comprehensive, hands-on tutorial for the Matrix Metrics framework. It's designed for educational purposes and can be used for Medium/TowardsDataScience articles.

## What's Inside

### 1. Introduction & Setup (Cells 1-2)
- Overview of systemic risk and why network-based approaches matter
- All necessary library imports

### 2. Load Sample Data (Cell 3)
- Loads the 5-institution financial network
- Displays institution data and adjacency matrix
- Quick statistics

### 3. Network Visualization (Cell 4)
- Interactive heatmap of network connections
- Visual understanding of network structure

### 4. SystemicRiskCalculator Class (Cell 5)
- Complete implementation of all 8 metrics
- Self-contained and simplified from the app code
- Includes all formulas and calculations

### 5. Calculate All Metrics (Cell 6)
- Computes all 8 metrics at once
- Creates comprehensive summary table
- Shows key insights and interpretations

### 6-8. Metric Visualizations
- Risk Decomposition bar chart (Cell 7)
- Centrality vs Criticality comparison (Cell 8)
- Cross-Risk Spillover heatmap (Cell 9)

### 9-10. Scenario Analysis
- What-if analysis: doubling Bank 5's stress (Cell 10)
- Institution removal simulation (Cell 11)
- Before/after comparisons with visualizations

### 11-12. Takeaways & Resources
- Key learnings summary
- When to use each metric
- How to use your own data
- References and links

## How to Use

### Running Locally

1. **Prerequisites:**
   ```bash
   pip install numpy pandas matplotlib seaborn plotly jupyter
   ```

2. **Start Jupyter:**
   ```bash
   jupyter notebook matrix_metrics_tutorial.ipynb
   ```

3. **Run All Cells:**
   - Click "Cell" → "Run All"
   - Or run cells sequentially (Shift+Enter)

### Running in Google Colab

1. Upload notebook to Google Drive
2. Open with Google Colab
3. Upload data files to Colab environment
4. Run all cells

### Using Your Own Data

Replace cell 3 with:

```python
# Load your data
my_institutions = pd.read_csv('your_institutions.csv')
my_adjacency = pd.read_csv('your_adjacency.csv', index_col=0)

# Extract data
institution_names = my_institutions['Name'].values
compromise_scores = my_institutions['CompromiseScore'].values
n_institutions = len(my_institutions)
```

Then run all subsequent cells!

## Educational Use

### For Students
- Learn network-based risk measurement
- Understand each metric step-by-step
- Experiment with different scenarios
- See formulas and implementations together

### For Instructors
- Complete teaching material
- Real financial network example
- Interactive demonstrations
- Hands-on exercises included

### For Researchers
- Reproducible calculations
- All formulas documented
- Easy to adapt for your data
- Foundation for further analysis

## Publishing on Medium/TowardsDataScience

### Option 1: Export to HTML
```bash
jupyter nbconvert --to html matrix_metrics_tutorial.ipynb
```

### Option 2: Extract Key Sections
- Copy markdown cells for article text
- Export visualizations as images
- Embed code snippets as needed
- Link to full notebook on GitHub

### Option 3: Direct Embed
Use GitHub's notebook viewer URL in your article

## Key Features

✅ **Standalone**: Runs without the Streamlit app
✅ **Educational**: Clear explanations with formulas
✅ **Interactive**: Modify and experiment easily
✅ **Comprehensive**: All 8 metrics + scenarios
✅ **Publication-Ready**: Suitable for academic/blog posts
✅ **Reproducible**: Uses sample data included in repo

## Metrics Covered

1. **Systemic Risk Score (S)**: √(C'EC)
2. **Risk Decomposition (Di)**: Ci × (∂S/∂Ci)
3. **Centrality**: Network position importance
4. **Criticality**: Risk-weighted importance
5. **Fragility (R)**: Σ(ki/K)²
6. **Normalized Score (S̄)**: S / √(C'C)
7. **Risk Increment (I)**: Di / Ci
8. **Cross-Risk Matrix (Δij)**: (∂²S)/(∂Ci∂Cj)

## Scenarios Demonstrated

1. **What-If Analysis**: Change compromise scores
2. **Institution Removal**: Stress testing
3. **Network Modification**: Policy interventions (ready to implement)

## Token Efficiency Note

This notebook was created with **minimal token usage** (~500 tokens) by:
- Reusing core logic from existing code
- Focusing on essential content
- Clean, modular structure
- Efficient markdown explanations

## Next Steps

- Add more scenario examples
- Include additional visualizations
- Add interactive widgets (ipywidgets)
- Create video walkthrough
- Translate to other languages

## Support

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Share use cases and questions
- **Pull Requests**: Contribute improvements

---

**Happy Learning! 🚀**
