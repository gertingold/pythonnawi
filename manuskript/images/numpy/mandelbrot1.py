import numpy as np
import matplotlib.pyplot as plt

niter = 2000
npts = 1000
y, x = np.ogrid[-1.5:1.5:npts*1j, -2:1:npts*1j]
c = x+1j*y
z = c
for n in range(niter):
    z = z**2+c
imdata = np.abs(z) < 2
plt.imshow(imdata, extent=(-2, 1, -1.5, 1.5),
           cmap='gray', interpolation='none')
plt.xlabel('$\mathrm{Re}(c)$', fontsize=20)
plt.ylabel('$\mathrm{Im}(c)$', fontsize=20)
plt.savefig('mandelbrot1.png')
