FROM python:3.10-slim

# Instala Tesseract + español + OpenCV dependencias
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libsm6 libxext6 libxrender-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crea y entra al directorio de trabajo
WORKDIR /app

# Copia los archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expone el puerto de Flask
EXPOSE 5000

# Comando de inicio
CMD ["python", "app.py"]
