import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import concurrent.futures
import heapq
import random
import math

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

class HNSW:
    def __init__(self, m=16, ef_construction=200):
        self.m = m
        self.ef_construction = ef_construction
        self.levels = {}
        self.entry_point = None
        self.max_level = -1

    def add_node(self, vector, level):
        node_id = len(self.levels)
        self.levels[node_id] = {l: [] for l in range(level + 1)}
        if self.entry_point is None:
            self.entry_point = node_id
            self.max_level = level
        else:
            current_node = self.entry_point
            for current_level in range(self.max_level, level, -1):
                current_node = self._search_layer(current_node, vector, 1, current_level)[0]
            for current_level in range(min(level, self.max_level), -1, -1):
                neighbors = self._search_layer(current_node, vector, self.ef_construction, current_level)
                self.levels[node_id][current_level] = neighbors
                for neighbor in neighbors:
                    self.levels[neighbor][current_level].append(node_id)
                current_node = neighbors[0]

    def _search_layer(self, entry_point, query_vector, ef, level):
        visited = set()
        candidates = [(self._distance(self.levels[entry_point][level], query_vector), entry_point)]
        heapq.heapify(candidates)
        closest = candidates[0]
        while candidates:
            distance, candidate = heapq.heappop(candidates)
            if distance > closest[0]:
                break
            for neighbor in self.levels[candidate][level]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    distance = self._distance(self.levels[neighbor][level], query_vector)
                    if distance < closest[0]:
                        closest = (distance, neighbor)
                        heapq.heappush(candidates, (distance, neighbor))
        return [node for _, node in heapq.nsmallest(ef, candidates)]

    def _distance(self, vector1, vector2):
        return np.linalg.norm(vector1 - vector2)

    def search(self, query_vector, top_n):
        current_node = self.entry_point
        for level in range(self.max_level, -1, -1):
            current_node = self._search_layer(current_node, query_vector, 1, level)[0]
        result = self._search_layer(current_node, query_vector, top_n, 0)
        return result

def build_hnsw(tfidf_matrix, m=16, ef_construction=200):
    num_documents = tfidf_matrix.shape[0]
    hnsw = HNSW(m, ef_construction)
    for i in range(num_documents):
        level = int(-math.log(random.random()) * m)
        hnsw.add_node(tfidf_matrix[i].toarray().flatten(), level)
    return hnsw

def tfidf_search(directory, query, top_n=5, m=16, ef_construction=200):
    filenames = load_text_files(directory)
    if not filenames:
        return []

    texts = parallel_load_texts(filenames)
    documents = texts + [query]
    vectorizer, tfidf_matrix = compute_tfidf_vectorizer(documents)
    query_vector = tfidf_matrix[-1]
    tfidf_matrix = tfidf_matrix[:-1]

    hnsw = build_hnsw(tfidf_matrix, m, ef_construction)
    top_indices = hnsw.search(query_vector.toarray().flatten(), top_n)

    top_files = [(filenames[i], 1 - cosine_similarity(tfidf_matrix[i], query_vector)[0][0]) for i in top_indices]
    return top_files
