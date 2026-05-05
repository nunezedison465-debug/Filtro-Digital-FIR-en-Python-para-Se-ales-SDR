import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la señal
fs = 1e6 
t = np.arange(0, 0.001, 1/fs) # 1 milisegundo de tiempo

# Generamos los tres tonos
tono1 = np.cos(2 * np.pi * 50e3 * t)
tono2 = np.cos(2 * np.pi * 200e3 * t)
tono3 = np.cos(2 * np.pi * 300e3 * t)

# Mezclamos todo en una sola señal
senal = tono1 + tono2 + tono3

# Calculamos el espectro de frecuencia usando FFT
f = np.fft.fftfreq(len(t), 1/fs)
espectro = np.abs(np.fft.fft(senal))

# Gráfica
plt.figure(figsize=(10, 5))
plt.plot(f[:len(f)//2]/1000, espectro[:len(espectro)//2], 'b', linewidth=1.5)
plt.title('Semana 3: Espectro de la Señal Multi-tono')
plt.xlabel('Frecuencia (kHz)')
plt.ylabel('Magnitud')
plt.grid(True, which="both", ls="-", color='0.8')

# Marcamos los tonos esperados
plt.axvline(50, color='red', linestyle='--', alpha=0.7)
plt.axvline(200, color='red', linestyle='--', alpha=0.7)
plt.axvline(300, color='red', linestyle='--', alpha=0.7)

plt.xlim([0, 400])
plt.show()