# Compressio - File Compression Web Application

Compressio is a web-based file compression application that allows users to compress and decompress files with a clean, user-friendly interface. The application features Firebase Authentication for secure access and session-based compression limits.

## Features

- File compression and decompression
- Google Sign-In authentication via Firebase
- Session-based compression history
- Support for various file types (images, documents)
- Clean and responsive UI
- No database required (uses sessionStorage/localStorage)

## Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript (Vanilla)
- Firebase Authentication

### Backend
- Python 3
- Flask
- Flask-CORS

## Project Structure

```
compressio/
├── backend/
│   ├── app.py
│   ├── utils/
│   │   ├── file_utils.py
│   │   ├── huffman.py
│   │   └── rle.py
├── frontend/
│   ├── index.html
│   ├── result.html
│   ├── about.html
│   ├── login.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── app.js
│   │   ├── compress.js
│   │   └── auth.js
│   └── assets/
├── static/
│   ├── uploads/
│   └── downloads/
└── README.md
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/compressio.git
cd compressio
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure Firebase:
   - Create a new Firebase project
   - Enable Google Authentication
   - Add your Firebase configuration to `frontend/js/auth.js`

4. Run the backend server:
```bash
python app.py
```

5. For frontend development:
   - Use VS Code Live Server or any static file server
   - Open `frontend/index.html` in your browser

## Usage

1. Open the application in your browser
2. Sign in with Google (optional)
3. Upload files for compression/decompression
4. View compression history and download results

## Limitations

- Non-authenticated users are limited to 5 compressions per session
- Authenticated users have unlimited compression access
- Supported file types: .png, .jpg, .txt, .pdf

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 