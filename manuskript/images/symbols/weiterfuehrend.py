# *-* coding: utf-8 *-*
import sys, os
sys.path.insert(0, os.path.expanduser('~/PyX-0.10'))
from pyx import *

text.set(mode="latex")
c = canvas.canvas()
t = text.text(0, 0, r"\sffamily\bfseries +")
tblarge = t.bbox().enlarged(0.1)
c.fill(tblarge.path(), [color.rgb(0,0.8,0)])
c.insert(t, [color.grey(1)])
basefilename = os.path.splitext(sys.argv[0])[0]
c.writePDFfile(basefilename)
c.pipeGS("%s.png" % basefilename, resolution=600)
