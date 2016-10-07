import numpy as np
import math
import timeit
import matplotlib.pyplot as plt

def f_numpy(nmax):
    x = np.linspace(0, np.pi, nmax)
    result = np.sin(x)

def f_math(nmax):
    dx = math.pi/(nmax-1)
    result = [math.sin(n*dx) for n in xrange(nmax)]

x = []
y = []
for n in np.logspace(0.31, 6, 20):
    nint = int(n)
    t_numpy = timeit.timeit("f_numpy(%i)" % nint,
                            "from __main__ import f_numpy",
                            number=20)
    t_math = timeit.timeit("f_math(%i)" % nint,
                            "from __main__ import f_math",
                            number=20)
    x.append(nint)
    y.append(t_math/t_numpy)
plt.plot(x, y)
plt.xscale("log")
plt.savefig("profiling_1.png")
plt.close()
