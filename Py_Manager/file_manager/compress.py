import heapq
import os
import pickle  

class HuffmanNode:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_frequency_table(data):
    frequency_table = {}
    for char in data:
        if char in frequency_table:
            frequency_table[char] += 1
        else:
            frequency_table[char] = 1
    return frequency_table

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

def compress_text(input_file):
    output_file = os.path.splitext(input_file)[0] + ".huff"

    with open(input_file, "r") as file:
        data = file.read().rstrip()

    frequency_table = build_frequency_table(data)
    huffman_tree = build_huffman_tree(frequency_table)
    encoding_table = build_encoding_table(huffman_tree)

    encoded_data = ""
    for char in data:
        encoded_data += encoding_table[char]

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
    while compressed_index < len(compressed_data) - padding:
        bit = int(compressed_data[compressed_index])
        if bit == 0:
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char:
            decoded_data += current_node.char
            current_node = huffman_tree

        compressed_index += 1

    return decoded_data
