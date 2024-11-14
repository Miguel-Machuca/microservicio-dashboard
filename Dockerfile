# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY electrodomesticos.csv electrodomesticos.csv

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que tu aplicación utiliza (ajusta según tu app)
EXPOSE 5000

# Define el comando para ejecutar tu aplicación
CMD ["python", "app.py"]
