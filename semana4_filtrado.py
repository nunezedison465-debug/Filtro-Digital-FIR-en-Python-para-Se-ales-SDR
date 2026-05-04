import numpy as np
import adi
import scipy.signal as signal
import matplotlib.pyplot as plt

# 1. Configurar el SDR para Recepción (Escuchar)
sdr = adi.Pluto('ip:192.168.2.1')
sdr.sample_rate = int(1e6)
sdr.rx_lo = int(900e6) # Sintonizamos la misma frecuencia que la transmisión
sdr.rx_rf_bandwidth = int(1e6)
sdr.rx_buffer_size = 10000 
sdr.rx_hardwaregain_chan0 = "slow_attack"

# 2. ¡Capturar la señal real del aire!
print("Capturando señal del aire...")
for i in range(10): # Limpiamos basura inicial
    rx_data = sdr.rx()
rx_data = sdr.rx()

# 3. Diseño del Filtro Paso Bajo (100 kHz)
fs = sdr.sample_rate
f_corte = 100e3
taps = 64
coeficientes = signal.firwin(taps, f_corte, fs=fs, window='hamming')

# 4. Filtrar la señal capturada
senal_filtrada = signal.lfilter(coeficientes, 1.0, rx_data)

# 5. Calcular la FFT
def calcular_fft(senal, fs):
    N = len(senal)
    espectro = np.fft.fft(senal)
    frecuencias = np.fft.fftfreq(N, 1/fs)
    magnitud = np.abs(espectro) / N
    mitad = N // 2
    return frecuencias[:mitad], magnitud[:mitad]

f_orig, mag_orig = calcular_fft(rx_data, fs)
f_filt, mag_filt = calcular_fft(senal_filtrada, fs)

# 6. Gráficas del Antes y Después
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(f_orig / 1000, mag_orig, 'b')
plt.title('ANTES: Señal Recibida por la Antena')
plt.xlabel('Frecuencia (kHz)')
plt.xlim([0, 400])
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(f_filt / 1000, mag_filt, 'r', linewidth=2)
plt.title('DESPUÉS: Filtrada (Paso Bajo 100 kHz)')
plt.xlabel('Frecuencia (kHz)')
plt.xlim([0, 400])
plt.grid(True)

plt.tight_layout()
plt.show()