import numpy as np
from scipy import misc
import matplotlib.pyplot as plt

face = misc.face(gray=True)

plt.imshow(face > 128, cmap=plt.cm.gray)
plt.savefig('face1.png')
plt.clf()
shiftedface = face/128-1
powerface = np.abs(shiftedface)**2
signface = np.sign(shiftedface)
contrastface = 128*(signface*powerface+1)
plt.imshow(contrastface, cmap=plt.cm.gray)
plt.savefig('face2.png')
plt.clf()
framedface = np.zeros_like(face)
fwidth = 30
framedface[fwidth:-fwidth, fwidth:-fwidth] = face[fwidth:-fwidth, fwidth:-fwidth]
plt.imshow(framedface, cmap=plt.cm.gray)
plt.savefig('face3.png')
plt.clf()
sy, sx = face.shape
y, x = np.ogrid[:sy, :sx]
centerx, centery = 660, 300
mask = ((y-centery)**2+(x-centerx)**2) > 230**2
face[mask] = 0
plt.imshow(face, cmap=plt.cm.gray)
plt.savefig('face4.png')
