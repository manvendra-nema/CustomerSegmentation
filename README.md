# Customer Clustering with K-Means

## Overview

Welcome to the Customer Clustering project! This project utilizes K-Means clustering to segment customers based on their transaction data. The goal is to identify distinct customer groups and understand their purchasing behavior. The project includes a Streamlit app that allows users to predict which cluster a customer belongs to based on transaction metrics and visualize key insights.

## Project Structure

- **`data_preprocessing.py`**: Pre-processes the data, calculates RFM values, and saves the necessary models and information.
- **`firstapp.py`**: Streamlit application that provides interactive features for clustering and visualization.
- **`requirements.txt`**: Lists all the Python packages required for running the project.

## Features

### 1. Clustering Analysis
- **K-Means Clustering**: Apply K-Means clustering algorithm to categorize customers into clusters.
- **Cluster Inferences**: Understand each cluster's characteristics and purchasing behavior.

### 2. Streamlit Application
- **Predict Cluster**: Enter transaction data (Amount, Frequency, Recency) to predict which cluster a new customer belongs to.
- **CSV Upload**: Upload a CSV file containing transaction data to calculate RFM values and predict the cluster.
- **Keyword Visualization**: View the top keywords associated with each cluster, including a word cloud and table of top items.

## Installation

1. **Clone the Repository:**
   git clone https://github.com/yourusername/customer-clustering.git
   cd customer-clustering
## Usage

### Data Preparation

Before using the Streamlit app, you need to prepare your data and generate the necessary model files. Follow these steps:

1. **Generate Pickle Files:**
   Run the `data_preprocessing.py` script to preprocess your data, calculate RFM values, and save the required models and cluster information.

   The script will produce several pickle files required by the Streamlit app for making predictions and visualizations.

### Running the Streamlit App

1. **Start the Application:**
   Launch the Streamlit app by running the `firstapp.py` script. This will start a local web server and open the app in your default web browser.

2. **Interact with the App:**
   - **Enter Customer Data:**
     - **Transaction Amount**: Input the transaction amount for the customer.
     - **Transaction Frequency**: Enter the number of transactions made by the customer.
     - **Recency (Days since last transaction)**: Provide the number of days since the customer's last transaction.

     Click the "Predict Cluster" button to see which cluster the customer belongs to, along with detailed insights about that cluster.

   - **Upload CSV File:**
     If you don’t have the individual RFM values, you can upload a CSV file containing transaction data. The app will calculate RFM values, predict the cluster, and display the results.

     The CSV file should contain the following columns:
     - `InvoiceNo`
     - `StockCode`
     - `Description`
     - `Quantity`
     - `InvoiceDate`
     - `UnitPrice`
     - `CustomerID`
     - `Country`

   - **View Keywords:**
     For each cluster, you can view:
     - **Top Keywords Table:** A table showing the top items for the cluster, filtered to include only words longer than three characters. The table displays keywords without frequency data.
     - **Word Cloud:** A visual representation of the most frequent keywords associated with the cluster.

### Example Workflow

1. **Enter Customer Data:**
   - **Transaction Amount**: 150.75
   - **Transaction Frequency**: 12
   - **Recency (Days since last transaction)**: 45

   Click "Predict Cluster" to get the predicted cluster and view its description and keywords.

2. **Upload CSV File:**
   - Click the upload button to select and upload your CSV file.
   - The app will process the file, calculate RFM values, and predict the cluster for the provided data.

## Notes

- Ensure the CSV file is formatted correctly, with the required columns mentioned above.
- Generating the word cloud may take some time depending on the volume of data.

## Contributing

We welcome contributions! If you have suggestions or improvements, please fork the repository and submit a pull request.

