# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dpLZWgeiZQvuwh9YB2Ni6tc4CMIlQ_JJ
"""

pip install -U sentence-transformers
pip install lbl2vec

pip install streamlit

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load and preprocess your unlabelled data
data = pd.read_csv('dataaaa.csv')
data.fillna(np.nan, inplace=True)  # Replace null values with NaN
text_samples = data['text']

# Convert text to numerical features using TF-IDF vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(text_samples)

# Encode text samples using a pre-trained transformer-based model
model = SentenceTransformer('bert-base-nli-mean-tokens')
embeddings = model.encode(text_samples)

# Perform hierarchical clustering on the text embeddings
n_clusters = 5  # Number of clusters
clustering = AgglomerativeClustering(n_clusters=n_clusters)
cluster_labels = clustering.fit_predict(embeddings)

# Define appropriate types for each cluster (adjust as needed)
cluster_types = {
    0: 'News',
    1: 'Customer Reviews',
    2: 'Social Media',
    3: 'Technical Discussions',
    4: 'Blogs/Opinions'
}

# Streamlit app
st.title('Text Category Detection')

# User input
text_input = st.text_input('Enter a text sample:', '')

# Classify user input
if text_input:
    # Encode user input
    text_embedding = model.encode([text_input])
    similarities = cosine_similarity(text_embedding, embeddings)[0]
    most_similar_cluster = np.argmax(similarities)
    cluster_label = cluster_labels[most_similar_cluster]
    cluster_type = cluster_types[cluster_label]

    # Display the detected category type
    st.write(f'Detected Category Type: {cluster_type}')