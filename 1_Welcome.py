import streamlit as st
from PIL import Image
import os
from auth_util.auth import login_form, is_authenticated

st.set_page_config(
    page_icon="🔍",
    page_title="Fraud Detection",
    layout="centered"
)

def main_page():
    login_form()
    if is_authenticated():
        st.write("Welcome! 🎉")

        st.title("**Customer Fraud Detection** 🔍⚡")

        st.write(
            """
            Detect potential fraudulent activities in customer transactions using advanced machine learning. 
            This app leverages our fraud detection API to provide real-time predictions.

            **Note:** This app uses real-time API predictions for fraud detection.

            ### **Why is fraud detection important?**

            [Customer fraud](https://www.investopedia.com/terms/f/fraud.asp) can significantly impact your business's financial health and reputation. 
            Early detection helps prevent losses and maintain trust with legitimate customers.

            **Key features:**
            * Real-time fraud detection
            * Advanced machine learning models
            * User-friendly interface
            * Secure API integration
            """
        )

        # Add fraud detection image
        fraud_img = Image.open(
            os.path.join(
                os.getcwd(),
                "images/fraud image 2.jpg"
            )
        )

        st.image(
            fraud_img,
            caption="Protect your business from fraud with real-time detection",
            use_column_width=True
        )

        st.markdown(
            """
            #### **Benefits of Using This App**
            * 🎯 Real-time Detection: Get instant fraud predictions for transactions
            * 📊 Data-driven Decisions: Make informed decisions based on ML predictions
            * 🔒 Risk Management: Proactively identify and prevent fraudulent activities
            * 💰 Cost Savings: Reduce losses from fraudulent transactions
            """
        )

        # Call-to-action
        st.write("## Try it out! 🚀")
        st.write("*Ready to detect fraud?* 👀")
        gif_path = 'images/mike-myers-austin-powers gif.gif'
        st.image(
        gif_path, 
        #caption='Retain Customers'
        )

        # Instructions
        st.write(
            """
            Head over to the [*Predict*](/Predict) page to analyze transactions for potential fraud.

            For more information about the app's functionality and technical details, visit our documentation.
            """
        )

        # Contact information
        st.write(
            """
            **Source Code:** [GitHub Repository](https://github.com/Code-str8/customer-frauds-detection)
            
            ### Contact Us 📧
            For support or inquiries, reach out to our team.
            """
        )
    else:
        st.error("Please log in to access the App. Username: admin Password: Admin01")

if __name__ == "__main__":
    main_page() 