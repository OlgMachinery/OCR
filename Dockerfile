# Usa una imagen base ligera
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto para Render (usará una variable de entorno $PORT)
EXPOSE $PORT

# Comando para correr el servidor con Flask (más ligero que Gunicorn)
CMD ["flask", "run", "--host=0.0.0.0", "--port=$PORT"]
