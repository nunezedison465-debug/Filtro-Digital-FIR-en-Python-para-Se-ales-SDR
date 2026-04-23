import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# 1. Parámetros del filtro según el proyecto
fs = 1e6            # Frecuencia de muestreo (1 MHz para el SDR)
f_corte = 100e3     # Frecuencia de corte: 100 kHz
taps = 64           # Orden del filtro
ventana = 'hamming' # Tipo de ventana

# 2. Diseño del filtro paso bajo FIR usando scipy
coeficientes = signal.firwin(taps, f_corte, fs=fs, window=ventana)

# 3. Cálculo de la respuesta en frecuencia para la gráfica
w, h = signal.freqz(coeficientes, worN=8000)
frecuencias = (fs * 0.5 / np.pi) * w

# 4. Configuración de la gráfica
plt.figure(figsize=(10, 6))
# Convertimos las frecuencias a kHz para que se lea mejor
plt.plot(frecuencias / 1000, 20 * np.log10(np.abs(h)), 'b', linewidth=2) 
plt.title('Semana 1: Respuesta en Frecuencia - Filtro Paso Bajo FIR')
plt.xlabel('Frecuencia (kHz)')
plt.ylabel('Amplitud (dB)')
plt.grid(True, which="both", ls="-", color='0.8')
plt.axvline(100, color='red', linestyle='--', label='Corte teórico (100 kHz)')
plt.legend()

# Ajustamos los límites de la gráfica para ver bien la atenuación
plt.ylim([-100, 5])
plt.xlim([0, 500])

# Mostrar la gráfica en pantalla
plt.show()