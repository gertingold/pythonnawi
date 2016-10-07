import numpy as np
import numexpr as ne
import timeit
import matplotlib.pyplot as plt

def f_numpy(nmax):
    x = np.linspace(0, 1, nmax)
    result = ((5*x-2)*x+1)*x-7

def f_numexpr(nmax):
    x = np.linspace(0, 1, nmax)
    result = ne.evaluate("5*x**3-2*x**2+x-7")

x = []
y = []
for n in np.logspace(0.31, 6, 20):
    nint = int(n)
    print nint
    t_numpy = timeit.timeit("f_numpy(%i)" % nint,
                            "from __main__ import f_numpy",
                            number=20)
    t_numexpr = timeit.timeit("f_numexpr(%i)" % nint,
                            "from __main__ import f_numexpr",
                            number=20)
    x.append(nint)
    y.append(t_numpy/t_numexpr)
plt.plot(x, y)
plt.xscale("log")
plt.savefig("profiling_2.png")
plt.close()
