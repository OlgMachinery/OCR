FROM python:3.11-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean

# Copiar archivos al contenedor
WORKDIR /app
COPY . /app

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# CORREGIDO: ejecutar gunicorn con shell para que lea $PORT correctamente
CMD gunicorn -b 0.0.0.0:$PORT app:app
