import numpy as np
import adi
import scipy.signal as signal
import matplotlib.pyplot as plt

# 1. SDR Pluto
sdr = adi.Pluto('ip:192.168.2.1')
sdr.sample_rate = int(1e6)
sdr.rx_lo = int(900e6)
sdr.rx_buffer_size = 10000

# 2. Capturar señal multi-tono 
print("Capturando señal para comparación...")
for _ in range(10): sdr.rx() # Limpieza
rx_data = sdr.rx()

# 3. Procesar con diferentes órdenes (32, 64, 128)
fs = sdr.sample_rate
f_corte = 100e3
ordenes = [32, 64, 128]
colores = ['g', 'b', 'r'] # Verde, Azul, Rojo

plt.figure(figsize=(10, 6))

# Calculos FFT de la señal original para referencia
N = len(rx_data)
frecuencias = np.fft.fftfreq(N, 1/fs)[:N//2]
mag_orig = np.abs(np.fft.fft(rx_data))[:N//2] / N
plt.plot(frecuencias/1000, 20*np.log10(mag_orig + 1e-9), color='gray', alpha=0.3, label='Original (Sucia)')

# Bucle para aplicar y graficar cada filtro
for tap, color in zip(ordenes, colores):
    # Diseño del filtro
    # Nota: Usamos taps impares (tap+1) para evitar el error de Nyquist en Paso Alto si decidieras cambiarlo
    taps_ajustados = tap + 1 
    coefs = signal.firwin(taps_ajustados, f_corte, fs=fs, window='hamming')
    
    # Aplicar filtro
    filtrada = signal.lfilter(coefs, 1.0, rx_data)
    
    # Calcular Espectro en dB
    mag_db = 20 * np.log10(np.abs(np.fft.fft(filtrada))[:N//2] / N + 1e-9)
    
    plt.plot(frecuencias/1000, mag_db, color=color, label=f'Orden: {tap} taps')

# 4. Configuración de la Gráfica
plt.title('Comparación de Órdenes de Filtro FIR (32 vs 64 vs 128 Taps)')
plt.xlabel('Frecuencia (kHz)')
plt.ylabel('Magnitud (dB)')
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.xlim([0, 400])
plt.ylim([-100, 0]) # Atenuación en dB
plt.tight_layout()

print("Gráfica generada. Revisa la atenuación en la banda de parada.")
plt.show()