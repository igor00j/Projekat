import numpy as np
import scipy.io.wavfile as wav
import cProfile
import pstats
import math
import os

# Ova funkcija radi ISTO sto i numpy, ali SPORO (jedan po jedan broj)
# Ovo simulira cisto procesorsko opterecenje bez vektorskih instrukcija.
def hardverska_simulacija_sinus(t_array, freq):
    # Rucno racunanje sinusa za svaki uzorak
    return [math.sin(2 * math.pi * freq * t) for t in t_array]

def hardverska_simulacija_mnozenje(data, carrier):
    # Rucno mnozenje dva niza
    result = []
    for i in range(len(data)):
        result.append(data[i] * carrier[i])
    return result

def run_profiling_simulation(input_file):
    if not os.path.exists(input_file):
        print("Nema fajla!")
        return

    # Učitavanje
    fs, data = wav.read(input_file)
    if len(data.shape) > 1: data = data[:, 0]
    
    # Smanjicemo broj uzoraka da ne cekas predugo (jer je ovo sporo!)
    # Uzimamo samo prvih 10.000 uzoraka za test
    data = data[:10000]
    data_float = data.astype(np.float64)
    t = np.arange(len(data)) / fs 
    
    print("--- POKRECEM SIMULACIJU OPTERECENJA (Cekaj...) ---")
    
    # === OVDE CE SE VIDETI OPTERECENJE ===
    # 1. Generisanje sinusa (Simulacija DDS-a)
    carrier = hardverska_simulacija_sinus(t, 450)
    
    # 2. Mnozenje (Simulacija DSP Mnozaca)
    output = hardverska_simulacija_mnozenje(data_float, carrier)
    
    print("Simulacija gotova.")

if __name__ == "__main__":
    ulaz = 'input.wav'
    
    profiler = cProfile.Profile()
    profiler.enable()
    run_profiling_simulation(ulaz)
    profiler.disable()
    
    stats = pstats.Stats(profiler).sort_stats('tottime')
    
    print("\nREZULTATI KOJE TRAZIS ZA DOKUMENTACIJU:")
    print("Trazis funkcije: 'hardverska_simulacija_sinus' i 'hardverska_simulacija_mnozenje'")
    print("-----------------------------------------------------------------------------")
    stats.print_stats(10)