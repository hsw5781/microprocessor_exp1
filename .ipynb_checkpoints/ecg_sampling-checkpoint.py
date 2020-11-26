import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import time

if len(sys.argv) != 3:
    sys.exit('invalid command\nproper usage: ecg_sampling.py [file_name.npz] [sampling_rate]')

filename = sys.argv[1]
try:
    d = np.load(filename)
except:
    sys.exit('no such file')

try:
    fs = int(sys.argv[2])
except:
    sys.exit('sampling rate is not valid, integer type required')

if fs > 360 or fs < 0:
    sys.exit('sampling rate is not valid, 0<fs<360')
f = 360

ecg = d['ecg']
peaks, _ = scipy.signal.find_peaks(ecg, height=0.65, distance=f*0.4)
n = ecg.shape[0]
t = np.arange(n)/f

ecg_resamp = scipy.signal.resample(ecg, int(np.floor(n*fs/f)))
ts = time.time()
peaks_resamp, _ = scipy.signal.find_peaks(ecg_resamp, height=0.65, distance=fs*0.4)
tf = time.time()
t_resamp = np.arange(ecg_resamp.shape[0])/fs

print('data size: {}, processing time: {:.3f}'.format(ecg_resamp.itemsize*ecg_resamp.size, (tf-ts)*100000))

fig, axes = plt.subplots(1, 2, figsize=(10,5))
axes[0].plot(t, ecg)
axes[0].plot(t[peaks], ecg[peaks], 'ro')
axes[0].set_title('original ecg')

axes[1].plot(t_resamp, ecg_resamp)
axes[1].plot(t_resamp[peaks_resamp], ecg_resamp[peaks_resamp], 'ro')
axes[1].set_title('resampled ecg ({}Hz)'.format(fs))
for peak in peaks_resamp:
    axes[1].annotate('{:.2f}'.format(t_resamp[peak]),
                (t_resamp[peak], ecg_resamp[peak]))
if peaks_resamp.shape != peaks.shape:
    axes[1].text(x=0, y=np.min(ecg_resamp), s='R detection failed',
                fontsize='large', c='r')
plt.show()