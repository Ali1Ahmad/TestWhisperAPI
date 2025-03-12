import os
from flask import Flask, request, render_template, send_file, jsonify
import pyttsx3
import requests
import uuid

app = Flask(__name__)

# Replace with your actual Groq key
GROQ_API_KEY = "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"

# 1) Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# 2) Text-to-Speech endpoint
@app.route('/tts', methods=['POST'])
def tts():
    text = request.form.get('text')  # text from form data
    if not text:
        return jsonify({"error": "No text provided."}), 400
    
    # Generate a unique filename so multiple users don’t collide
    output_filename = f"tts_output_{uuid.uuid4().hex}.wav"
    
    # Use pyttsx3 to generate WAV
    engine = pyttsx3.init()
    engine.save_to_file(text, output_filename)
    engine.runAndWait()
    
    # Send file back to the client
    return send_file(output_filename, mimetype="audio/wav")

# 3) Speech-to-Text endpoint
@app.route('/stt', methods=['POST'])
def stt():
    # We expect a file named "audio" in the request
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({"error": "No audio file received."}), 400
    
    # Save to a temporary file
    temp_filename = f"recorded_{uuid.uuid4().hex}.wav"
    audio_file.save(temp_filename)
    
    # Now call Groq Whisper API
    try:
        transcription_text = groq_transcribe(temp_filename)
        # Clean up the temp file
        os.remove(temp_filename)
        return jsonify({"transcription": transcription_text})
    except Exception as e:
        os.remove(temp_filename)
        return jsonify({"error": str(e)}), 500

def groq_transcribe(wav_path):
    """
    Send the WAV file to Groq Whisper API for transcription.
    """
    url = "https://api.groq.com/openai/v1/audio/transcriptions"  # For same-language STT
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    
    # "file" -> file to upload
    files = {"file": open(wav_path, "rb")}
    
    data = {
        "model": "distil-whisper-large-v3-en"  # or "distil-whisper-large-v3-en" etc.
        # "language": "en"
    }
    
    response = requests.post(url, headers=headers, files=files, data=data)
    if response.status_code == 200:
        result = response.json()
        # Groq typically returns {"text": "..."}
        return result.get("text", "")
    else:
        raise Exception(f"Groq Error {response.status_code}: {response.text}")

if __name__ == '__main__':
    app.run(debug=True)
