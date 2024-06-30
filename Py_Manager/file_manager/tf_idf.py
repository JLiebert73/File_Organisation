import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import concurrent.futures

def load_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_text_files(directory):
    texts = []
    filenames = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                filenames.append(os.path.join(root, file))
    return filenames

def parallel_load_texts(filenames):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        texts = list(executor.map(load_text_file, filenames))
    return texts

def compute_tfidf_vectorizer(documents):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    return vectorizer, tfidf_matrix

def tfidf_search(directory, query, top_n=5):
    filenames = load_text_files(directory)
    if not filenames:
        return []

    texts = parallel_load_texts(filenames)

    # Include the query in the list of documents for vectorization
    documents = texts + [query]

    # Vectorize the documents and the query
    vectorizer, tfidf_matrix = compute_tfidf_vectorizer(documents)

    # Compute the cosine similarity between the query and all documents
    query_vector = tfidf_matrix[-1]
    cosine_similarities = (tfidf_matrix[:-1] * query_vector.T).toarray().flatten()

    # Get the indices of the top_n most similar documents
    top_indices = cosine_similarities.argsort()[-top_n:][::-1]

    top_files = [(filenames[i], cosine_similarities[i]) for i in top_indices]
    return top_files
