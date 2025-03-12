import streamlit as st
import pandas as pd
import plotly.express as px
from auth_util.auth import login_form, is_authenticated

st.set_page_config(
    page_icon="⏳",
    page_title="History",
    layout="wide"
)

def history_page():
    login_form()
    if is_authenticated():
        st.title("**Prediction History** 📊")
        st.write(
            """
            View and analyze the history of fraud detection predictions made through the app.
            This helps track patterns and monitor the system's performance over time.
            """
        )

        def load_prediction_history():
            try:
                # Load the history from a CSV file
                history_df = pd.read_csv("Data/History.csv")
                
                # Add timestamp column if not present
                if 'timestamp' not in history_df.columns:
                    history_df['timestamp'] = pd.Timestamp.now()
                
                return history_df
            except FileNotFoundError:
                st.info("No prediction history available yet. Make some predictions to see them here!")
                return None
            except Exception as e:
                st.error(f"Error loading history: {str(e)}")
                return None

        # Add refresh button
        if st.button("🔄 Refresh Data"):
            history_df = load_prediction_history()
            
            if history_df is not None:
                # Display basic statistics
                st.subheader("📈 Prediction Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_predictions = len(history_df)
                    st.metric("Total Predictions", total_predictions)
                
                with col2:
                    if 'prediction' in history_df.columns:
                        fraud_rate = (history_df['prediction'].sum() / total_predictions) * 100
                        st.metric("Fraud Detection Rate", f"{fraud_rate:.2f}%")
                
                with col3:
                    if 'probability' in history_df.columns:
                        avg_probability = history_df['probability'].mean()
                        st.metric("Average Fraud Probability", f"{avg_probability:.2f}%")

                # Display the full history table
                st.subheader("📋 Detailed History")
                st.dataframe(history_df)

                # Create visualizations if there's enough data
                if len(history_df) > 0:
                    st.subheader("📊 Visualizations")
                    
                    # Time series of predictions
                    if 'timestamp' in history_df.columns:
                        fig_timeline = px.line(
                            history_df,
                            x='timestamp',
                            y='probability',
                            title='Fraud Probability Over Time'
                        )
                        st.plotly_chart(fig_timeline)

                    # Distribution of probabilities
                    if 'probability' in history_df.columns:
                        fig_dist = px.histogram(
                            history_df,
                            x='probability',
                            title='Distribution of Fraud Probabilities'
                        )
                        st.plotly_chart(fig_dist)

                    # Prediction counts
                    if 'prediction' in history_df.columns:
                        prediction_counts = history_df['prediction'].value_counts()
                        fig_counts = px.pie(
                            values=prediction_counts.values,
                            names=['Non-Fraudulent', 'Fraudulent'],
                            title='Prediction Distribution'
                        )
                        st.plotly_chart(fig_counts)

    else:
        st.error("Please log in to access the App. Username: admin Password: Admin01")

if __name__ == "__main__":
    history_page() 