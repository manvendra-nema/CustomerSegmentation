import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
# from wordcloud import WordCloud

# Load the dataset
# df = pd.read_csv("D:\Downloads\online\Online Retail.xlsx", sep=",", encoding="ISO-8859-1")
df = pd.read_excel("D:\Downloads\online\Online Retail.xlsx", dtype={'CustomerID': str,'InvoiceID': str})

# Data Preparation
df = df.dropna()
df['CustomerID'] = df['CustomerID'].astype(str)
df['Amount'] = df['Quantity'] * df['UnitPrice']
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%d-%m-%Y %H:%M')

max_date = df['InvoiceDate'].max()
df['Diff'] = (max_date - df['InvoiceDate']).dt.days
rfm_m = df.groupby('CustomerID')['Amount'].sum().reset_index()
rfm_f = df.groupby('CustomerID')['InvoiceNo'].count().reset_index()
rfm_f.columns = ['CustomerID', 'Frequency']
rfm_p = df.groupby('CustomerID')['Diff'].min().reset_index()
rfm = pd.merge(rfm_m, rfm_f, on='CustomerID')
rfm = pd.merge(rfm, rfm_p, on='CustomerID')
rfm.columns = ['CustomerID', 'Amount', 'Frequency', 'Recency']

# Standardize and Cluster
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['Amount', 'Frequency', 'Recency']])
kmeans = KMeans(n_clusters=3, max_iter=50)
clusters = kmeans.fit_predict(rfm_scaled)
rfm['Cluster_Id'] = clusters

# Save Scaler and KMeans
with open('scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)

with open('kmeans.pkl', 'wb') as kmeans_file:
    pickle.dump(kmeans, kmeans_file)

# Merge df with rfm to get cluster information
df_with_clusters = pd.merge(df, rfm[['CustomerID', 'Cluster_Id']], on='CustomerID')

# Function to get text for a cluster
def get_text_for_cluster(cluster_id):
    cluster_df = df_with_clusters[df_with_clusters['Cluster_Id'] == cluster_id]
    text = ' '.join(cluster_df['Description'].dropna().astype(str))
    return text

# Save cluster descriptions and keywords
cluster_info = {
    0: {
        'description': "Cluster 1: High-value customers with high transaction amounts. They make frequent purchases.",
        'keywords': get_text_for_cluster(0)
    },
    1: {
        'description': "Cluster 2: Frequent buyers with moderate transaction amounts.",
        'keywords': get_text_for_cluster(1)
    },
    2: {
        'description': "Cluster 3: Customers with fewer recent purchases and lower transaction amounts.",
        'keywords': get_text_for_cluster(2)
    }
}

with open('cluster_info.pkl', 'wb') as cluster_file:
    pickle.dump(cluster_info, cluster_file)

print("Pickle files saved successfully.")