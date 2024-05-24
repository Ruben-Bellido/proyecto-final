# Usamos una imagen base de Python
FROM python:3.10

# Definimos el directorio de trabajo en el contenedor
WORKDIR /manager_app

# Copiamos el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalamos las dependencias desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./app.py"]
