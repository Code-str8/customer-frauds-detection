import streamlit as st
import pandas as pd 
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from auth_util.auth import login_form, is_authenticated

st.set_page_config(
    page_icon="📊",
    page_title="Dashboard",
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

def dashboard_page():
    login_form()
    if is_authenticated():
        # Replace direct data loading with cached function
        data = load_data()
        if data is None:
            return
            
        st.title("**Fraud Detection Dashboard** 📈🔍")
        st.write(
            """
            Explore insightful visualizations and uncover key patterns in fraud detection through these interactive dashboards.
            Monitor trends, analyze risk factors, and identify potential fraud indicators.
            """
        )

        try:
            # EDA Dashboard
            def create_eda_dashboard(data):
                # Consumption Distribution
                st.subheader("Distribution of Consumption Patterns")
                fig_consumption = px.histogram(
                    data,
                    x="consommation_level_1",
                    title="Distribution of Consumption Levels",
                    color_discrete_sequence=['skyblue']
                )
                st.plotly_chart(fig_consumption)

                # Counter Coefficient Distribution
                fig_coefficient = px.histogram(
                    data,
                    x="counter_coefficient",
                    title="Distribution of Counter Coefficients",
                    color_discrete_sequence=['lightgreen']
                )
                st.plotly_chart(fig_coefficient)

                # Account Age Distribution
                fig_age = px.histogram(
                    data,
                    x="months_number",
                    title="Distribution of Account Ages",
                    color_discrete_sequence=['coral']
                )
                st.plotly_chart(fig_age)

                # Client Category Distribution
                fig_category = px.bar(
                    data["client_catg"].value_counts().reset_index(),
                    x="index",
                    y="client_catg",
                    title="Distribution of Client Categories",
                    labels={"index": "Client Category", "client_catg": "Count"}
                )
                st.plotly_chart(fig_category)

                # Correlation Matrix
                st.subheader("Correlation Matrix of Numerical Features")
                numeric_cols = ["counter_number", "months_number", "new_index", 
                              "old_index", "consommation_level_1", "counter_coefficient"]
                correlation_matrix = data[numeric_cols].corr()
                fig_corr = px.imshow(
                    correlation_matrix,
                    color_continuous_scale='icefire',
                    title="Feature Correlations"
                )
                st.plotly_chart(fig_corr)

            # KPIs Dashboard
            def create_kpis_dashboard(data):
                # Time Series Analysis
                st.subheader("Consumption Trends Over Time")
                fig_time = px.line(
                    data.groupby("invoice_year")["consommation_level_1"].mean().reset_index(),
                    x="invoice_year",
                    y="consommation_level_1",
                    title="Average Consumption by Year"
                )
                st.plotly_chart(fig_time)

                # Consumption by Client Category
                fig_cat_consumption = px.box(
                    data,
                    x="client_catg",
                    y="consommation_level_1",
                    title="Consumption Distribution by Client Category"
                )
                st.plotly_chart(fig_cat_consumption)

                # Index Difference Analysis
                data['index_difference'] = data['new_index'] - data['old_index']
                fig_diff = px.histogram(
                    data,
                    x="index_difference",
                    title="Distribution of Index Differences",
                    color_discrete_sequence=['lightcoral']
                )
                st.plotly_chart(fig_diff)

                # Monthly Patterns
                fig_monthly = px.bar(
                    data.groupby("creation_month")["consommation_level_1"].mean().reset_index(),
                    x="creation_month",
                    y="consommation_level_1",
                    title="Average Consumption by Month"
                )
                st.plotly_chart(fig_monthly)

            def create_kpis(data):
                total_records = len(data)
                avg_consumption = data['consommation_level_1'].mean()
                avg_account_age = data['months_number'].mean()
                unique_clients = data['client_catg'].nunique()

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Records 📊", f"{total_records:,}")
                col2.metric("Avg Consumption ⚡", f"{avg_consumption:.2f}")
                col3.metric("Avg Account Age 📅", f"{avg_account_age:.0f} days")
                col4.metric("Client Categories ��", unique_clients)

                # Additional Metrics
                st.subheader("Key Performance Indicators")
                
                # Consumption Change
                consumption_change = ((data['new_index'] - data['old_index']) / data['old_index'] * 100).mean()
                st.metric("Average Consumption Change", f"{consumption_change:.2f}%")

                # High Consumption Alerts
                high_consumption = len(data[data['consommation_level_1'] > data['consommation_level_1'].quantile(0.95)])
                st.metric("High Consumption Alerts 🚨", high_consumption)

            # Dashboard selection
            st.sidebar.header("Select Dashboard Type:")
            dashboard_type = st.sidebar.selectbox("", ["EDA", "KPIs"])

            if dashboard_type == "EDA":
                create_eda_dashboard(data)
            elif dashboard_type == "KPIs":
                create_kpis(data)
                create_kpis_dashboard(data)
            else:
                st.error("Invalid dashboard type.")

        except FileNotFoundError:
            st.error(
                """
                ❌ Dataset file not found. Please ensure:
                1. The dataset file exists in the Dataset folder
                2. The file name is correct (Lp2_df_coc.xlsx)
                3. You have the necessary permissions to access the file
                """
            )
        except Exception as e:
            st.error(f"An error occurred while loading the data: {str(e)}")

    else:
        st.error("Please log in to access the App. Username: admin Password: Admin01")

if __name__ == "__main__":
    dashboard_page() 