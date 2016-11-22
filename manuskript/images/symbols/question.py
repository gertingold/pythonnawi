from pyx import canvas, color, text

text.set(text.LatexRunner)
c = canvas.canvas()
t = text.text(0, 0, r"\sffamily\bfseries ?")
tblarge = t.bbox().enlarged(0.1)
c.fill(tblarge.path(), [color.rgb(0.8, 0.5, 0)])
c.insert(t, [color.grey(1)])

c.writePDFfile()
c.writeGSfile(device="png16m", resolution=600)
