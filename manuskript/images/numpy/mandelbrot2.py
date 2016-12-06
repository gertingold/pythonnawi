import numpy as np
import matplotlib.pyplot as plt

niter = 200
npts = 1000
xmin = -0.68
xmax = -0.66
ymin = 0.45
ymax = 0.47
y, x = np.ogrid[ymax:ymin:npts*1j, xmin:xmax:npts*1j]
c = x+1j*y
z = np.zeros_like(c)
output = np.zeros(c.shape, dtype=np.int)
for n in range(niter):
    notdone = np.abs(z) < 2
    output[notdone] = n
    z[notdone] = z[notdone]**2+c[notdone]
plt.imshow(output, extent=(xmin, xmax, ymin, ymax),
           cmap='Paired', interpolation='none')
plt.xlabel('$\mathrm{Re}(c)$', fontsize=20)
plt.ylabel('$\mathrm{Im}(c)$', fontsize=20)
plt.savefig('mandelbrot2.png')
