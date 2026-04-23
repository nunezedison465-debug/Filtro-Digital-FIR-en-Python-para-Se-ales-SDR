import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# 1. Señal original (Tonos de 50, 200 y 300 kHz)
fs = 1e6
t = np.arange(0, 0.001, 1/fs)
senal = np.cos(2*np.pi*50e3*t) + np.cos(2*np.pi*200e3*t) + np.cos(2*np.pi*300e3*t)

# 2. Diseño de los filtros (¡Usamos 65 taps por ser Paso Alto y Banda!)
taps = 65
coeffs_hp = signal.firwin(taps, 200e3, fs=fs, pass_zero=False, window='hamming')
coeffs_bp = signal.firwin(taps, [150e3, 250e3], fs=fs, pass_zero=False, window='hamming')

# 3. Aplicamos el filtrado a la señal
senal_hp = signal.lfilter(coeffs_hp, 1.0, senal)
senal_bp = signal.lfilter(coeffs_bp, 1.0, senal)

# 4. Calculamos los espectros (FFT)
f = np.fft.fftfreq(len(t), 1/fs)
esp_orig = np.abs(np.fft.fft(senal))
esp_hp = np.abs(np.fft.fft(senal_hp))
esp_bp = np.abs(np.fft.fft(senal_bp))

# 5. Gráfica de 3 paneles para el reporte
plt.figure(figsize=(15, 5))

# Panel 1: Original
plt.subplot(1, 3, 1)
plt.plot(f[:len(f)//2]/1000, esp_orig[:len(esp_orig)//2], 'b')
plt.title('ANTES: Señal Original (3 Tonos)')
plt.xlabel('Frecuencia (kHz)')
plt.xlim([0, 400])
plt.grid(True)

# Panel 2: Paso Alto
plt.subplot(1, 3, 2)
plt.plot(f[:len(f)//2]/1000, esp_hp[:len(esp_hp)//2], 'g', linewidth=2)
plt.title('DESPUÉS: Paso Alto (Corte 200 kHz)')
plt.xlabel('Frecuencia (kHz)')
plt.xlim([0, 400])
plt.grid(True)

# Panel 3: Paso Banda
plt.subplot(1, 3, 3)
plt.plot(f[:len(f)//2]/1000, esp_bp[:len(esp_bp)//2], 'm', linewidth=2)
plt.title('DESPUÉS: Paso Banda (150-250 kHz)')
plt.xlabel('Frecuencia (kHz)')
plt.xlim([0, 400])
plt.grid(True)

plt.tight_layout()
plt.show()