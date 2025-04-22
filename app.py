import os
import pytesseract
import cv2
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "🟢 API OCR en línea y funcional."

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No se recibió ninguna imagen'}), 400

    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Convierte a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # OCR
    text = pytesseract.image_to_string(gray, lang='spa')

    return jsonify({'text': text})

# Necesario si se usa flask run como en el Dockerfile
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
