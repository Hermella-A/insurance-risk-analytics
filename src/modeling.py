# src/modeling.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def preprocess_data(df, target_sev='TotalClaims', target_prob='Claimed',
                    num_features=None, cat_features=None, drop_cols=None):
    """Preprocess data for modeling: encoding, scaling, split."""
    if drop_cols is None:
        drop_cols = ['CustomerID', 'TransactionDate', target_sev, target_prob]
    if num_features is None:
        num_features = ['Age', 'AnnualIncome', 'RiskScore', 'CustomValueEstimate', 'VehicleAge']
    if cat_features is None:
        cat_features = ['Gender', 'Province', 'VehicleType', 'CoverType', 'AutoMake']
    
    # Ensure only existing columns
    num_features = [c for c in num_features if c in df.columns]
    cat_features = [c for c in cat_features if c in df.columns]
    
    df_model = df.copy()
    
    # Label encode categoricals
    le_dict = {}
    for col in cat_features:
        le = LabelEncoder()
        df_model[col] = le.fit_transform(df_model[col].astype(str))
        le_dict[col] = le
    
    # Scale numericals
    scaler = StandardScaler()
    df_model[num_features] = scaler.fit_transform(df_model[num_features])
    
    X = df_model[num_features + cat_features]
    y_sev = df_model[target_sev]
    y_prob = df_model[target_prob].astype(int)
    
    return X, y_sev, y_prob, le_dict, scaler

def split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

def train_severity_model(X_train, y_train, model_type='xgboost'):
    if model_type == 'linear':
        model = LinearRegression()
    elif model_type == 'randomforest':
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    elif model_type == 'xgboost':
        model = XGBRegressor(n_estimators=100, random_state=42, eval_metric='rmse')
    else:
        raise ValueError("model_type must be 'linear', 'randomforest', or 'xgboost'")
    model.fit(X_train, y_train)
    return model

def train_probability_model(X_train, y_train, model_type='randomforest'):
    if model_type == 'randomforest':
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    elif model_type == 'xgboost':
        model = XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
    else:
        raise ValueError("model_type must be 'randomforest' or 'xgboost'")
    model.fit(X_train, y_train)
    return model

def evaluate_regression(model, X_test, y_test):
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    return {'RMSE': rmse, 'R2': r2}

def evaluate_classification(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    return {
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1': f1_score(y_test, y_pred),
        'AUC': roc_auc_score(y_test, y_proba)
    }