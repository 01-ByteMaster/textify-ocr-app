

from flask import Flask, request, jsonify, send_file
import os
import cv2
import numpy as np
from datetime import datetime

from flask_cors import CORS


import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ocr_utils import extract_text_annotate_Image


app = Flask(__name__)
CORS(app)

# Create outputs folder if not exists
OUTPUT_FOLDER = os.path.join(os.getcwd(),'outputs')
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    uploaded_file = request.files['image']
    image_bytes = uploaded_file.read()

    npimg = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Running  OCR and annotate image
    processed_image, extracted_text = extract_text_annotate_Image(image)

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    base_filename = f"output_{timestamp}"

    img_path = os.path.join(OUTPUT_FOLDER, base_filename + '.jpg')
    txt_path = os.path.join(OUTPUT_FOLDER, base_filename + '.txt')

    cv2.imwrite(img_path, processed_image)
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(extracted_text))

    # response
    return jsonify({
        "extracted_text": extracted_text,
        "download_image": f"/download/image?path={img_path}",
        "download_text": f"/download/text?path={txt_path}"
    })

@app.route('/download/image')
def download_image():
    path = request.args.get('path')
    if os.path.exists(path):
        return send_file(path, mimetype='image/jpeg', as_attachment=True)
    return jsonify({'error': 'Image not found'}), 404

@app.route('/download/text')
def download_text():
    path = request.args.get('path')
    if os.path.exists(path):
        return send_file(path, mimetype='text/plain', as_attachment=True)
    return jsonify({'error': 'Text file not found'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
