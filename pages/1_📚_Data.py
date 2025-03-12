import streamlit as st
import pandas as pd
import plotly.express as px
from auth_util.auth import login_form, is_authenticated

st.set_page_config(
    page_icon="📚",
    page_title="Data",
    layout="wide"
)

@st.cache(allow_output_mutation=True)  # Use older cache decorator
def load_data():
    try:
        data = pd.read_csv("datasets/fraud_detection.csv")
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def data_page():
    login_form()
    if is_authenticated():
        # Replace direct data loading with cached function
        data = load_data()
        if data is None:
            return
            
        # Show sample of data instead of full dataset
        st.write("Sample of the dataset (first 1000 rows):")
        st.dataframe(data.head(1000))

        st.title("Explore Fraud Detection Data ⭐")
        st.write(
            """
            Gain valuable insights into our fraud detection dataset and understand the factors that contribute to identifying fraudulent activities.
            """
        )

        # Define feature categories
        numeric_features = [
            "counter_number", "account_age_days", "new_index", 
            "old_index", "consumption_level_1", "counter_coefficient"
        ]
        categorical_features = [
            "client_catg", "invoice_year", "creation_year", "creation_month"
        ]

        # Feature selection radio
        selected_feature_type = st.radio(
            "Select Feature Type:",
            options=["Numerical", "Categorical"]
        )

        if selected_feature_type == "Numerical":
            selected_feature = st.selectbox(
                "Select a Numeric Feature",
                options=numeric_features
            )
            st.write(f"Exploring Numerical Feature: {selected_feature}")
            
            # Display distribution plot
            fig = px.histogram(
                data, 
                x=selected_feature,
                title=f"Distribution of {selected_feature}"
            )
            st.plotly_chart(fig)
            
            # Display basic statistics
            st.write("Basic Statistics:")
            st.write(data[selected_feature].describe())

        elif selected_feature_type == "Categorical":
            selected_feature = st.selectbox(
                "Select a Categorical Feature",
                options=categorical_features
            )
            st.write(f"Exploring Categorical Feature: {selected_feature}")
            
            # Display value counts
            fig = px.bar(
                data[selected_feature].value_counts().reset_index(),
                x='index',
                y=selected_feature,
                title=f"Distribution of {selected_feature}"
            )
            st.plotly_chart(fig)

        # Feature explanations
        st.header("Feature Explanations")
        st.write(
            """
            Click on a feature name to view its description and potential impact on fraud detection:
            """
        )

        # Feature descriptions with emojis
        column_descriptions = {
            "counter_number": "🔢 Unique identifier for the electricity meter.",
            "account_age_days": "📅 Number of days since the account was created.",
            "new_index": "📈 Current meter reading value.",
            "old_index": "📉 Previous meter reading value.",
            "consumption_level_1": "⚡ Amount of electricity consumed in the period.",
            "counter_coefficient": "📊 Multiplication factor for the meter reading.",
            "client_catg": "👥 Category of the client (residential, commercial, etc.).",
            "invoice_year": "📆 Year when the invoice was generated.",
            "creation_year": "🗓️ Year when the account was created.",
            "creation_month": "📅 Month when the account was created."
        }

        # Display feature explanations
        feature_explanation = st.selectbox("Select a feature to learn more:", data.columns)
        st.write(
            f"{feature_explanation}: {column_descriptions.get(feature_explanation, 'No description available')}"
        )

        # Display feature statistics
        st.write(f"Statistics for {feature_explanation}:")
        st.write(data[feature_explanation].describe())

        # Add some insights about fraud detection
        st.header("💡 Key Insights for Fraud Detection")
        st.write(
            """
            Understanding these features is crucial for fraud detection:
            
            1. **Consumption Patterns** 📊
               * Unusual changes in consumption levels
               * Inconsistencies between new and old index values
               * Abnormal counter coefficient values

            2. **Account Characteristics** 👤
               * Account age and history
               * Client category patterns
               * Seasonal variations in usage

            3. **Time-based Patterns** ⏰
               * Creation date anomalies
               * Invoice timing patterns
               * Historical consumption trends
            """
        )

    else:
        st.error("Please log in to access the App. Username: admin Password: Admin01")

if __name__ == "__main__":
    data_page() 