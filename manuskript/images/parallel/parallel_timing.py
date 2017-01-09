from concurrent import futures
from itertools import product
from functools import partial
import time

import numpy as np

def mandelbrot_tile(nitermax, nx, ny, cx, cy):
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
    return (nx, ny, data)

def mandelbrot(xmin, xmax, ymin, ymax, npts, nitermax, ndiv, max_workers=4):
    start = time.time()
    cy, cx = np.mgrid[ymin:ymax:npts*1j, xmin:xmax:npts*1j]
    nlen = npts//ndiv
    paramlist = [(nx, ny,
                  cx[nx*nlen:(nx+1)*nlen, ny*nlen:(ny+1)*nlen],
                  cy[nx*nlen:(nx+1)*nlen, ny*nlen:(ny+1)*nlen])
                 for nx, ny in product(range(ndiv), repeat=2)]
    with futures.ProcessPoolExecutor(max_workers=max_workers) as executors:
        wait_for = [executors.submit(partial(mandelbrot_tile, nitermax),
                                             nx, ny, cx, cy)
                    for (nx, ny, cx, cy) in paramlist]
        results = [f.result() for f in futures.as_completed(wait_for)]
    data = np.zeros(cx.shape, dtype=np.int)
    for nx, ny, result in results:
        data[nx*nlen:(nx+1)*nlen, ny*nlen:(ny+1)*nlen] = result
    return time.time()-start

def mandelbrot_single(xmin, xmax, ymin, ymax, npts, nitermax, ndiv):
    start = time.time()
    cy, cx = np.mgrid[ymin:ymax:npts*1j, xmin:xmax:npts*1j]
    nlen = npts//ndiv
    paramlist = [(nx, ny,
                  cx[nx*nlen:(nx+1)*nlen, ny*nlen:(ny+1)*nlen],
                  cy[nx*nlen:(nx+1)*nlen, ny*nlen:(ny+1)*nlen])
                 for nx, ny in product(range(ndiv), repeat=2)]
    data = np.zeros(cx.shape, dtype=np.int)
    for nx, ny, cx, cy in paramlist:
        nx, ny, result = mandelbrot_tile(nitermax, nx, ny, cx, cy)
        data[nx*nlen:(nx+1)*nlen, ny*nlen:(ny+1)*nlen] = result
    return time.time()-start

nitermax = 2000
npts = 1024
xmin = -2
xmax = 1
ymin = -1.5
ymax = 1.5

for ndiv in (1, 2, 4, 8, 16, 32, 64, 128,):
    t1 = mandelbrot_single(xmin, xmax, ymin, ymax, npts, nitermax, ndiv)
    t4 = mandelbrot(xmin, xmax, ymin, ymax, npts, nitermax, ndiv)
    print(ndiv, t1, t4)
