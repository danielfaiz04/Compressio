from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from utils.file_utils import validate_file, save_file
from utils.huffman import compress_huffman, decompress_huffman
from utils.rle import compress_rle, decompress_rle
import sys

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'downloads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'txt', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload and download directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static_frontend(path):
    return send_from_directory('../frontend', path)

@app.route('/api/compress', methods=['POST'])
def compress_file():
    print("DEBUG: Masuk ke /api/compress", file=sys.stderr)
    sys.stderr.flush()
    if 'file' not in request.files:
        print("DEBUG: Tidak ada file di request", file=sys.stderr)
        sys.stderr.flush()
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    algorithm = request.form.get('algorithm', 'auto')
    
    if file.filename == '':
        print("DEBUG: Tidak ada file yang dipilih", file=sys.stderr)
        sys.stderr.flush()
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        print(f"DEBUG: File type not allowed: {file.filename}", file=sys.stderr)
        sys.stderr.flush()
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"DEBUG: Menyimpan file ke {filepath}", file=sys.stderr)
        sys.stderr.flush()
        file.save(filepath)
        
        # Determine compression algorithm based on file type
        if algorithm == 'auto':
            ext = filename.rsplit('.', 1)[1].lower()
            if ext in ['png', 'jpg', 'jpeg']:
                algorithm = 'huffman'
            else:
                algorithm = 'rle'
        
        print(f"Using compression algorithm: {algorithm}")
        
        # Compress file
        if algorithm == 'huffman':
            output_path = compress_huffman(filepath, app.config['DOWNLOAD_FOLDER'])
        else:
            output_path = compress_rle(filepath, app.config['DOWNLOAD_FOLDER'])
        
        print(f"Compressed file saved to: {output_path}")
        
        # Get file sizes
        original_size = os.path.getsize(filepath)
        compressed_size = os.path.getsize(output_path)
        compression_ratio = (1 - (compressed_size / original_size)) * 100
        
        # Clean up uploaded file
        os.remove(filepath)
        
        response_data = {
            'success': True,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': round(compression_ratio, 2),
            'output_filename': os.path.basename(output_path),
            'algorithm': algorithm
        }
        print(f"Sending response: {response_data}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.stderr.flush()
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500

@app.route('/api/decompress', methods=['POST'])
def decompress_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    algorithm = request.form.get('algorithm', 'auto')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Decompress file
        if algorithm == 'huffman':
            output_path = decompress_huffman(filepath, app.config['DOWNLOAD_FOLDER'])
        else:
            output_path = decompress_rle(filepath, app.config['DOWNLOAD_FOLDER'])
        
        return jsonify({
            'success': True,
            'output_filename': os.path.basename(output_path)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        print(f"Attempting to download file: {file_path}")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return jsonify({'error': 'File not found'}), 404
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print(f"Error during download: {str(e)}")
        return jsonify({'error': str(e)}), 404

# Add CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 