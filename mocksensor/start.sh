#!/bin/bash

# Ejecutar el sensor 1 en segundo plano (&)
python mocksensor_1.py &

# Ejecutar el sensor 2 en segundo plano (&)
python mocksensor_2.py &

# Esperar a que cualquier proceso termine (mantiene el contenedor vivo)
wait