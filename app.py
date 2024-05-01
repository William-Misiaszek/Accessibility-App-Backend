from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging
import os
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

    filename = secure_filename(file.filename)
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, filename)
    file.save(file_path)

    # Initialize and run the AccessibilityProcessor
    processor = AccessibilityProcessor(file_path)
    processor.initialize_agents()

    # Load the HTML content
    processor.load_and_parse_html()
    
    # Store the original HTML for comparison
    original_html = processor.original_html
    
    processor.analyze_html()

    results = processor.summarize_changes()
    updated_html = processor.updated_html

    app.logger.info(f"File processed: {filename}")

    # Return the results, including the original HTML
    return jsonify({
        'summary': results,
        'updated_html': updated_html,
        'original_html': original_html
    })

if __name__ == '__main__':
    app.run(debug=True)
