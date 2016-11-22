import sys
import os.path

from pyx import canvas, color, deco, path, text, trafo, unit

def make_stride_figure(lowerstride, uperstride=1, nrentries=6):
    c = canvas.canvas()
    ht = 0.5
    wd = 2
    dist = 0.2
    textcolor = color.hsb(0.02, 1, 0.6)
    for n in range(nrentries):
        x = n*(wd+dist)
        c.stroke(path.rect(x, 0, wd, ht))
        c.text(x+0.5*wd, 0.5*ht, str(n), [text.halign.center, text.valign.middle])

    for n in range(nrentries-1):
        x = n*(wd+dist)
        c.stroke(path.curve(x-dist/3, ht+0.5*dist,
                            x+0.3*wd, ht+3*dist,
                            x+0.7*wd, ht+3*dist,
                            x+wd+dist/3, ht+0.5*dist),
                 [deco.earrow.large])
        c.text(x+0.5*wd, ht+3.2*dist, r'\Large 8', [text.halign.center, textcolor])

    if lowerstride:
        for n in range((nrentries-1)//lowerstride):
            x = n*lowerstride*(wd+dist)
            c.stroke(path.curve(x-dist/3, -0.5*dist,
                                x+0.5*wd, -5*dist,
                                x+(lowerstride-0.5)*wd+lowerstride*dist, -5*dist,
                                x+lowerstride*wd+(lowerstride-0.7)*dist, -0.5*dist),
                     [deco.earrow.large])
            c.text(x+0.5*lowerstride*wd+dist,-5.2*dist, r'\Large %i' % (lowerstride*8),
                   [text.halign.center, text.valign.top, textcolor])
    return c

text.set(text.LatexRunner)
text.preamble(r'\usepackage{arev}\usepackage[T1]{fontenc}\usepackage{amsmath}')
unit.set(xscale=1.2, wscale=1.5)

c = canvas.canvas()
c.insert(make_stride_figure(0), [trafo.translate(0, 9)])
c.text(0, 11.3, r"\Large(8,)", [color.rgb(0, 0, 0.8)])
c.text(-2, 9.5, r"\Large $\begin{pmatrix}0 & 1 & 2 & 3 & 4 & 5\end{pmatrix}$",
       [text.halign.right, text.valign.middle])
c.insert(make_stride_figure(3), [trafo.translate(0, 5)])
c.text(0, 7.3, r"\Large(24, 8)", [color.rgb(0, 0, 0.8)])
c.text(-2, 5.5, r"\Large $\begin{pmatrix}0 & 1 & 2 \\ 3 & 4 & 5\end{pmatrix}$",
       [text.halign.right, text.valign.middle])
c.insert(make_stride_figure(2), [trafo.translate(0, 0)])
c.text(0, 2.3, r"\Large(16, 8)", [color.rgb(0, 0, 0.8)])
c.text(-2, 0.5, r"\Large $\begin{pmatrix}0 & 1 \\ 2 & 3 \\ 4 & 5\end{pmatrix}$",
       [text.halign.right, text.valign.middle])
c.writePDFfile()
c.writeGSfile(device="png16m", resolution=600)
