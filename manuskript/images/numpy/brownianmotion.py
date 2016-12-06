import numpy as np
import matplotlib.pyplot as plt

stories = 50
length = 10000
jumps = np.random.choice(np.array([-1, 1]), size=(length, stories))
trajectories = np.cumsum(jumps, axis=0)
plt.xlabel('$t$', fontsize=20)
plt.ylabel('$x$', fontsize=20)
plt.plot(trajectories)
plt.savefig('brownianmotion1.png')
plt.clf()
plt.xlabel('$t$', fontsize=20)
plt.ylabel(r'$\langle x\rangle$', fontsize=20)
plt.plot(np.mean(trajectories, axis=1))
plt.savefig('brownianmotion2.png')
plt.clf()
plt.xlabel('$t$', fontsize=20)
plt.ylabel(r'$\langle x^2\rangle-\langle x\rangle^2$', fontsize=20)
plt.plot(np.var(trajectories, axis=1))
plt.savefig('brownianmotion3.png')
