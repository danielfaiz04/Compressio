from PIL import Image
import os
import numpy as np
from collections import Counter
import heapq
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_dict(data):
    """Build frequency dictionary from input data."""
    freq_dict = defaultdict(int)
    for byte in data:
        freq_dict[byte] += 1
    return freq_dict

def build_huffman_tree(freq_dict):
    """Build Huffman tree from frequency dictionary."""
    heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        internal = HuffmanNode(None, left.freq + right.freq)
        internal.left = left
        internal.right = right
        
        heapq.heappush(heap, internal)
    
    return heap[0]

def build_huffman_codes(root, current_code="", codes=None):
    """Build Huffman codes from Huffman tree."""
    if codes is None:
        codes = {}
    
    if root is None:
        return
    
    if root.char is not None:
        codes[root.char] = current_code if current_code else "0"
    
    build_huffman_codes(root.left, current_code + "0", codes)
    build_huffman_codes(root.right, current_code + "1", codes)
    
    return codes

def compress_huffman(input_path, output_folder):
    """Compress file using Huffman coding."""
    try:
        # Read input file
        with open(input_path, 'rb') as f:
            data = f.read()
        
        # Build frequency dictionary and Huffman tree
        freq_dict = build_frequency_dict(data)
        huffman_tree = build_huffman_tree(freq_dict)
        huffman_codes = build_huffman_codes(huffman_tree)
        
        # Create output filename
        filename = os.path.basename(input_path)
        output_filename = f"compressed_{filename}"
        output_path = os.path.join(output_folder, output_filename)
        
        # Write compressed data
        with open(output_path, 'wb') as f:
            # Write frequency dictionary
            f.write(len(freq_dict).to_bytes(4, 'big'))
            for char, freq in freq_dict.items():
                f.write(char.to_bytes(1, 'big'))
                f.write(freq.to_bytes(4, 'big'))
            
            # Write compressed data
            compressed_data = ''.join(huffman_codes[byte] for byte in data)
            # Pad to multiple of 8
            padding = (8 - len(compressed_data) % 8) % 8
            compressed_data += '0' * padding
            
            # Convert to bytes
            for i in range(0, len(compressed_data), 8):
                byte = int(compressed_data[i:i+8], 2)
                f.write(byte.to_bytes(1, 'big'))
        
        return output_path
    except Exception as e:
        print(f"Error in compress_huffman: {str(e)}")
        raise

def decompress_huffman(input_path, output_folder):
    """Decompress file using Huffman coding (dummy implementation)."""
    # Read compressed file
    with open(input_path, 'rb') as f:
        # Read frequency dictionary
        dict_size = int.from_bytes(f.read(4), 'big')
        freq_dict = {}
        for _ in range(dict_size):
            char = int.from_bytes(f.read(1), 'big')
            freq = int.from_bytes(f.read(4), 'big')
            freq_dict[char] = freq
        
        # Read compressed data
        compressed_data = f.read()
    
    # Build Huffman tree
    huffman_tree = build_huffman_tree(freq_dict)
    
    # Create output filename
    filename = os.path.basename(input_path)
    output_filename = f"decompressed_{filename.replace('compressed_', '')}"
    output_path = os.path.join(output_folder, output_filename)
    
    # Write decompressed data (dummy implementation)
    with open(output_path, 'wb') as f:
        current = huffman_tree
        for byte in compressed_data:
            for bit in format(byte, '08b'):
                if bit == '0':
                    current = current.left
                else:
                    current = current.right
                
                if current.char is not None:
                    f.write(current.char.to_bytes(1, 'big'))
                    current = huffman_tree
    
    return output_path

def compress_image(input_path, output_folder):
    """Compress image using Huffman coding (simplified version)."""
    # Read image
    img = Image.open(input_path)
    img_array = np.array(img)
    
    # Flatten image array
    flat_array = img_array.flatten()
    
    # Build Huffman tree and codes
    tree = build_huffman_tree(flat_array)
    codes = build_huffman_codes(tree)
    
    # Encode the image data
    encoded_data = ''.join(codes[pixel] for pixel in flat_array)
    
    # Pad the encoded data to make it byte-aligned
    padding = 8 - (len(encoded_data) % 8)
    encoded_data += '0' * padding
    
    # Convert binary string to bytes
    encoded_bytes = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i+8]
        encoded_bytes.append(int(byte, 2))
    
    # Save compressed data
    output_filename = f"compressed_{os.path.basename(input_path)}.huf"
    output_path = os.path.join(output_folder, output_filename)
    
    with open(output_path, 'wb') as f:
        # Save metadata
        f.write(img_array.shape[0].to_bytes(4, 'big'))  # height
        f.write(img_array.shape[1].to_bytes(4, 'big'))  # width
        f.write(padding.to_bytes(1, 'big'))  # padding
        # Save encoded data
        f.write(bytes(encoded_bytes))
    
    return output_path 