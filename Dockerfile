FROM python:3.11-slim

# Instala dependencias del sistema necesarias para Tesseract y OpenCV
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean

# Copia el código de la app
WORKDIR /app
COPY . /app

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Render define la variable de entorno PORT, la usaremos para correr gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app"]
