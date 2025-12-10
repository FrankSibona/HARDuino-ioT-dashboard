import time
import json
import random

# Variables globales para controlar los tiempos
last_tank_switch_time = 0
tank_state_change_time = 0

# Variable para almacenar cuánto durará el ciclo actual (será dinámico)
current_cycle_duration = 0 

def update_sensor_data(data):
    global last_tank_switch_time, tank_state_change_time, current_cycle_duration
    
    current_time = time.time()
    data["timestamp"] = current_time
    
    # --- 1. Control Maestro: Simular cambio del Flotante Tanque (Aleatorio) ---
    # Si es la primera vez (0), definimos una duración inicial
    if current_cycle_duration == 0:
        current_cycle_duration = random.randint(60, 240) # Entre 1 y 4 minutos

    # Verificamos si ya pasó el tiempo aleatorio definido para este ciclo
    if current_time - last_tank_switch_time > current_cycle_duration:
        # Invertimos el estado
        new_state = 0 if data["flotante_tanque"] == 1 else 1
        
        if new_state != data["flotante_tanque"]:
            data["flotante_tanque"] = new_state
            tank_state_change_time = current_time
            
            # --- AQUÍ ESTÁ LA MAGIA ---
            # Calculamos cuánto durará el PRÓXIMO estado de forma aleatoria
            # Ejemplo: Entre 60 segundos (1 min) y 300 segundos (5 min)
            current_cycle_duration = random.randint(70, 300) 
            
            print(f"--> CAMBIO DE ESTADO: Flotante Tanque ahora es {new_state}")
            print(f"    (El próximo cambio será en {current_cycle_duration} segundos)")
            
        last_tank_switch_time = current_time

    # --- 2. Lógica de Control (Cisterna y Sensores) ---
    time_since_change = current_time - tank_state_change_time
    
    # Valores base calibrados (los que tú me pasaste)
    base_values = {
        "caudal_entrada": 803.0,
        "caudal_salida": 501.0,
        "presion_entrada": 3.0,
        "presion_membrana": 12.0,
        "conductividad": 36.5
    }
    
    analog_keys = list(base_values.keys())

    if data["flotante_tanque"] == 0: # CASO OFF (Tanque Lleno/Parada)
        # A) Todos los sensores a 0 inmediatamente
        for key in analog_keys:
            data[key] = 0.0
            
        # B) Esperar 1 minuto para apagar la cisterna
        if time_since_change > 60:
            data["flotante_cisterna"] = 0

    else: # CASO ON (Tanque Vacío/Marcha)
        # A) Sensores miden con oscilación sobre el valor base
        for key in analog_keys:
            noise = random.uniform(-0.3, 0.3)
            data[key] = base_values[key] + noise
            if data[key] < 0: data[key] = 0.0

        # B) Esperar 1 minuto para encender la cisterna
        if time_since_change > 60:
            data["flotante_cisterna"] = 1

    # Simulación simple del dosificador
    if random.random() < 0.01: 
        data["flotante_dosificador"] = 1 if data["flotante_dosificador"] == 0 else 0

def main():
    global last_tank_switch_time, tank_state_change_time
    
    # Inicialización
    sensor_data = {
        "device_id": "e2e78334",
        "client_id": "c03d5155",
        "sensor_type": "EstadoPlanta",
        # Valores iniciales
        "caudal_entrada": 803.0,
        "caudal_salida": 501.0,
        "presion_entrada": 3.0,
        "presion_membrana": 12.0,
        "conductividad": 36.5,
        "flotante_tanque": 1,
        "flotante_cisterna": 1,
        "flotante_dosificador": 0,
        "timestamp": time.time()
    }
    
    last_tank_switch_time = time.time()
    tank_state_change_time = time.time()

    print("Iniciando simulación con tiempos variables...")
    
    while True:
        update_sensor_data(sensor_data)
        
        with open('/tmp/ouput_mock_sensor_1.json', 'a') as output_file:
            output_file.write(f'{json.dumps(sensor_data)}\n')
        
        time.sleep(1.0)

if __name__ == '__main__':
    main()