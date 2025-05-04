from flask import Flask, request, jsonify
import cv2
import tempfile
import os
import traceback
import base64
import requests

app = Flask(__name__)

# API Key de Google Cloud Vision directamente en uso
google_api_key = "AIzaSyCEUciixN-yfxSIPrw0_UqNIKCwS41WWFU"

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "online"})

@app.route("/ocr", methods=["POST"])
def ocr():
    processed_path = None
    img_path = None

    try:
        if 'image' not in request.files:
            return jsonify({"error": "No se subió ninguna imagen"}), 400

        # Guardar imagen temporal
        img_file = request.files['image']
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img_path = temp.name
        img_file.save(img_path)

        # Preprocesamiento con OpenCV
        image = cv2.imread(img_path)
        if image is None:
            raise Exception("OpenCV no pudo leer la imagen")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Guardar imagen procesada
        processed_path = img_path.replace(".png", "_processed.png")
        cv2.imwrite(processed_path, thresh)

        # Codificar imagen para Google Vision
        with open(processed_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode("utf-8")

        url = f"https://vision.googleapis.com/v1/images:annotate?key={google_api_key}"
        body = {
            "requests": [{
                "image": {"content": encoded_image},
                "features": [{"type": "TEXT_DETECTION"}]
            }]
        }

        response = requests.post(url, json=body)
        result = response.json()
        text = result['responses'][0].get('fullTextAnnotation', {}).get('text', '').strip()

        return jsonify({
            "text": text
        })

    except Exception as e:
        print("🔥 OCR ERROR:")
        traceback.print_exc()
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

    finally:
        if img_path and os.path.exists(img_path):
            os.remove(img_path)
        if processed_path and os.path.exists(processed_path):
            os.remove(processed_path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
