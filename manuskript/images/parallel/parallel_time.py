from concurrent import futures
from functools import partial
from itertools import product
import os
import time

import numpy as np
from pyx import color, deco, graph, style

def mandelbrot_iteration(niter, nx, ny, c):
    start = time.time()
    z = np.zeros_like(c)
    result = np.zeros(c.shape, dtype=int)
    for n in range(niter):
        notdone = np.abs(z) < 2
        result[notdone] = n
        z[notdone] = z[notdone]**2+c[notdone]
    ende = time.time()
    return (nx, ny, os.getpid(), start, ende, result)

def mandelbrot(xmin, xmax, width, ymin, ymax, height,
               npts, ndiv, niter, max_workers=4):
    y, x = np.ogrid[ymin:ymax:height*1j, xmin:xmax:width*1j]
    c = x+1j*y
    nlen = npts//ndiv
    clist = [(nx, ny, c[nx*nlen:(nx+1)*nlen, ny*nlen:(ny+1)*nlen])
             for nx, ny in product(range(ndiv), repeat=2)]
    start = time.time()
    ex = futures.ProcessPoolExecutor(max_workers=max_workers)
    wait_for = [ex.submit(partial(mandelbrot_iteration, niter), nx, ny, c)
                for (nx, ny, c) in clist]
    results = [f.result()[0:5] for f in futures.as_completed(wait_for)]
    ende = time.time()
    processids = sorted(set([r[2] for r in results]))
    processdict = dict(zip(processids, range(len(processids))))
    return (len(processdict), start, ende,
            [(processdict[r[2]], r[3]-start, r[4]-start) for r in results])

npts = 2048
xmin = -2
xmax = 1
width = npts
ymin = -1.5
ymax = 1.5
height = npts
niter = 2000

data = []
for nr, ndiv in enumerate((1, 2, 4, 8, 16, 32, 64, 128, 256, 512)):
    nrproc, start, ende, result = mandelbrot(xmin, xmax, width, ymin, ymax, height,
                      npts, ndiv, niter)
    print(ndiv, ende-start)
    data.append((ndiv, ende-start))

acceleration = [(ndiv, data[0][1]/d) for ndiv, d in data]

logparter = graph.axis.parter.log(tickpreexps=
                [graph.axis.parter.preexp([graph.axis.tick.rational(1, 1)], 2)])
g = graph.graphxy(width=8,
        x=graph.axis.log(min=data[0][0], max=data[-1][0], parter=logparter,
                         title='Unterteilungen einer Achse'),
        y=graph.axis.lin(min=0, max=4, title='Beschleunigung'))
g.plot(graph.data.points(acceleration, x=1, y=2),
        [graph.style.line(lineattrs=[style.linestyle.dotted]),
	 graph.style.symbol(symbol=graph.style.symbol.circle,
			    size=0.1, symbolattrs=[deco.filled([color.grey(1)])])
	])
g.writePDFfile()
g.writeGSfile(device="png16m", resolution=600)
