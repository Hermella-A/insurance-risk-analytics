# Insurance Risk Analytics
[![CI](https://github.com/Hermella-A/insurance-risk-analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/Hermella-A/insurance-risk-analytics/actions/workflows/ci.yml)

## Project Overview
Analysing 18 months of car insurance claim data (Feb 2014 – Aug 2015) for AlphaCare Insurance Solutions (ACIS) to optimise marketing, identify low‑risk targets, and build predictive models for claim severity and probability.

## Completed Tasks

### Task 1 – Exploratory Data Analysis (EDA)
- **Notebook:** `notebooks/01_eda.ipynb`
- **Key outputs:**
  - Data quality assessment (no missing values, no duplicates)
  - Univariate and bivariate visualisations
  - Geographic trends (loss ratio by province, vehicle type, gender)
  - Outlier detection, temporal trends
  - Identification of auto makes with highest/lowest claim amounts
- **Overall loss ratio:** 0.53

### Task 2 – Data Version Control (DVC)
- **Why DVC:** Regulatory and audit requirements demand reproducible data pipelines.
- **Setup:**
  - DVC initialised (`dvc init`)
  - Local remote storage: `C:\Users\Dataencoder\Desktop\dvc_remote`
  - Data tracked: `data/insurance_data.csv` (raw) and `data/insurance_data_cleaned.csv` (second version)
- **Reproducibility:** Any collaborator can run `dvc pull` to obtain the exact data.

### Task 3 – A/B Hypothesis Testing
- **Notebook:** `notebooks/02_hypothesis_testing.ipynb`
- **Tests performed:** Chi‑squared (claim frequency), t‑tests (severity, margin) for provinces, zip codes, gender.
- **Key result:** No statistically significant differences for tested pairs (p > 0.05). Pricing should not be adjusted solely based on these factors without considering other variables.

### Task 4 – Predictive Modeling
- **Notebook:** `notebooks/03_modeling.ipynb`
- **Claim probability model (Random Forest):** Accuracy 0.85, AUC 0.74, but low recall (0.19) – misses most claims.
- **Claim severity models (Linear Regression, Random Forest, XGBoost):** R² < 0.22, insufficient predictive power.
- **SHAP analysis:** Top features – RiskScore, CustomValueEstimate, AnnualIncome.
- **Recommendations:** Collect more claim examples, gather telematics data, use simplified pricing formula for now.

## Repository Structure
├── .github/workflows/ # CI pipeline
├── data/ # CSV files (tracked by DVC, ignored by Git)
├── notebooks/ # Jupyter notebooks for Tasks 1‑4
├── src/ # Reusable Python modules
├── reports/ # Final report placeholder
├── tests/ # Unit tests
├── .dvc/ # DVC internal files
├── .gitignore
├── requirements.txt
└── README.md


## Setup Instructions
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Pull data with DVC: `dvc pull`
6. Run Jupyter: `jupyter notebook`

## CI/CD
GitHub Actions (`.github/workflows/ci.yml`) runs `pip install -r requirements.txt` on every push to `main`.