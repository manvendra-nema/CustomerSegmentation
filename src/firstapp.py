# import streamlit as st
# import pickle
# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans
# from dateutil import parser
# from io import StringIO
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# from collections import Counter
# import nltk
# from nltk.corpus import stopwords

# # Load NLTK stopwords
# nltk.download('stopwords')
# stop_words = set(stopwords.words('english'))

# # Load the scaler, KMeans model, and cluster information
# with open('scaler.pkl', 'rb') as scaler_file:
#     scaler = pickle.load(scaler_file)

# with open('kmeans.pkl', 'rb') as kmeans_file:
#     kmeans = pickle.load(kmeans_file)

# with open('cluster_info.pkl', 'rb') as cluster_file:
#     cluster_info = pickle.load(cluster_file)

# # Function to calculate RFM metrics from CSV
# def calculate_rfm_from_csv(csv_file):
#     df = pd.read_csv(csv_file)
#     df['InvoiceDate'] = df['InvoiceDate'].apply(lambda x: parser.parse(x, dayfirst=True))
#     max_date = pd.Timestamp('2011-12-09 12:50:00')
#     df['Amount'] = df['Quantity'] * df['UnitPrice']
#     rfm_m = df.groupby('CustomerID')['Amount'].sum().reset_index()
#     rfm_f = df.groupby('CustomerID')['InvoiceNo'].count().reset_index()
#     rfm_f.columns = ['CustomerID', 'Frequency']
#     df['Diff'] = max_date - df['InvoiceDate']
#     rfm_p = df.groupby('CustomerID')['Diff'].min().reset_index()
#     rfm_p['Diff'] = rfm_p['Diff'].dt.days
#     rfm = pd.merge(rfm_m, rfm_f, on='CustomerID')
#     rfm = pd.merge(rfm, rfm_p, on='CustomerID')
#     rfm.columns = ['CustomerID', 'Amount', 'Frequency', 'Recency']
#     return rfm

# # Function to get cluster inference
# def get_cluster_inference(cluster_id):
#     return cluster_info[cluster_id]['description']

# # Function to get top keywords for a cluster
# def get_keywords_for_cluster(cluster_id):
#     return cluster_info[cluster_id]['keywords']

# # Function to generate top words table
# def generate_top_words_table(text):
#     words = [word for word in text.split() if word.lower() not in stop_words and len(word) > 3]
#     word_counts = Counter(words)
    
#     # Get top 10 most common words
#     top_words = word_counts.most_common(10)
#     top_words_df = pd.DataFrame(top_words, columns=['Keyword', 'Frequency'])
    
#     # Reset index for clean display and start index from 1
#     top_words_df.index += 1
    
#     return top_words_df

# # Function to generate a word cloud image
# def generate_wordcloud_image(text):
#     words = [word for word in text.split() if word.lower() not in stop_words and len(word) > 3]
#     wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
    
#     fig, ax = plt.subplots(figsize=(10, 5))
#     ax.imshow(wordcloud, interpolation='bilinear')
#     ax.axis('off')
#     return fig

# # Streamlit app
# st.title("Customer Clustering with K-Means")

# # Option to upload CSV file
# st.header("Upload CSV File for RFM Calculation (Optional)")
# uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# if uploaded_file is not None:
#     rfm = calculate_rfm_from_csv(uploaded_file)
#     st.write("RFM Calculation Completed")
#     st.write(rfm.head())

# # Input fields
# st.header("Enter Customer Data")
# amount = st.number_input('Transaction Amount', min_value=0.01, step=0.01)
# frequency = st.number_input('Transaction Frequency', min_value=1)
# recency = st.number_input('Recency (Days since last transaction)', min_value=1)

# if st.button("Predict Cluster and Get Recommendations"):
#     if uploaded_file is not None:
#         # Predict clusters from CSV data
#         rfm_data = rfm[['Amount', 'Frequency', 'Recency']]
#         rfm_scaled = scaler.transform(rfm_data)
        
#         # Predict clusters
#         rfm['Cluster_Id'] = kmeans.predict(rfm_scaled)
#         st.write("RFM Data with Predicted Clusters")
#         st.write(rfm.head())
        
#         # Display cluster details
#         for cluster_id in rfm['Cluster_Id'].unique():
#             st.subheader(f"Cluster {cluster_id+1} Details")
#             st.write(get_cluster_inference(cluster_id))
#             st.write("Top 10 Words:")
#             cluster_df = rfm[rfm['Cluster_Id'] == cluster_id]
            
#             # Display top words table
#             top_words_df = generate_top_words_table(get_keywords_for_cluster(cluster_id))
#             st.write(top_words_df)
#     else:
#         # Predict cluster based on input fields
#         customer_data = [[amount, frequency, recency]]
#         customer_data_scaled = scaler.transform(customer_data)
#         cluster_id = kmeans.predict(customer_data_scaled)[0]
        
#         # Display result
#         st.subheader(f"Customer belongs to Cluster {cluster_id+1}")
#         st.write(get_cluster_inference(cluster_id))
#         st.write("Top 10 Words:")
        
#         # Display top words table
#         top_words_df = generate_top_words_table(get_keywords_for_cluster(cluster_id))
#         st.write(top_words_df)
    
#     st.write("Generating word cloud...")
#     with st.spinner('Generating word cloud...'):
#         # Generate and display word cloud
#         keywords_text = get_keywords_for_cluster(cluster_id)
#         wordcloud_fig = generate_wordcloud_image(keywords_text)
#         st.pyplot(wordcloud_fig)
import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from dateutil import parser
from io import StringIO
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Load NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load the scaler, KMeans model, and cluster information
with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

with open('kmeans.pkl', 'rb') as kmeans_file:
    kmeans = pickle.load(kmeans_file)

with open('cluster_info.pkl', 'rb') as cluster_file:
    cluster_info = pickle.load(cluster_file)

# Function to validate the CSV data
def validate_csv(df):
    required_columns = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']

    # Check for missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check for negative values in Quantity and UnitPrice
    if (df['Quantity'] < 0).any() or (df['UnitPrice'] < 0).any():
        return False, "Negative values detected in Quantity or UnitPrice."

    # Check if there's more than one unique CustomerID
    if len(df['CustomerID'].unique()) > 1:
        return False, "Multiple CustomerIDs found. Please provide data for only one customer."

    return True, "CSV file is valid."

# Function to calculate RFM metrics from CSV
def calculate_rfm_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    
    # Validate the CSV data
    is_valid, message = validate_csv(df)
    if not is_valid:
        st.error(message)
        return None

    df['InvoiceDate'] = df['InvoiceDate'].apply(lambda x: parser.parse(x, dayfirst=True))
    max_date = pd.Timestamp('2011-12-09 12:50:00')
    df['Amount'] = df['Quantity'] * df['UnitPrice']
    rfm_m = df.groupby('CustomerID')['Amount'].sum().reset_index()
    rfm_f = df.groupby('CustomerID')['InvoiceNo'].count().reset_index()
    rfm_f.columns = ['CustomerID', 'Frequency']
    df['Diff'] = max_date - df['InvoiceDate']
    rfm_p = df.groupby('CustomerID')['Diff'].min().reset_index()
    rfm_p['Diff'] = rfm_p['Diff'].dt.days
    rfm = pd.merge(rfm_m, rfm_f, on='CustomerID')
    rfm = pd.merge(rfm, rfm_p, on='CustomerID')
    rfm.columns = ['CustomerID', 'Amount', 'Frequency', 'Recency']
    return rfm

# Function to get cluster inference
def get_cluster_inference(cluster_id):
    return cluster_info[cluster_id]['description']

# Function to get top keywords for a cluster
def get_keywords_for_cluster(cluster_id):
    return cluster_info[cluster_id]['keywords']

# Function to generate top words table
def generate_top_words_table(text):
    words = [word for word in text.split() if word.lower() not in stop_words and len(word) > 3]
    word_counts = Counter(words)
    
    # Get top 10 most common words
    top_words = word_counts.most_common(10)
    top_words_df = pd.DataFrame(top_words, columns=['Keyword', 'Frequency'])
    
    # Reset index for clean display and start index from 1
    top_words_df.index += 1
    
    return top_words_df

# Function to generate a word cloud image
def generate_wordcloud_image(text):
    words = [word for word in text.split() if word.lower() not in stop_words and len(word) > 3]
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

# Streamlit app
st.title("Customer Clustering with K-Means")

# Option to upload CSV file
st.header("Upload CSV File for RFM Calculation (Optional)")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    rfm = calculate_rfm_from_csv(uploaded_file)
    if rfm is not None:
        st.write("RFM Calculation Completed")
        st.write(rfm.head())

# Input fields
st.header("Enter Customer Data")
amount = st.number_input('Transaction Amount', min_value=0.01, step=0.01)
frequency = st.number_input('Transaction Frequency', min_value=1)
recency = st.number_input('Recency (Days since last transaction)', min_value=1)

if st.button("Predict Cluster and Get Recommendations"):
    if uploaded_file is not None and rfm is not None:
        # Predict clusters from CSV data
        rfm_data = rfm[['Amount', 'Frequency', 'Recency']]
        rfm_scaled = scaler.transform(rfm_data)
        
        # Predict clusters
        rfm['Cluster_Id'] = kmeans.predict(rfm_scaled)
        st.write("RFM Data with Predicted Clusters")
        st.write(rfm.head())
        
        # Display cluster details
        for cluster_id in rfm['Cluster_Id'].unique():
            st.subheader(f"Cluster {cluster_id} Details")
            st.write(get_cluster_inference(cluster_id))
            st.write("Top 10 Words:")
            cluster_df = rfm[rfm['Cluster_Id'] == cluster_id]
            
            # Display top words table
            top_words_df = generate_top_words_table(get_keywords_for_cluster(cluster_id))
            st.write(top_words_df)
    else:
        # Predict cluster based on input fields
        customer_data = [[amount, frequency, recency]]
        customer_data_scaled = scaler.transform(customer_data)
        cluster_id = kmeans.predict(customer_data_scaled)[0]
        
        # Display result
        st.subheader(f"Customer belongs to Cluster {cluster_id+1}")
        st.write(get_cluster_inference(cluster_id))
        st.write("Top 10 Words:")
        
        # Display top words table
        top_words_df = generate_top_words_table(get_keywords_for_cluster(cluster_id))
        st.write(top_words_df)
    
    st.write("Generating word cloud...")
    with st.spinner('Generating word cloud...'):
        # Generate and display word cloud
        keywords_text = get_keywords_for_cluster(cluster_id)
        wordcloud_fig = generate_wordcloud_image(keywords_text)
        st.pyplot(wordcloud_fig)