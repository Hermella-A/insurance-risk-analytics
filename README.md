# Insurance Risk Analytics

## Project Overview
Analysing 18 months of car insurance data to optimise marketing, identify low‑risk targets, and build predictive models for claim severity and probability.

## Tasks Completed

### Task 1 – Exploratory Data Analysis (EDA)
- **Notebook:** `notebooks/01_eda.ipynb`
- **Key analyses:**
  - Data quality assessment (no missing values, no duplicates)
  - Univariate and bivariate visualisations
  - Geographic trends (loss ratio by province, vehicle type, gender)
  - Outlier detection (box plots for key numerical features)
  - Temporal trends (monthly claims and premiums)
- **Key findings:**
  - Overall portfolio loss ratio: [calculated value – you can fill later]
  - Provinces/vehicle types with highest loss ratio
  - Top auto makes with highest average claim amounts

### Task 2 – Data Version Control (DVC)
- **Goal:** Reproducible data pipeline for auditing and regulatory compliance.
- **Setup:**
  - DVC initialised (`dvc init`)
  - Local remote storage: `C:\Users\Dataencoder\Desktop\dvc_remote`
  - Raw data tracked: `data/insurance_data.csv` (via `dvc add`)
  - Cleaned data version: `data/insurance_data_cleaned.csv` (also tracked)
- **Reproducing the data:**
  ```bash
  pip install dvc
  dvc pull