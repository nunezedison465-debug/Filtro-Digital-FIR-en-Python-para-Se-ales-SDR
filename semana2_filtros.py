import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# Parámetros generales
fs = 1e6            # Frecuencia de muestreo (1 MHz)
taps = 65           # Taps 64 (65)
ventana = 'hamming' # Tipo de ventana

# 1. Filtro Paso Alto (Corte: 200 kHz)
f_corte_hp = 200e3
coeffs_hp = signal.firwin(taps, f_corte_hp, fs=fs, pass_zero=False, window=ventana)

# 2. Filtro Paso Banda (Banda: 150 kHz - 250 kHz)
f_banda = [150e3, 250e3]
coeffs_bp = signal.firwin(taps, f_banda, fs=fs, pass_zero=False, window=ventana)

# Cálculos de respuesta en frecuencia 
w_hp, h_hp = signal.freqz(coeffs_hp, worN=8000)
w_bp, h_bp = signal.freqz(coeffs_bp, worN=8000)
frecuencias = (fs * 0.5 / np.pi) * w_hp

# Configuración de las Gráficas
plt.figure(figsize=(12, 5))

# Gráfica 1: Paso Alto
plt.subplot(1, 2, 1)
plt.plot(frecuencias / 1000, 20 * np.log10(np.abs(h_hp)), 'g', linewidth=2)
plt.title('Semana 2: Filtro Paso Alto (200 kHz)')
plt.xlabel('Frecuencia (kHz)')
plt.ylabel('Amplitud (dB)')
plt.grid(True, which="both", ls="-", color='0.8')
plt.axvline(200, color='red', linestyle='--', label='Corte (200 kHz)')
plt.legend()
plt.ylim([-100, 5])
plt.xlim([0, 500])

# Gráfica 2: Paso Banda
plt.subplot(1, 2, 2)
plt.plot(frecuencias / 1000, 20 * np.log10(np.abs(h_bp)), 'm', linewidth=2)
plt.title('Semana 2: Filtro Paso Banda (150-250 kHz)')
plt.xlabel('Frecuencia (kHz)')
plt.grid(True, which="both", ls="-", color='0.8')
plt.axvline(150, color='red', linestyle='--', label='Inicio (150 kHz)')
plt.axvline(250, color='red', linestyle='--', label='Fin (250 kHz)')
plt.legend()
plt.ylim([-100, 5])
plt.xlim([0, 500])

plt.tight_layout()
plt.show()