import streamlit as st
import pandas as pd
import requests
import json
from PIL import Image
import os
from auth_util.auth import login_form, is_authenticated

st.set_page_config(
    page_icon="🔮",
    page_title="Predict",
    layout="wide"
)

def save_prediction(data, result):
    # Ensure the Data directory exists
    if not os.path.exists("Data"):
        os.makedirs("Data")
    
    # Prepare the data to save
    data_to_save = data.copy()
    # Remove the % symbol and store as float
    probability = float(result["probability"].strip('%'))
    data_to_save.update({
        "prediction": result["prediction"],
        "probability": probability,  # Store as number, not string
        "timestamp": pd.Timestamp.now()
    })
    
    # Convert to DataFrame
    df = pd.DataFrame([data_to_save])
    
    # Append to CSV
    file_path = "Data/History.csv"
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)

def main():
    login_form()
    if is_authenticated():
        st.title("**Fraud Detection Prediction** 🔍")
        st.write(
            """
            Protect your business from fraud! This tool uses our advanced machine learning API 
            to analyze transactions and identify potential fraudulent activities in real-time.
            """
        )

        # Add fraud prediction image
        fraud_img = Image.open(
            os.path.join(
                os.getcwd(),
                "images/fraud image"
            )
        )

        st.image(
            fraud_img,
            use_column_width=True,
            caption="Real-time fraud detection for your transactions"
        )

        # Initialize session state for predictions
        if 'prediction' not in st.session_state:
            st.session_state.prediction = None

        # Create form for user input
        with st.form(key='fraud_detection_form', clear_on_submit=True):
            st.header('**Transaction Details** 📝')
            
            # Transaction information
            counter_number = st.number_input('Counter Number', min_value=0)
            account_age_days = st.number_input('Account Age (days)', min_value=0)
            new_index = st.number_input('New Index', min_value=0)
            old_index = st.number_input('Old Index', min_value=0)
            consumption_level_1 = st.number_input('Consumption Level', min_value=0.0)
            counter_coefficient = st.number_input('Counter Coefficient', min_value=0.0)
            
            # Client information
            st.header('**Client Information** 👤')
            client_catg = st.number_input('Client Category', min_value=0)
            invoice_year = st.number_input('Invoice Year', min_value=2000, max_value=2030)
            creation_year = st.number_input('Creation Year', min_value=1900, max_value=2030)
            creation_month = st.number_input('Creation Month', min_value=1, max_value=12)

            submit_button = st.form_submit_button(label='Detect Fraud')

        if submit_button:
            # Prepare the data for API request
            data = {
                "counter_number": counter_number,
                "account_age_days": account_age_days,
                "new_index": new_index,
                "old_index": old_index,
                "consumption_level_1": consumption_level_1,
                "counter_coefficient": counter_coefficient,
                "client_catg": client_catg,
                "invoice_year": invoice_year,
                "creation_year": creation_year,
                "creation_month": creation_month
            }

            # Make API request
            try:
                # Choose between stacked and XGB models
                model_choice = st.radio(
                    "Select Model:",
                    ["Stacked Model", "XGBoost Model"]
                )

                api_endpoint = "http://localhost:8000/stacked/predict" if model_choice == "Stacked Model" else "http://localhost:8000/xgb/predict"
                
                response = requests.post(api_endpoint, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Store prediction in session state
                    st.session_state.prediction = result
                    
                    # Save the prediction
                    save_prediction(data, result)
                    
                    # Display prediction results
                    st.subheader("Prediction Results 📊")
                    
                    # Create columns for better layout
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        prediction_text = "🚨 Fraudulent" if result["prediction"] == 1 else "✅ Non-Fraudulent"
                        st.markdown(f"**Prediction:** {prediction_text}")
                    
                    with col2:
                        st.markdown(f"**Probability:** {result['probability']}")
                    
                    # Add explanation based on prediction
                    if result["prediction"] == 1:
                        st.warning(
                            """
                            ⚠️ **High Risk Transaction Detected**
                            
                            This transaction shows patterns consistent with fraudulent activity. 
                            We recommend:
                            * Immediate review of the transaction
                            * Verification of client information
                            * Additional security checks
                            """
                        )
                    else:
                        st.success(
                            """
                            ✅ **Low Risk Transaction**
                            
                            This transaction appears to be legitimate. 
                            Standard processing can continue.
                            """
                        )
                    
                else:
                    st.error(f"Error from API: {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error(
                    """
                    ❌ **API Connection Error**
                    
                    Could not connect to the fraud detection API. Please ensure:
                    1. The API server is running
                    2. You're connected to the correct network
                    3. The API endpoint is accessible
                    
                    Try running: `uvicorn api:app --reload`
                    """
                )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    else:
        st.error("Please log in to access the App. Username: admin Password: Admin01")

if __name__ == "__main__":
    main() 