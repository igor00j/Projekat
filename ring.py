import numpy as np
import scipy.io.wavfile as wav
import os

def ring_modulator(input_file, output_file, mod_freq=300):
   
    if not os.path.exists(input_file):
        print(f"Greška: Ulazni fajl '{input_file}' nije pronađen.")
        return

    try:
        fs, data = wav.read(input_file)
    except Exception as e:
        print("Greška pri učitavanju fajla: {e}")
        return

    if len(data.shape) > 1:
        data = data[:, 0]

    max_val = np.iinfo(data.dtype).max
    data_float = data.astype(np.float64) / max_val
    
    print(f"Učitan fajl: {input_file}")
    print(f"Frekvencija uzorkovanja (fs): {fs} Hz")
    print(f"Frekvencija modulacije (f_mod): {mod_freq} Hz")
    print(f"Ukupno uzoraka: {len(data)}")

    t = np.arange(len(data)) / fs 
    
    carrier = np.sin(2 * np.pi * mod_freq * t)
    
    output_float = data_float * carrier
    
    output_int16 = np.int16(output_float * max_val)

    wav.write(output_file, fs, output_int16)
    print(f"Obrada uspešno završena. Rezultat sačuvan u: {output_file}")

if __name__ == "__main__":
    
    ulaz = 'input.wav'
    izlaz = 'output.wav'

    ring_modulator(ulaz, izlaz, mod_freq=300)
    


