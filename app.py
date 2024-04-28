from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging
import os  # Import the os module
from main import AccessibilityProcessor

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "http://localhost:3000"}})
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/upload', methods=['POST'])
def handle_upload():
    app.logger.info("Upload endpoint was hit")
    file = request.files['file']
    
    # Make sure to secure the filename
    filename = secure_filename(file.filename)
    # Ensure the uploads directory exists
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    file_path = os.path.join(uploads_dir, filename)
    file.save(file_path)
    
    # Initialize and run the AccessibilityProcessor
    processor = AccessibilityProcessor(file_path)
    processor.initialize_agents()
    processor.process()
    
    app.logger.info(f"File processed: {filename}")

    # Collect the results
    results = processor.summarize_changes()
    updated_html = processor.updated_html

    # Return the results
    return jsonify({
        'summary': results,
        'updated_html': updated_html
    })

if __name__ == '__main__':
    app.run(debug=True)
