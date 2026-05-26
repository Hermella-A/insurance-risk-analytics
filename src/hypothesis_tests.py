import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind

def test_claim_frequency(df, group_col, group_a, group_b):
    """Chi-squared test for claim frequency between two groups."""
    subset = df[df[group_col].isin([group_a, group_b])]
    contingency = pd.crosstab(subset[group_col], subset['Claimed'])
    chi2, p, dof, expected = chi2_contingency(contingency)
    return chi2, p

def test_claim_severity(df, group_col, group_a, group_b):
    """t-test for claim severity (TotalClaims > 0) between two groups."""
    subset = df[(df[group_col].isin([group_a, group_b])) & (df['TotalClaims'] > 0)]
    if len(subset) < 2:
        return None, None
    t_stat, p = ttest_ind(subset[subset[group_col]==group_a]['TotalClaims'],
                          subset[subset[group_col]==group_b]['TotalClaims'],
                          equal_var=False)
    return t_stat, p

def test_margin(df, group_col, group_a, group_b):
    """t-test for margin (TotalPremium - TotalClaims) between two groups."""
    subset = df[df[group_col].isin([group_a, group_b])].copy()
    subset['Margin'] = subset['TotalPremium'] - subset['TotalClaims']
    t_stat, p = ttest_ind(subset[subset[group_col]==group_a]['Margin'],
                          subset[subset[group_col]==group_b]['Margin'],
                          equal_var=False)
    return t_stat, p