# Customer Frauds Detection 🔍⚡

This project addresses a fraud detection challenge for STEG (Tunisian Company of Electricity and Gas), focusing on identifying fraudulent meter manipulation through billing history data.

## 📋 Table of Contents

- [Introduction](#introduction)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
  - [Streamlit App](#streamlit-app)
  - [API Usage](#api-usage)
  - [Model Training](#model-training)
- [API Documentation](#api-documentation)
- [Methodology](#methodology)
- [Results](#results)
- [Challenges & Trade-offs](#challenges--trade-offs)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Introduction

The goal of this project is to develop a machine learning model that can accurately detect fraudulent activities in electricity and gas consumption. By analyzing historical billing data, the model aims to help STEG reduce losses due to fraud.

## 💾 Dataset

The dataset consists of historical billing data, including features such as client ID, invoice date, consumption levels, and counter types. The target variable indicates whether a client is fraudulent or not.

## 🛠️ Installation

To run this project, you need to have Python installed along with the required libraries. You can install the dependencies using the following command:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

### 💫 Streamlit App

We've developed an interactive Streamlit application that provides a user-friendly interface for fraud detection:

1. Start the Streamlit app:
   ```bash
   streamlit run 1_Welcome.py
   ```

2. Login credentials:
   - Username: admin
   - Password: Admin01

The app includes several features:

#### 🏠 Welcome Page
![Welcome Page](images/app%201.PNG)
![Welcome Page](images/app%202.PNG)
![Welcome Page](images/app%203.PNG)
A welcoming interface introducing the fraud detection system.

#### 📚 Data Explorer
![Data Explorer](images/app%204.PNG)
![Data Explorer](images/app%205.PNG)
![Data Explorer](images/app%206.PNG)
![Data Explorer](images/app%207.PNG)
Explore and analyze the dataset with interactive visualizations.


#### 🔮 Prediction Interface
![Prediction Form](images/app%208.PNG)
![Prediction Form](images/app%209.PNG)
Easy-to-use form for making fraud predictions:
- Input transaction details
- Choose between models
- Get instant predictions

![Prediction Results](images/app%2010.PNG)
Detailed prediction results with confidence scores.

#### ⏳ History Tracking
![Prediction History](images/app%2011.PNG)
![Prediction History](images/app%2012.PNG)
Track and analyze prediction history:
- View all past predictions
- Analyze trends
- Export results
### 🔄 API Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/customer-frauds-detection.git
   ```

2. Navigate to the project directory:
   ```bash
   cd customer-frauds-detection
   ```

3. Start the API server:
   ```bash
   uvicorn api:app
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/docs
   ```

The API provides two main endpoints ✨:
- `/stacked/predict`: Uses the stacked ensemble model
- `/xgb/predict`: Uses the XGBoost model

![API Documentation UI](images/api%201.PNG)
![API Documentation UI](images/api%202.PNG)

Example of making predictions using the API:

![API Prediction Example - Stacked Model](images/stacked%20api%203.PNG)
![API Prediction Example - Stacked Model](images/stacked%20api%204.PNG)
![API Prediction Example - XGBoost Model](images/xgb%20api%205.PNG)
![API Prediction Example - XGBoost Model](images/xgb%20api%206.PNG)

### 🤖 Model Training

To train or experiment with the models:

1. Run the Jupyter Notebook:
   ```bash
   jupyter notebook fraud_detection.ipynb
   ```

## 📝 API Documentation

The API accepts the following input parameters:

```json
{
    "counter_number": int,
    "account_age_days": int,
    "new_index": int,
    "old_index": int,
    "consumption_level_1": float,
    "counter_coefficient": float,
    "client_catg": int,
    "invoice_year": int,
    "creation_year": int,
    "creation_month": int
}
```

Response format:
```json
{
    "prediction": int,  // 0 or 1
    "probability": string,  // percentage
    "prediction_text": string  // "Fraudulent" or "Non-Fraudulent"
}
```

Example curl request:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/stacked/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "counter_number": 0,
    "account_age_days": 0,
    "new_index": 0,
    "old_index": 0,
    "consumption_level_1": 0,
    "counter_coefficient": 0,
    "client_catg": 0,
    "invoice_year": 2015,
    "creation_year": 0,
    "creation_month": 6
  }'
```

## 🏗️ Methodology

The project follows these steps:
1. **Data Preprocessing** 📊: Cleaning and transforming the data to make it suitable for modeling.
2. **Exploratory Data Analysis (EDA)** 📊: Visualizing data distributions and relationships.
3. **Feature Engineering** ✨: Creating new features and selecting the most relevant ones.
4. **Modeling** 🤖: Training various machine learning models, including ensemble methods.
5. **Evaluation** 📈: Assessing model performance using cross-validation and ROC AUC scores.

## 📈 Results

The stacked model, combining XGBoost, Extra Trees, and Random Forest, achieved the best performance with an AUC of 0.83. This indicates a strong ability to distinguish between fraudulent and non-fraudulent clients.

## ⚠️ Challenges & Trade-offs

- **Hyperparameter Tuning** ⚙️: Limited by computational resources, which could have improved model robustness.
- **High Variance** 📊: Models performed well on training data but showed lower performance on testing data.
- **Class Imbalance** ⚖️: Addressed through resampling techniques to ensure balanced training data.

## 🔮 Future Work

- ✅ **API Development**: Implemented a FastAPI-based REST API for real-time fraud detection.
- 🔄 **Model Updates**: Regular retraining with new data to maintain accuracy.
- ⚡ **Performance Optimization**: Further API optimization for higher throughput.
- 📊 **Monitoring**: Add model performance monitoring and drift detection.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
