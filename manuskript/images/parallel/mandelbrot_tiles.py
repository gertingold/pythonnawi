from concurrent import futures
from functools import partial
from itertools import product
import os
import numpy as np
from pyx import color, deco, graph, path

def mandelbrot_iteration(niter, *args):
    nx, ny, c = args[0]
    z = np.zeros_like(c)
    for n in range(niter):
        z = z**2+c
    return nx, ny, os.getpid(), np.abs(z) < 2

npts = 1024
xmin = -2
xmax = 1
width = npts
ymin = -1.5
ymax = 1.5
height = npts
niter = 2000

y, x = np.ogrid[ymin:ymax:height*1j, xmin:xmax:width*1j]
c = x+1j*y

nexponent = 2
n = 2**nexponent
nlen = npts//n
clist = []
for nx, ny in product(range(n), repeat=2):
    clist.append((nx, ny, c[nx*nlen:(nx+1)*nlen, ny*nlen:(ny+1)*nlen]))
ex = futures.ProcessPoolExecutor(max_workers=4)
results = list(ex.map(partial(mandelbrot_iteration, niter), clist))

data = []
procdict = {}
for r in results:
    nx, ny, procid, partialdata = r
    for mx, my in product(range(nlen), repeat=2):
        cval = c[nx*nlen+mx, ny*nlen+my]
        data.append((cval.real, cval.imag, partialdata[mx, my]))
    procdict[(nx, ny)] = procid
procids = set(procdict.values())
colors = [color.hsb(n/(len(procids)-1)*0.67, 1, 1) for n in range(len(procids))]
proccolors = dict(zip(procids, colors))

g = graph.graphxy(width=8, height=8,
        x=graph.axis.lin(),
        y=graph.axis.lin())
g.plot(graph.data.points(data, x=1, y=2, color=3),
       [graph.style.density(keygraph=None)])

dx = (xmax-xmin)/n
dy = (ymax-ymin)/n
for k, v in procdict.items():
    nx, ny = k
    tilecolor = proccolors[v]
    xll, yll = g.pos(xmin+dx*nx, ymin+dy*ny)
    xur, yur = g.pos(xmin+dx*(nx+1), ymin+dy*(ny+1))
    g.fill(path.rect(xll, yll, xur-xll, yur-yll),
           [deco.stroked([color.grey(0)]), tilecolor, color.transparency(0.5)])
g.writePDFfile()
