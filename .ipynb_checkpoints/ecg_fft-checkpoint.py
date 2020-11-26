import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import scipy.fftpack

if len(sys.argv) != 2:
    sys.exit('invalid command\nproper usage: ecg_sampling.py [file_name.npz]')

filename = sys.argv[1]
try:
    d = np.load(filename)
except:
    sys.exit('cannot find the ecg data file')

f = 360

ecg = d['ecg']
peaks, _ = scipy.signal.find_peaks(ecg, height=0.65)
n = ecg.shape[0]
t = np.arange(n)/f


ecg_fft = scipy.fftpack.fft(ecg)
ecg_fft_roll = np.roll(ecg_fft, n//2)
ecg_freq = scipy.fftpack.fftfreq(n, 1/f)
ecg_freq_roll = np.roll(ecg_freq, n//2)

fig, axes = plt.subplots(1, 2, figsize=(10,5))
axes[0].plot(t, ecg)
axes[0].set_title('ecg plot (sampling rate: 360 Hz)')
axes[1].plot(ecg_freq_roll, np.abs(ecg_fft_roll))
axes[1].set_ylim(bottom=0, top=30)
#axes[1].set_xlim(left=-180, right=180)
axes[1].set_title('fft result')

plt.show()