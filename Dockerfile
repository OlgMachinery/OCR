FROM python:3.10-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libsm6 libxext6 libxrender-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la app
COPY . .

# Expone el puerto
EXPOSE 5000

# Comando de inicio
CMD ["python", "app.py"]
