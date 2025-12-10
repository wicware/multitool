import serial
from scope import Scope
import time

# --- Configuración Inicial ---
s = Scope()
s.glitch.repeat = 7
SERIAL_PORT = '/dev/ttyUSB0' # Reemplaza con tu puerto serie real (ej. COM3 en Windows)
BAUD_RATE = 115200             # Reemplaza con la velocidad en baudios correcta

# Función para intentar abrir el puerto serie
def open_serial_port():
    while True:
        try:
            # Intentamos abrir el puerto serial
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            print(f"Puerto serie {SERIAL_PORT} abierto correctamente.")
            return ser
        except serial.SerialException as e:
            print(f"Error al abrir el puerto serie: {e}")
            print("Esperando a que el dispositivo se conecte...")
            time.sleep(2)

# --- Bucle Principal de Ejecución ---
ser = open_serial_port()

while (1):
    for width in range (2, 200, 1):
        s.glitch.repeat = width
        for pulses in range (2, 200, 1):
            
            # --- Monitoreo del Puerto Serie ---
            # Intentamos leer una línea o verificar la conexión antes de ejecutar s.trigger()
            try:
                # Intenta leer una línea del puerto serie. 
                # Si el dispositivo se desconecta, esto puede lanzar una excepción 
                # si el timeout expira o si la conexión física se pierde.
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(f"Datos recibidos: {line}")
                
                # Si todo está bien, disparamos el trigger
                s.trigger() 

            except serial.SerialException:
                # Esta excepción se dispara si el puerto serie se cierra inesperadamente
                print("-" * 40)
                print(f"¡ADVERTENCIA: Conexión serial perdida!")
                print(f"Parámetros actuales a la espera: WIDTH = {width}, PULSES = {pulses}")
                print("Pausando ejecución del script. Reconectando...")
                print(" GLITCHEADO  !!!!!")
                print("-" * 40)
                
                # Cierra el objeto serie actual e intenta reabrirlo
                ser.close()
                ser = open_serial_port()
                
                # Continúa con la siguiente iteración del bucle exterior (while True) 
                # reanudando los parámetros guardados (width y pulses)
                continue 
            
            except Exception as e:
                # Captura otros posibles errores de lectura/decodificación
                print(f"Ocurrió un error inesperado al leer datos seriales: {e}")
                time.sleep(1)

        time.sleep(0.5)

