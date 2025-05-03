# Imagen base con Python 3.11 y slim
FROM python:3.11-slim

# Instalar dependencias del sistema requeridas por OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Puerto expuesto (Render lo asigna automáticamente vía $PORT)
ENV PORT=5000

# Comando de inicio (Gunicorn, recomendado por Render)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
