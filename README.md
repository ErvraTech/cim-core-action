# CIM-Core Action

Run CIM-Core (Chaos Intelligence Model) directly inside your GitHub workflows.  
CIM-Core is a domain-agnostic analysis engine designed to process complex datasets and provide adaptive insights such as anomaly detection, dynamic behaviour evaluation, and multi-scale analysis.

This action connects to a CIM-Core API endpoint (local or remote) and returns a structured analysis report.

---

## 🚀 Features

- Adaptive analysis for any dataset  
- Anomaly and drift detection  
- Multi-scale dynamic evaluation  
- Domain-agnostic: engineering, finance, science, R&D, automation  
- Simple API-based integration  
- Fully compatible with CI/CD workflows  

---

## 📦 Usage

Add the following step to your GitHub workflow:

```yaml
- name: Run CIM-Core Analysis
  uses: ErvraTech/cim-core-action@v1
  with:
    api_key: ${{ secrets.CIM_API_KEY }}
    data_path: data/input.csv
    config_file: cim-config.yaml
    endpoint: https://api.cim-core.com/analyze
