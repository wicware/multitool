import serial
from scope import Scope
import time

# --- Configuración Inicial ---
s = Scope()
s.glitch.repeat = 7
SERIAL_PORT = '/dev/ttyUSB0' # Reemplaza con tu puerto serie real (ej. COM3 en Windows)
BAUD_RATE = 115200             # Reemplaza con la velocidad en baudios correcta
RECONNECTION_TIMEOUT_SECONDS = 2.0 # El umbral de tiempo para diferenciar 'glitch' de 'reset'

# Función para intentar abrir el puerto serie, ahora mide el tiempo
def open_serial_port():
    start_time = time.time()
    while True:
        try:
            # Intentamos abrir el puerto serial
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            end_time = time.time()
            recovery_time = end_time - start_time
            
            # Devolvemos el objeto serial y el tiempo de recuperación
            return ser, recovery_time
        
        except serial.SerialException as e:
            # Comprobamos si ya pasó el umbral mientras esperamos
            if time.time() - start_time > RECONNECTION_TIMEOUT_SECONDS:
                 # Este mensaje se repite hasta reconectar
                 print("Esperando a que el dispositivo se conecte (Sistema Reseteado)...")
            time.sleep(0.5) 

# --- Bucle Principal de Ejecución ---
print("Iniciando script. Intentando conectar al puerto serial...")
ser, _ = open_serial_port() # La primera conexión no tiene tiempo de recuperación relevante

while (1):
    for width in range (2, 10, 1):
        s.glitch.repeat = width
        for pulses in range (2, 20, 1):
            
            try:
                # Intenta leer una línea para verificar que la conexión está viva
                if ser.in_waiting > 0:
                   line = ser.readline().decode('utf-8').strip()
                   if line:
                       # print(f"Datos recibidos: {line}")
                       pass
                
                # Si todo está bien, disparamos el trigger
                s.trigger() 

            except serial.SerialException:
                # --- Manejo de Desconexión ---
                print("-" * 60)
                print(f"¡ADVERTENCIA: Conexión serial perdida!")
                print(f"Parámetros a la espera: WIDTH = {width}, PULSES = {pulses}")
                
                # Cierra el objeto serie actual e intenta reabrirlo, midiendo el tiempo
                ser.close()
                # Esta llamada bloquea la ejecución hasta reconectar.
                ser, recovery_time = open_serial_port() 
                
                # --- Reporte de Recuperación con Parámetros ---
                if recovery_time < RECONNECTION_TIMEOUT_SECONDS:
                    print(f"-> RECONEXIÓN RÁPIDA ({recovery_time:.2f}s): Se ha producido un GLITCH.")
                    print(f"-> Reanudando con: WIDTH = {width}, PULSES = {pulses}")
                else:
                    print(f"-> SISTEMA RESETEADO ({recovery_time:.2f}s): Puerto serie reestablecido.")
                    print(f"-> Reanudando con: WIDTH = {width}, PULSES = {pulses}")

                print("-" * 60)
                
                # Continúa con la siguiente iteración del bucle, manteniendo los parámetros actuales
                continue 
            
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
                time.sleep(1)

        time.sleep(1)
