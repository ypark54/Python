import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq, ifft
l = 100
n = 10000
x = np.linspace(0, l, n)

print(x)

y1 = np.cos(2*np.pi*x)+4*np.sin(3*np.pi*x)
freqs = fftfreq(n)

plt.figure(1)
plt.plot(x,y1)
#plt.show()

result = fft(y1)

#print(result)

plt.figure(2)
plt.plot(freqs*2*n/l, 2*np.abs(result)/n)
plt.show()
print(np.max(2*np.abs(result)/n))