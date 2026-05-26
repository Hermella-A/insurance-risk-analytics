# Insurance Risk Analytics – Task 4: Predictive Modeling

## Overview
This branch contains the modeling work for claim severity and claim probability, as part of Week 3 challenge.

## Files
- `notebooks/03_modeling.ipynb` – complete modeling notebook (data prep, regression, classification, SHAP)
- `src/modeling.py` – reusable modeling functions

## Modeling Results

### Claim Probability (Random Forest)
- Accuracy: 0.8515
- Precision: 0.5481
- Recall: 0.1857
- F1: 0.2774
- AUC: 0.7408

### Claim Severity (on claims > 0)
| Model | RMSE | R² |
|-------|------|-----|
| Linear Regression | 5256.18 | 0.2189 |
| Random Forest | 5371.00 | 0.1844 |
| XGBoost | 5995.12 | -0.0162 |

### SHAP Feature Importance (XGBoost)
Top features: RiskScore, CustomValueEstimate, AnnualIncome.

## Business Recommendations
- Use probability model as screening tool; improve recall with more data.
- Current severity models are weak – need additional features (e.g., telematics).
- Pricing formula: Premium = P(claim) × average severity + expense loading.

## Setup
Same as main branch (see main README after merge).

## Next Step
Merge this branch into `main` to combine all tasks.