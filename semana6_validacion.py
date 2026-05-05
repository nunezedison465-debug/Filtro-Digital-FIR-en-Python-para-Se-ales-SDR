import numpy as np
import scipy.signal as signal

# Parámetros del sistema
fs = 1e6
f_tonos = [50e3, 200e3, 300e3]

# Diseños de los filtros (64 taps para LPF, 65 para HPF/BPF por Nyquist)
lpf = signal.firwin(64, 100e3, fs=fs, window='hamming')
hpf = signal.firwin(65, 200e3, fs=fs, pass_zero=False, window='hamming')
bpf = signal.firwin(65, [150e3, 250e3], fs=fs, pass_zero=False, window='hamming')

filtros = {'Paso Bajo (100 kHz)': lpf, 'Paso Alto (200 kHz)': hpf, 'Paso Banda (150-250 kHz)': bpf}

print("\n" + "="*50)
print(" RESULTADOS DE VALIDACIÓN EXPERIMENTAL ")
print("="*50)

for nombre, coefs in filtros.items():
    # Calcular respuesta en frecuencia teórica
    w, h = signal.freqz(coefs, worN=8000, fs=fs)
    mag_db = 20 * np.log10(np.abs(h) + 1e-12)
    
    print(f"\n[ Filtro: {nombre} ]")
    print("-" * 30)
    
    # 1. Medición en los tonos de prueba
    for f in f_tonos:
        idx = np.argmin(np.abs(w - f)) # Buscar la frecuencia más cercana
        ganancia = mag_db[idx]
        estado = "PASA" if ganancia > -3 else "ATENUADO"
        print(f"  Ganancia a {int(f/1000)} kHz: {ganancia:>6.2f} dB ({estado})")
        
    # 2. Validación de métricas de la Rúbrica
    if 'Bajo' in nombre:
        idx_pass = w <= 80e3
        idx_stop = w >= 150e3
    elif 'Alto' in nombre:
        idx_pass = w >= 220e3
        idx_stop = w <= 150e3
    else: # Banda
        idx_pass = (w >= 170e3) & (w <= 230e3)
        idx_stop = (w <= 100e3) | (w >= 300e3)
        
    # Calcular Ripple (diferencia max-min en banda de paso)
    ripple = np.max(mag_db[idx_pass]) - np.min(mag_db[idx_pass])
    # Calcular Atenuación máxima (el peor caso en la banda de rechazo)
    atenuacion = np.max(mag_db[idx_stop])
    
    print("-" * 30)
    print(f"  Ripple Passband:   {ripple:.4f} dB (Objetivo: < 1 dB)")
    print(f"  Atenuación Stop:  {atenuacion:.2f} dB (Objetivo: > -40 dB)")
print("="*50 + "\n")