# TestWhisperAPI

This project provides a simple API that interacts with Whisper, an AI-based speech-to-text model. It includes a backend written in Python using Flask and a frontend script written in JavaScript.

## Installation and Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Node.js and npm
- pip (Python package manager)
- A virtual environment tool (recommended)

### Clone the Repository
```sh
git clone <repository_url>
cd TestWhisperAPI
```

### Backend Setup (Python Flask API)
1. **Create and activate a virtual environment** (Recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the Flask application**
   ```sh
   python app.py
   ```
   By default, the Flask server runs on `http://127.0.0.1:5000/`.

### Frontend Setup (JavaScript)
1. **Navigate to the frontend directory** (if applicable)
   ```sh
   cd frontend  # Adjust if needed
   ```
2. **Install frontend dependencies** (if applicable)
   ```sh
   npm install
   ```
3. **Run the frontend script**
   ```sh
   node script.js
   ```

## Usage
1. Ensure the backend is running (`app.py`).
2. Run the frontend (`script.js`).
3. The API will process speech-to-text requests via Whisper.

## API Endpoints
- `POST /transcribe` - Accepts audio input and returns transcribed text.

## Dependencies
### Python (Backend)
Install dependencies using:
```sh
pip install -r requirements.txt
```

### JavaScript (Frontend)
Ensure `node.js` and `npm` are installed and run:
```sh
npm install
```

## Contributing
Feel free to fork this project and submit pull requests.

## License
This project is licensed under the MIT License.

## Author
Ali Ahmad

