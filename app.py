from flask import Flask, request, jsonify
import cv2
import pytesseract
import tempfile
import os
import traceback

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "online"})

@app.route("/ocr", methods=["POST"])
def ocr():
    processed_path = None

    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        img_file = request.files['image']
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img_path = temp.name
        img_file.save(img_path)

        image = cv2.imread(img_path)
        if image is None:
            raise Exception("Failed to read image with OpenCV")

        # 🖼️ Redimensiona si es muy grande
        max_width = 1600
        if image.shape[1] > max_width:
            scale = max_width / image.shape[1]
            new_size = (max_width, int(image.shape[0] * scale))
            image = cv2.resize(image, new_size)

        # Preprocesamiento mejorado
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        processed_path = img_path.replace(".png", "_processed.png")
        cv2.imwrite(processed_path, thresh)

        config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed_path, lang='eng+spa', config=config)

        return jsonify({"text": text.strip()})

    except Exception as e:
        print("🔥 OCR ERROR:")
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

    finally:
        if os.path.exists(img_path):
            os.remove(img_path)
        if processed_path and os.path.exists(processed_path):
            os.remove(processed_path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
