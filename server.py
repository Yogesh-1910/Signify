from flask import Flask, jsonify, request, send_file, Response
from flask_cors import CORS
import inference_classifier
import translate  # Import the translate module
import cv2
import os
import time
import subprocess

app = Flask(__name__, static_folder='webpage', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Camera Control Routes
@app.route('/start-camera', methods=['POST'])
def start_camera():
    inference_classifier.start_camera()  # Start camera in inference_classifier
    return jsonify({'output': 'Camera Started'})

@app.route('/stop-camera', methods=['POST'])
def stop_camera():
    inference_classifier.stop_camera()  # Stop camera in inference_classifier
    return jsonify({'output': 'Camera Stopped'})

# Detection Control Routes
@app.route('/start-detection', methods=['POST'])
def start_detection():
    inference_classifier.start_detection()  # Start detection process
    return jsonify({'output': 'Detection Started'})

@app.route('/stop-detection', methods=['POST'])
def stop_detection():
    inference_classifier.stop_detection()  # Stop detection process
    return jsonify({'output': 'Detection Stopped'})

# Save detected text
@app.route('/save-text', methods=['POST'])
def save_text():
    inference_classifier.save_text()  # Save detected text
    return jsonify({'output': 'Text Saved'})

# Clear detected text
@app.route('/clear-text', methods=['POST'])
def clear_text_route():
    inference_classifier.clear_text()  # Clear saved text
    return jsonify({'output': 'Text Cleared'})

# Get detected letters
@app.route('/get-detected-letters', methods=['GET'])
def get_detected_letters():
    with open("detected_letters.txt", "r") as file:
        detected_letters = file.read()
    return jsonify({'detected_letters': detected_letters})  # Return detected letters

# Audio Conversion Route
@app.route('/convert-to-audio', methods=['POST'])
def convert_to_audio():
    with open("detected_letters.txt", "r") as file:
        text = file.read().strip()  # Get the detected text from file
    if not text:
        return jsonify({'output': 'No text to convert', 'audio_files': {}})
    audio_files = translate.generate_audio_files_for_all_languages(text)  # Generate audio files
    return jsonify({'output': 'Text Converted to Audio', 'audio_files': audio_files})

# Get audio file
@app.route('/get-audio/<lang_code>', methods=['GET'])
def get_audio(lang_code):
    audio_file = f'audio_output/output_{lang_code}.mp3'
    try:
        if not os.path.exists(audio_file):
            return jsonify({'error': f'Audio file for {lang_code} not found'}), 404
        return send_file(audio_file, mimetype='audio/mpeg')  # Send audio file
    except Exception as e:
        return jsonify({'error': 'Error fetching audio file', 'details': str(e)}), 500

# Video feed route
def generate_frames():
    while True:
        if inference_classifier.cap is None or not inference_classifier.cap.isOpened():
            continue
        success, frame = inference_classifier.cap.read()
        if not success:
            break

        frame = inference_classifier.process_frame(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True, port=8000)