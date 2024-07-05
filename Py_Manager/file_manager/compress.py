import heapq
import os
import pickle
import multiprocessing
from collections import Counter
from shutil import move

class HuffmanNode:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_frequency_table(data):
    return Counter(data)

def build_huffman_tree(frequency_table):
    heap = []
    for char, frequency in frequency_table.items():
        node = HuffmanNode(char, frequency)
        heapq.heappush(heap, node)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged_node = HuffmanNode(None, node1.frequency + node2.frequency)
        merged_node.left = node1
        merged_node.right = node2
        heapq.heappush(heap, merged_node)

    return heap[0]

def build_encoding_table(huffman_tree):
    encoding_table = {}
    def traverse(node, code):
        if node.char:
            encoding_table[node.char] = code
        else:
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")
    traverse(huffman_tree, "")
    return encoding_table

def compress_chunk(data_chunk, encoding_table):
    encoded_data = ""
    for char in data_chunk:
        encoded_data += encoding_table[char]
    return encoded_data

def compress_text(input_file):
    output_file = os.path.splitext(input_file)[0] + ".huff"

    with open(input_file, "r") as file:
        data = file.read().rstrip()

    num_chunks = multiprocessing.cpu_count()
    chunk_size = len(data) // num_chunks
    data_chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    with multiprocessing.Pool() as pool:
        frequency_tables = pool.map(build_frequency_table, data_chunks)
    
    frequency_table = sum(frequency_tables, Counter())

    huffman_tree = build_huffman_tree(frequency_table)
    encoding_table = build_encoding_table(huffman_tree)

    with multiprocessing.Pool() as pool:
        encoded_chunks = pool.starmap(compress_chunk, [(chunk, encoding_table) for chunk in data_chunks])
    
    encoded_data = ''.join(encoded_chunks)

    padding = 8 - len(encoded_data) % 8
    huffman_tree_pickle = pickle.dumps(huffman_tree)
    encoded_data += "0" * padding

    byte_data = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i + 8]
        byte_data.append(int(byte, 2))

    with open(output_file, "wb") as file:
        file.write(bytes([padding]))
        file.write(len(huffman_tree_pickle).to_bytes(4, byteorder='big'))
        file.write(huffman_tree_pickle)
        file.write(byte_data)

    print("File compressed successfully!")

def decompress_text(input_file):
    with open(input_file, "rb") as file:
        padding = int.from_bytes(file.read(1), byteorder='big')
        huffman_tree_length = int.from_bytes(file.read(4), byteorder='big')
        huffman_tree_pickle = file.read(huffman_tree_length)
        reconstructed_tree = pickle.loads(huffman_tree_pickle)
        compressed_data = file.read()

    decoded_data = decode_data(compressed_data, reconstructed_tree, padding)

    output_file = os.path.splitext(input_file)[0] + "_decompressed.txt"
    with open(output_file, "w") as file:
        file.write(decoded_data)

    print("File decompressed successfully!")

def decode_data(compressed_data, huffman_tree, padding):
    decoded_data = ""
    current_node = huffman_tree

    compressed_index = 0
    bit_string = ""
    for byte in compressed_data:
        bit_string += f"{byte:08b}"

    bit_string = bit_string[:-padding]  # Remove padding bits

    for bit in bit_string:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char:
            decoded_data += current_node.char
            current_node = huffman_tree

    return decoded_data
