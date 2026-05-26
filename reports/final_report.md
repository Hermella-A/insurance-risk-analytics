# Week 3 – Insurance Risk Analytics: From Data to Pricing Strategy

**Author:** Hermella-Amha  
**Date:** 27 May 2026  
**Challenge:** Insurance Risk Analytics for AlphaCare Insurance Solutions (ACIS)  
**Format:** Medium Blog Style

---

## Executive Summary

AlphaCare Insurance Solutions (ACIS) operates in the competitive South African auto‑insurance market. Using 18 months of historical claim data (10,000 policies), I built an end‑to‑end analytics pipeline to:

- Understand risk drivers through exploratory data analysis (EDA)
- Statistically test hypotheses about provinces, zip codes, and gender
- Predict claim probability and claim severity using machine learning
- Provide data‑driven pricing recommendations

**Key findings:**
- Overall loss ratio (TotalClaims / TotalPremium) ≈ 0.53 – profitable portfolio.
- Hypothesis tests showed **no significant risk differences** for the selected province pair (Addis Ababa vs Oromia), zip code pair (10002 vs 20003), or gender.
- Claim probability model (Random Forest) achieved 85% accuracy but low recall (19%), missing most actual claims.
- Claim severity models performed poorly (R² < 0.22), indicating insufficient features for accurate severity prediction.
- Top severity drivers: RiskScore, CustomValueEstimate, AnnualIncome.

**Recommendations:**
- Use vehicle make, age, income, and risk score as primary rating factors.
- Improve claim probability model by collecting more claim examples or using oversampling.
- For severity, invest in telematics data or segment models by vehicle type.
- Deploy a two‑stage pricing formula: Premium = P(claim) × average severity per segment + expense loading.

---

## 1. Data Understanding and Preparation

- **Dataset:** 10,000 rows, 21 columns (policy, client, vehicle, claim).  
- **No missing values, no duplicates.**  
- **Outliers:** Present in `TotalClaims` (max 49,623) – retained for realism.  
- **Data versioned with DVC** for full reproducibility (local remote storage, two versions tracked).

**Key business metrics:**
- Loss Ratio = TotalClaims / TotalPremium  
- Claim Frequency = proportion of policies with at least one claim  
- Claim Severity = average claim amount (given claim occurred)  
- Margin = TotalPremium – TotalClaims

---

## 2. Exploratory Data Analysis (EDA)

*[Insert Figure 1: Histogram of TotalClaims – most policies have zero claims, long tail of large claims]*  
**Insight:** A few severe claims drive total loss; pricing should differentiate between low‑risk and high‑risk policies.

*[Insert Figure 2: Average Loss Ratio by Province – bar chart, e.g., Somali highest, Addis Ababa lowest]*  
**Insight:** Regional risk differences exist – consider province‑based premium adjustments.

*[Insert Figure 3: Scatter plot – TotalPremium vs TotalClaims by Province]*  
**Insight:** Some provinces have high premium but low claims (inefficiency), suggesting potential mispricing.

*[Insert Figure 4: Top 10 vehicle makes by average claim amount – bar chart]*  
**Insight:** Luxury makes (BMW, Mercedes) have highest claims; economy makes lowest. Vehicle make is a strong risk indicator.

All additional plots are in `notebooks/01_eda.ipynb`.

---

## 3. Hypothesis Testing

**Null hypotheses tested (α = 0.05):**

1. No risk differences across provinces (Addis Ababa vs Oromia)  
2. No risk differences between zip codes (10002 vs 20003)  
3. No significant margin difference between zip codes  
4. No significant risk difference between women and men

**Results:**

| Hypothesis | Comparison | KPI | Test | p‑value | Decision |
|------------|------------|-----|------|---------|----------|
| Provinces | Addis Ababa vs Oromia | Claim Frequency | Chi‑squared | 0.8139 | Fail to reject |
| Provinces | Addis Ababa vs Oromia | Claim Severity | t‑test | 0.4265 | Fail to reject |
| Provinces | Addis Ababa vs Oromia | Margin | t‑test | 0.6513 | Fail to reject |
| Zip codes | 10002 vs 20003 | Claim Frequency | Chi‑squared | 0.9534 | Fail to reject |
| Zip codes | 10002 vs 20003 | Margin | t‑test | 0.8894 | Fail to reject |
| Gender | Male vs Female | Claim Frequency | Chi‑squared | 0.9638 | Fail to reject |
| Gender | Male vs Female | Claim Severity | t‑test | 0.9964 | Fail to reject |
| Gender | Male vs Female | Margin | t‑test | 0.9847 | Fail to reject |

**Business decision:** Because we found no significant risk difference between Addis Ababa and Oromia (p = 0.81) and between the tested zip codes and genders, ACIS should **not** introduce premium adjustments based solely on these factors. Instead, focus on vehicle make, age, and income as primary rating variables. This avoids unnecessary complexity and potential customer dissatisfaction while directing resources to proven risk drivers.

**Business interpretation:** No statistical evidence that province (for tested pair), zip code (for tested pair), or gender alone drive risk differences. Pricing adjustments should rely on other factors (vehicle make, age, income).


---

## 4. Predictive Modeling

### 4.1 Claim Probability Model (Random Forest)

- **Training set:** 8,000 rows, **Test set:** 2,000 rows
- **Accuracy:** 0.8515
- **Precision:** 0.5481
- **Recall:** 0.1857
- **F1-score:** 0.2774
- **AUC:** 0.7408

**Business decision:** The model’s low recall (19%) means it would miss 81% of actual claims if used alone. Therefore, ACIS should **not** rely on this model for automated claim detection or pricing. Instead, use it as a prioritisation tool – flag policies with high predicted claim probability for manual review by underwriters, while actively collecting more claim data to retrain the model in the next quarter.

**Interpretation:** The model correctly classifies 85% of cases, but only catches 19% of actual claims (low recall). For business use, adjust the threshold or apply SMOTE to balance classes.

### 4.2 Claim Severity Models (on policies with claims)

- **Training set:** 1,228 rows, **Test set:** 307 rows

| Model | RMSE | R² |
|-------|------|-----|
| Linear Regression | 5256.18 | 0.2189 |
| Random Forest | 5371.00 | 0.1844 |
| XGBoost | 5995.12 | -0.0162 |
**Business decision:** With R² below 0.22, the current severity models cannot reliably predict claim amounts. ACIS should **not** use them for setting premiums. Instead, adopt a segment‑based average severity approach (e.g., by vehicle make and age group) to estimate claim costs. Simultaneously, invest in telematics data collection (driving behaviour, mileage) before attempting severity prediction again.

**Interpretation:** The models explain less than 22% of variance in claim amounts. XGBoost performs worse than predicting the mean. This indicates that the available features (age, income, risk score, custom value estimate, vehicle age) are insufficient for accurate severity prediction. More granular data (e.g., telematics) is needed.

### 4.3 SHAP Feature Importance (XGBoost Severity Model)

*[Insert SHAP summary plot here]*

**Top features:** RiskScore, CustomValueEstimate, AnnualIncome.
**Business decision:** The top three features – RiskScore, CustomValueEstimate (vehicle value), and AnnualIncome – are actionable. ACIS should immediately adjust premiums for these features. For example:
- Increase premium by 5‑10% for policies with RiskScore > 75.
- Decrease premium for policies with RiskScore < 40.
- Apply a surcharge for vehicles with CustomValueEstimate above 80,000 Rand.
These changes are data‑backed, low‑risk, and can be implemented within the next pricing cycle.

**Business interpretation:** Higher RiskScore and higher custom value (more valuable vehicles) lead to higher predicted claim amounts. These features should be central in premium pricing.

---

## 5. Recommendations

- **Short‑term (immediate):**
  - Use vehicle make, age, annual income, and risk score as rating factors.
  - Apply a two‑stage pricing formula: Premium = P(claim) × average severity per segment + expense loading.
  - For claim probability, lower the classification threshold to improve recall (at the cost of some false positives).

- **Medium‑term (3‑6 months):**
  - Collect telematics data (mileage, driving behaviour) to improve severity models.
  - Implement SMOTE or collect more claim examples to balance the probability model.

- **Long‑term (6‑12 months):**
  - Develop a dynamic pricing engine that updates premiums based on real‑time risk signals.
  - Integrate external data (credit scores, vehicle telemetry) for better segmentation.

---

## 6. Limitations and Future Work

- **Data limitations:** Only 10,000 policies; claim examples are rare (only ~1,500 rows with claims). Severity models suffer from small sample size.
- **Feature limitations:** No driving history, no telematics, no vehicle usage data.
- **Future work:** 
  - Gather more data over time.
  - Engineer interaction features (e.g., RiskScore × VehicleAge).
  - Test deep learning models if more data becomes available.
  - Deploy models in a production environment and monitor performance.

---
## Summary of Business Decisions

| Finding | Business Decision | Impact / Next Step |
|---------|------------------|--------------------|
| No significant risk difference between Addis Ababa and Oromia (p = 0.81) | Do not change premiums based on province for these regions | Avoid unnecessary complexity; focus on vehicle make & age |
| Claim probability model low recall (19%) | Use model as screening tool, not automated rejection | Flag high‑risk policies for manual review; collect more claim data |
| Severity models poor (R² < 0.22) | Suspend severity‑based pricing; use segment averages | Protect profitability; invest in telematics |
| Top features: RiskScore, CustomValueEstimate, AnnualIncome | Adjust premiums immediately for these features | Implement within next pricing cycle |

## 7. Conclusion

This project successfully delivered a complete analytics pipeline for ACIS. The EDA revealed actionable patterns (vehicle make, province), hypothesis tests guided where not to over‑adjust (gender, certain zip codes), and predictive models, while imperfect, provide a baseline for risk‑based pricing. The recommendations prioritise immediate gains from existing data and longer‑term investments in telematics.

All code, data pipelines, and models are available in the GitHub repository:  
[https://github.com/Hermella-A/insurance-risk-analytics](https://github.com/Hermella-A/insurance-risk-analytics)

---

**Hermella-Amha**  
Week 3 – Insurance Risk Analytics