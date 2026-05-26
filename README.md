# Task 3 – A/B Hypothesis Testing

## Objective
Statistically validate risk drivers (provinces, zip codes, gender) using claim frequency, claim severity, and margin as KPIs.

## Hypotheses Tested

1. **Provinces** – Addis Ababa vs Oromia  
   - No difference in claim frequency, severity, or margin.
2. **Zip codes** – 10002 vs 20003  
   - No difference in claim frequency or margin.
3. **Gender** – Male vs Female  
   - No difference in claim frequency, severity, or margin.

## Methodology

- **Claim frequency:** Chi‑squared test (categorical).  
- **Claim severity:** t‑test (only on policies with claims > 0).  
- **Margin (TotalPremium – TotalClaims):** t‑test.

All tests use α = 0.05.

## Results Summary

| Hypothesis | Comparison | KPI | p‑value | Decision |
|------------|------------|-----|---------|----------|
| Provinces | Addis Ababa vs Oromia | Claim Frequency | 0.8139 | Fail to reject H₀ |
| Provinces | Addis Ababa vs Oromia | Claim Severity | 0.4265 | Fail to reject H₀ |
| Provinces | Addis Ababa vs Oromia | Margin | 0.6513 | Fail to reject H₀ |
| Zip codes | 10002 vs 20003 | Claim Frequency | 0.9534 | Fail to reject H₀ |
| Zip codes | 10002 vs 20003 | Margin | 0.8894 | Fail to reject H₀ |
| Gender | Male vs Female | Claim Frequency | 0.9638 | Fail to reject H₀ |
| Gender | Male vs Female | Claim Severity | 0.9964 | Fail to reject H₀ |
| Gender | Male vs Female | Margin | 0.9847 | Fail to reject H₀ |

All p‑values > 0.05 → no statistical evidence for risk differences in the selected comparisons.

## Business Recommendation

- Do **not** adjust premiums solely based on province (Addis Ababa vs Oromia), zip code (10002 vs 20003), or gender based on this analysis.  
- Explore additional province pairs or use multivariate modeling to control for confounding variables.

## Files

- `notebooks/02_hypothesis_testing.ipynb` – complete analysis.  
- `src/hypothesis_tests.py` – reusable test functions.

## How to Run

1. Ensure the data is available (via DVC: `dvc pull`).  
2. Run the notebook cells in order.  
3. The results table and interpretations are embedded.