FROM python:3.11-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Establece directorio de trabajo
WORKDIR /app

# Copia archivos
COPY . .

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto estándar para Render
EXPOSE 10000

# Usa gunicorn para producción
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

