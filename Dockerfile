# ✅ Imagen base de Python
FROM python:3.11-slim

# ✅ Actualiza e instala librerías necesarias
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ✅ Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copiar el resto del código
COPY . .

# ✅ Exponer puerto
EXPOSE 5000

# ✅ Iniciar servidor
CMD ["python", "app.py"]
