from pyx import color, deco, graph, style

with open('numba_parallel.dat') as fh:
    t_cpu = float(fh.readline().rstrip('\n').split()[1])
    t_parallel = []
    for _ in range(8):
        elems = fh.readline().rstrip('\n').split()
        t_parallel.append((int(elems[0]), float(elems[1])))
t_parallel = [(n, t_cpu/t) for n, t in t_parallel]

g = graph.graphxy(width=8,
        x=graph.axis.linear(min=1, max=8, title="Zahl der Threads"),
        y=graph.axis.linear(title="Beschleunigung"))
g.plot(graph.data.points(t_parallel, x=1, y=2),
       [graph.style.line([style.linestyle.dotted]),
        graph.style.symbol(symbol=graph.style.symbol.circle,
                           size=0.1,
                           symbolattrs=[deco.filled([color.grey(1)])])
       ])
g.writePDFfile()
g.writeGSfile(device="png16m", resolution=600)
