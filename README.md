# Matrix Metrics: Network-Based Systemic Risk Scoring

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A comprehensive framework for measuring and analyzing systemic risk in financial networks using network-based metrics and interactive visualizations. This project is inspired by the network-based systemic risk framework proposed in  Das (2016), *Matrix metrics: Network-based systemic risk scoring*,  The Journal of Alternative Investments. https://doi.org/10.3905/jai.2016.18.4.033

---

## 📚 Overview

**Matrix Metrics** is an interactive web application that implements a network-based approach to systemic risk measurement. This tool helps you:

- 🔍 **Identify** systemically important institutions
- 📊 **Quantify** interconnected risks across networks
- 🎯 **Simulate** stress scenarios and policy interventions
- 📈 **Visualize** risk propagation patterns

### Theoretical Foundation

This application implements a network-based approach to systemic risk measurement, inspired by the work of Das (2016). Traditional risk metrics focus on individual institutions in isolation. However, the 2008 financial crisis demonstrated that interconnectedness amplifies risk. A single institution's failure can cascade through the network, causing systemic collapse.

**Matrix Metrics addresses this by:**
1. Explicitly modeling network connections
2. Measuring risk contribution of each institution
3. Quantifying spillover effects between institutions
4. Identifying structural vulnerabilities

---

## 👥 Who Might Find This Useful

- **Researchers and practitioners** interested in network-based measures of concentration and contagion risk
- **Credit risk and portfolio analytics teams** exploring connected-clients effects beyond single-name exposure limits
- **Regulators and quants** experimenting with explainable systemic or concentration risk metrics
- **Students and learners** studying financial networks, contagion, and risk decomposition methods

---

## ✨ Features

### Core Capabilities
- ✅ **8 Comprehensive Risk Metrics**: S, Di, Centrality, Criticality, R, Δij, I, S̄
- ✅ **Interactive Network Visualization**: Dynamic graph with customizable node metrics
- ✅ **Scenario Analysis Tools**:
  - Sensitivity to Compromise Scores (what-if analysis)
  - Institution Removal Simulation (stress testing)
  - Network Modification (policy intervention testing)
- ✅ **Comparative Analysis**: Save and compare multiple scenarios side-by-side
- ✅ **Multiple Export Formats**: Excel, JSON, PDF reports, and chart exports
- ✅ **Built-in Documentation**: Comprehensive help system with formulas and interpretations

### Self-Documenting Interface
- Contextual tooltips throughout the application
- Expandable help sections for all metrics
- Step-by-step quick start guide
- Complete metrics reference with formulas

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/1sbsharma/matrix-metrics.git
   cd matrix-metrics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run matrix_metrics_app/app.py
   ```

4. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

---

## 📖 Quick Start

### Using Sample Data

1. Navigate to the **Data Upload** page
2. Click **"Load Sample Data"** button
3. The app loads a 5-institution financial network
4. Click **"Validate Data"** to verify (optional)
5. Go to **Results Dashboard** → Click **"Calculate All Metrics"**
6. Explore the visualizations and metrics!

### Using Your Own Data

You need two files:

#### 1. Institution Data (CSV/Excel)
Required columns:
- `InstitutionID`: Unique identifier (integer or string)
- `Name`: Human-readable institution name
- `CompromiseScore`: Stress/vulnerability measure (non-negative)

**Example:**
```csv
InstitutionID,Name,CompromiseScore
1,Bank Alpha,2.5
2,Bank Beta,1.8
3,Bank Gamma,3.2
```

#### 2. Adjacency Matrix (CSV/Excel)
Square matrix representing network connections:
- Rows and columns represent institutions (same order)
- Values represent connection strengths (e.g., exposures, lending amounts)
- Element (i,j) = connection from institution i to institution j

**Example:**
```csv
,1,2,3
1,0,0.5,0.3
2,0.5,0,0.7
3,0.3,0.7,0
```

---

## 📊 Metrics Reference

### Systemic Risk Score (S)
**Formula:** `S = √(C'EC)`

The aggregate measure of total systemic risk in the network. Combines individual institution stress (compromise scores) with network structure to produce an overall risk score.

### Normalized Risk Score (S̄)
**Formula:** `S̄ = S / √(C'C)`

Isolates the network effect on systemic risk. Values > 1 indicate network amplification; < 1 indicate network dampening.

### Risk Decomposition (Di)
**Formula:** `Di = Ci × (∂S/∂Ci)`

Breaks down total systemic risk into individual institution contributions. The sum of all Di equals S (perfect decomposition property).

### Centrality
Measures an institution's importance in the network structure based on connections (node degree). Highly central institutions act as conduits for risk transmission.

### Criticality
Risk-weighted measure combining centrality with compromise scores. Identifies institutions that are both vulnerable and interconnected.

### Fragility (R)
**Formula:** `R = Σ(ki/K)²`

Measures network concentration. Higher fragility means risk is concentrated in fewer institutions, making the network vulnerable to targeted shocks.

### Cross-Risk Matrix (Δij)
**Formula:** `Δij = (∂²S)/(∂Ci∂Cj)`

Quantifies spillover effects between institutions. Shows how stress in one institution affects another's risk contribution.

### Risk Increment (I)
**Formula:** `Ii = Di / Ci`

The amplification factor - how much systemic impact an institution has per unit of its own stress. Identifies institutions whose stress has outsized systemic consequences.

---

## 🎯 Application Workflow

1. **About** (Page 1)
   - Learn about the framework and metrics
   - Review data requirements
   - Access complete documentation

2. **Data Upload** (Page 2)
   - Load sample dataset OR upload your own
   - Validate data format and requirements

3. **Network Construction** (Page 3)
   - Review network structure
   - Visualize connections
   - Examine network statistics

4. **Results Dashboard** (Page 4)
   - Calculate all systemic risk metrics
   - View interactive visualizations
   - Analyze risk decomposition and spillovers

5. **Scenario Analysis** (Page 5)
   - **Sensitivity to Compromise Scores**: Test what-if scenarios
   - **Institution Removal**: Simulate stress testing
   - **Network Modification**: Test policy interventions

6. **Compare Scenarios** (Page 6)
   - Save multiple scenario results
   - Compare metrics side-by-side
   - Track changes across scenarios

7. **Export Results** (Page 7)
   - Download data as Excel/JSON
   - Generate PDF reports
   - Export charts and visualizations

---

## 📁 Project Structure

```
matrix_metrics_app/
├── app.py                      # Main Streamlit application
├── src/
│   ├── core/
│   │   ├── metrics.py         # Core metric calculations
│   │   ├── network_utils.py   # Network analysis utilities
│   │   └── systemic_risk.py   # SystemicRiskCalculator class
│   ├── data/
│   │   ├── loader.py          # Data loading utilities
│   │   └── preprocessor.py    # Data preprocessing
│   ├── utils/
│   │   ├── exporters.py       # Export functionality
│   │   └── validators.py      # Data validation
│   └── visualization/
│       ├── metrics_viz.py     # Metric visualizations
│       └── network_viz.py     # Network graph visualization
├── data/
│   └── sample_data/
│       ├── das_2016_institutions.csv
│       └── das_2016_adjacency.csv
└── tests/
    └── test_systemic_risk.py  # Unit tests
```

---

## 📚 Documentation

- **In-App Documentation**: Complete help system available in the About page
- **[DOCUMENTATION_GUIDE.md](DOCUMENTATION_GUIDE.md)**: Details on the help system and user interface
- **[ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)**: Scenario analysis and comparative features
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)**: Technical implementation details

---

## 💡 Example Use Cases

### 1. Systemic Risk Monitoring
Track how systemic risk evolves over time by uploading data from different time periods and comparing the S metric.

### 2. Stress Testing
Use the Institution Removal simulation to identify Systemically Important Financial Institutions (SIFIs) - institutions whose removal would significantly impact the network.

### 3. Network Vulnerability Analysis
Examine the Fragility (R) metric and Cross-Risk Matrix to understand concentration risk and identify contagion pathways.

### 4. Policy Evaluation
Test the impact of regulatory interventions (e.g., exposure limits) using the Network Modification tool to adjust connection strengths.

### 5. Research and Education
Study contagion mechanisms, risk decomposition methods, and network effects in financial systems using the interactive visualizations and comprehensive metrics.

---

## 🔧 Technical Details

### Built With

- **[Streamlit](https://streamlit.io/)**: Interactive web application framework
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation and analysis
- **[NumPy](https://numpy.org/)**: Numerical computing
- **[Plotly](https://plotly.com/)**: Interactive visualizations
- **[NetworkX](https://networkx.org/)**: Network analysis (if used)

### Requirements

See `requirements.txt` for complete list of dependencies.

---

## 📄 Citation

If you use Matrix Metrics in your research, please cite:

```bibtex
@software{matrix_metrics,
  title = {Matrix Metrics: Network-Based Systemic Risk Scoring},
  author = {[Shashi B Sharma]},
  year = {2026},
  url = {https://github.com/1sbsharma/matrix-metrics}
}
```

**Theoretical Foundation:**
```bibtex
@article{das2016,
  title = {Matrix Metrics: Network-Based Systemic Risk Scoring},
  author = {Das, S. R.},
  year = {2016}
}
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas for Contribution

- Additional metrics and risk measures
- Enhanced visualizations
- Performance optimizations
- Additional export formats
- Documentation improvements
- Bug fixes and testing

---

## 🙏 Acknowledgments

- Inspired by the work of **Das (2016)** on systemic risk in financial networks
- Built with amazing open-source tools: Streamlit, Pandas, NumPy, and Plotly
- Sample data based on financial network research methodologies

---

## 📞 Contact

- **GitHub**: [@1sbsharma](https://github.com/1sbsharma)
- **Issues**: [Report bugs or request features](https://github.com/1sbsharma/matrix-metrics/issues)

---

## 🔗 Related Resources

- **Matrix Metrics Paper**: [Das (2016), *Matrix metrics: Network-based systemic risk scoring*, The Journal of Alternative Investments.  
https://doi.org/10.3905/jai.2016.18.4.033]


---

## ⚠️ Disclaimer

This tool is for educational and research purposes. It should not be used as the sole basis for financial decisions or regulatory actions without proper validation and professional oversight.

---

**Made with ❤️ for the systemic risk research community**
