FROM python:3.10.4-slim
WORKDIR /mocksensor

# Copiamos los dos scripts de los sensores
COPY mocksensor_1.py mocksensor_1.py
COPY mocksensor_2.py mocksensor_2.py

# Copiamos el script de arranque y le damos permisos de ejecución
COPY start.sh start.sh
RUN chmod +x start.sh

# El comando ahora ejecuta el script que lanza ambos sensores
CMD ["./start.sh"]