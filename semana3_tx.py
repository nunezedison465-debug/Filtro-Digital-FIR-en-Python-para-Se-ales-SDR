import numpy as np
import adi
import time

# 1. Configuración del SDR (ADALM-Pluto)
# Nos conectamos a la IP por defecto
sdr = adi.Pluto('ip:192.168.2.1')
sdr.sample_rate = int(1e6)         # Frecuencia de muestreo (1 MHz)
sdr.tx_rf_bandwidth = int(1e6)     # Ancho de banda
sdr.tx_lo = int(900e6)             # Frecuencia portadora (900 MHz)
sdr.tx_hardwaregain_chan0 = -10    # Ganancia para no saturar

# 2. Generación de la señal multi-tono (50, 200 y 300 kHz)
fs = sdr.sample_rate
N = 10000 # Número de muestras
t = np.arange(N) / fs

# Creamos los tres tonos como señales complejas (I/Q)
tono1 = np.exp(2j * np.pi * 50e3 * t)
tono2 = np.exp(2j * np.pi * 200e3 * t)
tono3 = np.exp(2j * np.pi * 300e3 * t)

# Sumamos los tonos y escalamos la señal para el DAC del Pluto
senal_tx = tono1 + tono2 + tono3
senal_tx = senal_tx / np.max(np.abs(senal_tx)) # Normalizar
senal_tx = senal_tx * (2**14) # Ajustar a 14 bits

# 3. Transmisión
print("Iniciando transmisión de la señal multi-tono...")
sdr.tx_cyclic_buffer = True # Esto hace que la señal se repita infinitamente
sdr.tx(senal_tx)

print("¡Transmitiendo! El Pluto está enviando la señal al aire.")
print("Presiona Ctrl + C en la terminal para detener la transmisión.")

try:
    # Mantenemos el programa corriendo para que el Pluto siga transmitiendo
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDeteniendo transmisión y limpiando buffer...")
    sdr.tx_destroy_buffer()