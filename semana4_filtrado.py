import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# 1. Recreamos la señal original (3 tonos)
fs = 1e6
t = np.arange(0, 0.001, 1/fs)
senal = np.cos(2*np.pi*50e3*t) + np.cos(2*np.pi*200e3*t) + np.cos(2*np.pi*300e3*t)

# 2. Recreamos el Filtro Paso Bajo (Corte: 100 kHz)
taps = 64 
f_corte = 100e3
coeffs_lpf = signal.firwin(taps, f_corte, fs=fs, window='hamming')

# 3. ¡EL FILTRADO! Aplicamos el filtro a la señal
senal_filtrada = signal.lfilter(coeffs_lpf, 1.0, senal)

# 4. Calculamos los espectros (FFT) para comparar
f = np.fft.fftfreq(len(t), 1/fs)
espectro_original = np.abs(np.fft.fft(senal))
espectro_filtrado = np.abs(np.fft.fft(senal_filtrada))

# 5. Configuramos la gráfica comparativa
plt.figure(figsize=(12, 5))

# Gráfica Izquierda: Antes del filtro
plt.subplot(1, 2, 1)
plt.plot(f[:len(f)//2]/1000, espectro_original[:len(espectro_original)//2], 'b')
plt.title('ANTES: Señal Original (3 Tonos)')
plt.xlabel('Frecuencia (kHz)')
plt.grid(True)
plt.xlim([0, 400])

# Gráfica Derecha: Después del filtro
plt.subplot(1, 2, 2)
plt.plot(f[:len(f)//2]/1000, espectro_filtrado[:len(espectro_filtrado)//2], 'r', linewidth=2)
plt.title('DESPUÉS: Filtrada (Paso Bajo 100 kHz)')
plt.xlabel('Frecuencia (kHz)')
plt.grid(True)
plt.xlim([0, 400])

plt.tight_layout()
plt.show()