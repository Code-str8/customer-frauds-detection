import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator, TransformerMixin

class LogTransformer(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return np.log1p(X)
    
    def get_feature_names_out(self, input_features=None):
        return input_features

def clean_and_feature_engineer(df):
    processed_df = df.copy()

    # --- Data Cleaning ---
    if 'target' in processed_df.columns:
        processed_df['target'] = processed_df['target'].astype(int)
    if 'counter_statue' in processed_df.columns:
        processed_df['counter_statue'] = (
                   pd.to_numeric(processed_df['counter_statue'], errors='coerce')
                         .fillna(0)
                         .astype(int)
        )

    # Convert to datetime
    date_columns = ['creation_date', 'invoice_date']
    date_format = '%d/%m/%Y'

    for col in date_columns:
        if col in processed_df.columns:
            processed_df[col] = pd.to_datetime(processed_df[col], format=date_format)

    # Date-based features
    if 'creation_date' in processed_df.columns:
        processed_df['creation_year'] = processed_df['creation_date'].dt.year
        processed_df['creation_month'] = processed_df['creation_date'].dt.month
        processed_df['account_age_days'] = (pd.Timestamp.now() - processed_df['creation_date']).dt.days

    if 'invoice_date' in processed_df.columns:
        processed_df['invoice_year'] = processed_df['invoice_date'].dt.year
        processed_df['invoice_month'] = processed_df['invoice_date'].dt.month
        processed_df['invoice_quarter'] = processed_df['invoice_date'].dt.quarter

    # Columns to drop
    cols_to_drop = [
        'creation_date',
        'client_id',
        'months_number',
        'invoice_date',
        'reading_remarque'
    ]
    processed_df = processed_df.drop(
        columns=[col for col in cols_to_drop if col in processed_df.columns],
        errors='ignore'
    )

    # Column renaming
    column_rename_map = {
        'disrict': 'district',
        'consommation_level_1': 'consumption_level_1',
        'consommation_level_2': 'consumption_level_2',
        'consommation_level_3': 'consumption_level_3',
        'consommation_level_4': 'consumption_level_4'
    }
    processed_df = processed_df.rename(columns={
        k: v for k, v in column_rename_map.items()
        if k in processed_df.columns
    })

    return processed_df

def select_features(X, y=None, k=10):
    # If y is None (prediction time), return X as is
    if y is None:
        return X
        
    # a copy 
    X = X.copy()
    
    # Encode categorical variables if present
    if 'counter_type' in X.columns:
        le = LabelEncoder()
        X['counter_type'] = le.fit_transform(X['counter_type'])
    
    # smaller sample for feature selection
    sample_size = min(500000, len(X))
    X_sample = X.sample(sample_size, random_state=42)
    y_sample = y.sample(sample_size, random_state=42) if y is not None else None
    
    # Mutual Information
    mi_selector = SelectKBest(score_func=mutual_info_classif, k=k)
    mi_selector.fit(X_sample, y_sample)
    mi_scores = pd.Series(mi_selector.scores_, index=X.columns)
    
    # Random Forest Importance
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_sample, y_sample)
    rf_scores = pd.Series(rf.feature_importances_, index=X.columns)
    
    # Combine scores
    feature_scores = pd.DataFrame({
        'MI_Score': mi_scores,
        'RF_Score': rf_scores
    })
    
    # Select top features
    selected_features = feature_scores.mean(axis=1).sort_values(ascending=False)[:k].index
    
    return X[selected_features] 