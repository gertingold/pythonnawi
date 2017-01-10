from concurrent import futures
from functools import partial
from itertools import product
import os
import time

import numpy as np
from pyx import canvas, color, deco, path, text, unit

def mandelbrot_tile(nitermax, nx, ny, cx, cy):
    start = time.time()
    x = np.zeros_like(cx)
    y = np.zeros_like(cx)
    data = np.zeros(cx.shape, dtype=np.int)
    for n in range(nitermax):
        x2 = x*x
        y2 = y*y
        notdone = x2+y2 < 4
        data[notdone] = n
        x[notdone], y[notdone] = (x2[notdone]-y2[notdone]+cx[notdone],
                                  2*x[notdone]*y[notdone]+cy[notdone])
    ende = time.time()
    return (nx, ny, os.getpid(), start, ende, data)

def mandelbrot(xmin, xmax, width, ymin, ymax, height,
               npts, ndiv, niter, max_workers=4):
    y, x = np.mgrid[ymin:ymax:height*1j, xmin:xmax:width*1j]
    nlen = npts//ndiv
    clist = [(nx, ny,
              x[nx*nlen:(nx+1)*nlen, ny*nlen:(ny+1)*nlen],
              y[nx*nlen:(nx+1)*nlen, ny*nlen:(ny+1)*nlen])
             for nx, ny in product(range(ndiv), repeat=2)]
    start = time.time()
    ex = futures.ProcessPoolExecutor(max_workers=max_workers)
    wait_for = [ex.submit(partial(mandelbrot_tile, niter), nx, ny, cx, cy)
                for (nx, ny, cx, cy) in clist]
    results = [f.result()[0:5] for f in futures.as_completed(wait_for)]
    ende = time.time()
    processids = sorted(set([r[2] for r in results]))
    processdict = dict(zip(processids, range(len(processids))))
    return (len(processdict), start, ende,
            [(processdict[r[2]], r[3]-start, r[4]-start) for r in results])

npts = 1024
xmin = -2
xmax = 1
width = npts
ymin = -1.5
ymax = 1.5
height = npts
niter = 2000

cnvs = canvas.canvas()
unit.set(wscale=0.8)
cellheight = 0.17

for nr, ndiv in enumerate((2, 4, 8, 16, 32)):
    nrproc, start, ende, data = mandelbrot(xmin, xmax, width, ymin, ymax, height,
                      npts, ndiv, niter)
    offset = -(nrproc+1.2)*cellheight*nr
    cnvs.text(-0.2, offset+2*cellheight, "$n=%s$" % ndiv,
              [text.halign.right, text.valign.middle])
    cnvs.stroke(path.line(0, -0.2*cellheight+offset, 0,
        (nrproc+0.2)*cellheight+offset))
    cnvs.stroke(path.line(ende-start, -0.2*cellheight+offset, ende-start,
        (nrproc+0.2)*cellheight+offset))
    for d in data:
        colours = color.hsb(0.667*d[0]/(nrproc-1), 1, 0.3)
        colourf = color.hsb(0.667*d[0]/(nrproc-1), 0.2, 1)
        cnvs.stroke(path.rect(d[1], d[0]*cellheight+offset, (d[2]-d[1]), 0.8*cellheight),
                [colours, deco.filled([colourf])])

cnvs.writePDFfile()
cnvs.writeGSfile(device="png16m", resolution=600)
