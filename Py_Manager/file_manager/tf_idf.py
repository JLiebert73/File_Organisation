import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def load_text_files(directory):
    texts = []
    filenames = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    texts.append(f.read())
                filenames.append(file_path)
    return texts, filenames

def tfidf_search(directory, query, top_n=5):
    texts, filenames = load_text_files(directory)
    if not texts:
        return []

    # Include the query in the list of documents for vectorization
    documents = texts + [query]
    
    # Vectorize the documents and the query
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Compute the cosine similarity between the query and all documents
    query_vector = tfidf_matrix[-1]
    cosine_similarities = (tfidf_matrix[:-1] * query_vector.T).toarray().flatten()
    
    # Get the indices of the top_n most similar documents
    top_indices = cosine_similarities.argsort()[-top_n:][::-1]
    
    top_files = [(filenames[i], cosine_similarities[i]) for i in top_indices]
    return top_files
