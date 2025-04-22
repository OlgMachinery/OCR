FROM python:3.11-slim

# Instala tesseract y el idioma español + dependencias para OpenCV
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Usa gunicorn para producción en Render, en el puerto proporcionado por el sistema
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app"]
