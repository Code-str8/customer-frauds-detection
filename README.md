# Customer Frauds Detection

This project addresses a fraud detection challenge for STEG (Tunisian Company of Electricity and Gas), focusing on identifying fraudulent meter manipulation through billing history data.

## Table of Contents

- [Introduction](#introduction)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Results](#results)
- [Challenges & Trade-offs](#challenges--trade-offs)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The goal of this project is to develop a machine learning model that can accurately detect fraudulent activities in electricity and gas consumption. By analyzing historical billing data, the model aims to help STEG reduce losses due to fraud.

## Dataset

The dataset consists of historical billing data, including features such as client ID, invoice date, consumption levels, and counter types. The target variable indicates whether a client is fraudulent or not.

## Installation

To run this project, you need to have Python installed along with the required libraries. You can install the dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/customer-frauds-detection.git
   ```
2. Navigate to the project directory:
   ```bash
   cd customer-frauds-detection
   ```
3. Run the Jupyter Notebook:
   ```bash
   jupyter notebook fraud_detection.ipynb
   ```

## Methodology

The project follows these steps:
1. **Data Preprocessing**: Cleaning and transforming the data to make it suitable for modeling.
2. **Exploratory Data Analysis (EDA)**: Visualizing data distributions and relationships.
3. **Feature Engineering**: Creating new features and selecting the most relevant ones.
4. **Modeling**: Training various machine learning models, including ensemble methods.
5. **Evaluation**: Assessing model performance using cross-validation and ROC AUC scores.

## Results

The stacked model, combining XGBoost, Extra Trees, and Random Forest, achieved the best performance with an AUC of 0.83. This indicates a strong ability to distinguish between fraudulent and non-fraudulent clients.

## Challenges & Trade-offs

- **Hyperparameter Tuning**: Limited by computational resources, which could have improved model robustness.
- **High Variance**: Models performed well on training data but showed lower performance on testing data.
- **Class Imbalance**: Addressed through resampling techniques to ensure balanced training data.

## Future Work

- **App Development**: Plan to develop a user-friendly application for real-time fraud detection.
- **API Integration**: Implement an API to allow external systems to interact with the fraud detection model.
- **Image Folder**: Create an `images` folder to store emojis and images used in this README and other documentation.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.