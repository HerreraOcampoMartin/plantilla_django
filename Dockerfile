# Usa una imagen oficial de Python como base
FROM python:3.12-slim

# Establece variables de entorno para Gunicorn y el entorno
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE="app.settings.production"

# 1. Configuración del Entorno
# Crea un directorio de trabajo y un usuario no-root
WORKDIR /usr/src/app
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /usr/src/app

# 2. Copia de Requisitos e Instalación
# Copia solo el archivo de requisitos para aprovechar el cache de Docker
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia el resto del código de la aplicación
COPY . /usr/src/app/

# Configura al usuario no-root
USER appuser

# 4. Comando de Ejecución (Gunicorn)
# El puerto 8000 es el estándar de Django/Gunicorn
# Ajusta los workers según tu número de CPU (2 * num_cores + 1)
EXPOSE 8000
CMD gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 3
