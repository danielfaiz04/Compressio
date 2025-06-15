import os

def compress_rle(input_path, output_folder):
    """Compress file using Run-Length Encoding."""
    try:
        # Read input file
        with open(input_path, 'rb') as f:
            data = f.read()
        
        # Create output filename
        filename = os.path.basename(input_path)
        output_filename = f"compressed_{filename}"
        output_path = os.path.join(output_folder, output_filename)
        
        # Perform RLE compression
        compressed_data = bytearray()
        i = 0
        while i < len(data):
            # Count consecutive identical bytes
            count = 1
            while i + count < len(data) and data[i] == data[i + count] and count < 255:
                count += 1
            
            # Write count and byte
            compressed_data.extend([count, data[i]])
            i += count
        
        # Write compressed data
        with open(output_path, 'wb') as f:
            f.write(compressed_data)
        
        return output_path
    except Exception as e:
        print(f"Error in compress_rle: {str(e)}")
        raise

def decompress_rle(input_path, output_folder):
    """Decompress file using Run-Length Encoding (dummy implementation)."""
    # Read compressed file
    with open(input_path, 'rb') as f:
        compressed_data = f.read()
    
    # Create output filename
    filename = os.path.basename(input_path)
    output_filename = f"decompressed_{filename.replace('compressed_', '')}"
    output_path = os.path.join(output_folder, output_filename)
    
    # Perform RLE decompression
    decompressed_data = bytearray()
    i = 0
    while i < len(compressed_data):
        count = compressed_data[i]
        byte = compressed_data[i + 1]
        decompressed_data.extend([byte] * count)
        i += 2
    
    # Write decompressed data
    with open(output_path, 'wb') as f:
        f.write(decompressed_data)
    
    return output_path 