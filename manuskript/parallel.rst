===============================
Aspekte des parallelen Rechnens
===============================

Bereits in normalen Rechnern sind heutzutage CPUs verbaut, die mehrere
Rechenkerne enthalten. Da man es gerade beim numerischen Rechnen immer
wieder mit Problemen zu tun hat, bei denen sich Aufgaben parallel erledigen
lassen, stellt sich die Frage, wie man in Python diese Parallelverarbeitung
realisieren und mehrere Rechenkerne gleichzeitig beschäftigen kann. Damit
ließe sich die Ausführung des Programms entsprechend beschleunigen. Dies
gilt umso mehr als oft auch Rechencluster zur Verfügung stehen, die viele
CPUs enthalten und es erlauben, die numerische Arbeit auf viele Rechenkerne
zu verteilen.

Im Zusammenhang mit dem parallelen Rechnen ist zu beachten, dass Python
einen sogenannten *Global Interpreter Lock* (GIL) besitzt, der verhindert,
dass im Rahmen eines einzigen Python-Prozesses eine echte Parallelverarbeitung
realisiert werden kann. Auf diese Problematik werden wir im nächsten Abschnitt
eingehen.

Trotz des GIL ist eine Parallelverarbeitung möglich, wenn mehrere
Prozesse gestartet werden. Wie dies in Python realisiert wird, werden wir
uns im Abschnitt :ref:`parallelverarbeitung` am konkreten Beispiel der
Berechnung der Mandelbrotmenge ansehen. Dieses Problem zeichnet sich dadurch
aus, dass die parallel zu bearbeitenden Teilaufgaben unabhängig voneinander
sind, so dass während der Bearbeitung keine Kommunikation, also zum Beispiel
Austausch von Daten, erforderlich ist. Man spricht dann von einem
Problem, das *embarrassingly parallel* ist. Wir wollen uns auf diese Klasse
von Problemen beschränken, da die Kommunikation zwischen verschiedenen
Prozessen bei der Parallelverarbeitung eine Reihe von Problemen aufwirft,
deren Diskussion hier den Rahmen sprengen würde.

Im letzten Abschnitt werden wir noch auf Numba eingehen, das schon als
sogenannter *Just in Time Compiler* (JIT Compiler) zu einer Beschleunigung
der Programmausführung führt. Zusätzlich kann Numba aber auch die
parallele Abarbeitung von Python-Skripten unterstützen.

-----------------------------
Threads, Prozesse und der GIL
-----------------------------

Moderne Betriebssysteme erlauben es selbst auf nur einem Rechenkern,
verschiedene Vorgänge scheinbar parallel ablaufen zu lassen. Dies geschieht
dadurch, dass diese Vorgänge abwechselnd Rechenzeit zugewiesen bekommen,
so dass ein einzelner Vorgang normalerweise nicht die Ausführung der anderen
Vorgänge über eine längere Zeit blockieren kann. 

Dabei muss man zwei Arten von Vorgängen unterscheiden, nämlich Prozesse und
Threads. Prozesse verfügen jeweils über ihren eigenen reservierten
Speicherbereich und über einen eigenen Zugang zu Systemressourcen. Dies
bedeutet aber auch, dass das Starten eines Prozesses mit einem gewissen
Aufwand verbunden ist. Ein Prozess startet zunächst einen und anschließend
eventuell auch mehrere Threads, um verschiedene Aufgaben zu bearbeiten. 
Threads unterscheiden sich dabei von Prozessen vor allem dadurch, dass sie
einen gemeinsamen Speicherbereich besitzen und den gleichen Zugang zu den
Systemressourcen benutzen. Einen Thread zu starten, ist somit deutlich weniger
aufwändig als das Starten eines Prozesses.

Da sich Threads einen gemeinsamen Speicherbereich teilen, können sie sehr
leicht auf die gleichen Daten zugreifen oder Daten untereinander austauschen.
Die Kommunikation von Threads ist also mit wenig Aufwand verbunden. Allerdings
birgt der Zugriff auf gemeinsame Daten auch Gefahren. Trifft man nämlich keine
geeigneten Vorkehrungen, um das Lesen und Schreiben von Daten in der
erforderlichen Reihenfolge zu gewährleisten, kann es dazu kommen, dass ein
Thread nicht die richtigen Daten bekommt. Da das Auftreten solcher Fehler davon
abhängt, wann genau welcher Thread welche Aufgaben ausführt, sind diese Fehler
nicht ohne Weiteres reproduzierbar und daher nicht immer leicht zu
identifizieren. Es gibt Techniken wie man den Datenaustausch zwischen Threads
in geordnete Bahnen lenken kann, so dass eine parallele Abarbeitung von Threads,
das so genannte *Multithreading*, möglich wird. Wir wollen hier jedoch darauf
verzichten, diese Techniken weiter zu diskutieren.

Die am häufigsten verwendete Implementation von Python, nämlich das in C
geschriebene CPython, verwendet einen sogenannten *Global Interpreter Lock*
(GIL). Dieser verhindert, dass ein einzelner Python-Prozess mehrere Threads
parallel ausführen kann. Es ist zwar durchaus möglich, in Python\ [#CPython]_
Multithreading zu verwenden. Dann sorgt aber der GIL dafür, dass die
verschiedenen Threads in Wirklichkeit abwechselnd immer wieder Rechenzeit
bekommen, so dass nur der Anschein von paralleler Verarbeitung erweckt wird.

Wenn die Abarbeitung eines Programms durch die Rechenzeit begrenzt ist, führt
die Verwendung von Multithreading in Python somit zu keiner Beschleunigung.  Im
Gegenteil wird der Mehraufwand, der durch den Wechsel zwischen verschiedenen
Threads entsteht, eher zu einer Verlangsamung des Programms führen. Es gibt
jedoch auch Probleme, deren Bearbeitungsgeschwindigkeit durch Ein- und
Ausgabevorgänge bestimmt wird. Ein Beispiel wäre ein Programm, das von vielen
Webseiten Daten herunterladen muss, um diese zu bearbeiten. Da ein Thread
während des Wartens auf Daten ohnehin untätig ist, kann es in einem solchen
Fall auch in Python sinnvoll sein, mehrere Threads zu starten, die dann 
problemlos ihre benötigte Rechenzeit erhalten können.

Da Programme im numerischen Bereich normalerweise nicht durch Ein- und Ausgabe
verlangsamt werden, sondern durch die erforderliche Rechenzeit, werden wir
uns im Folgenden nicht mit Multithreading beschäftigen, sondern uns auf die
Parallelverarbeitung von Daten durch das Starten von mehreren Prozessen
(*multiprocessing*) konzentrieren. 

Abschließend sei noch erwähnt, dass Multithreading im numerischen Bereich auch
in Python eine Rolle spielen kann, wenn numerische Bibliotheksroutinen zum
Einsatz kommen, die beispielsweise in C geschrieben sind und dann nicht mehr
unter der Kontrolle des GIL ausgeführt werden müssen. Ein Beispiel hierfür sind
eine Reihe von Operationen aus dem Bereich der linearen Algebra bei der
Verwendung einer geeignet kompilierten Version von NumPy. Hierzu zählt das mit
der Anaconda-Distribution ausgelieferte, mit der Intel® Math Kernel
Library (Intel® MKL) kompilierte NumPy. Eine andere Möglichkeit, den GIL zu
umgehen, bietet Cython\ [#cython]_, mit dem C-Erweiterungen aus Python-Code
erzeugt werden können. Dabei lassen sich Code-Teile, die keine Python-Objekte
verwenden, in einem ``nogil``-Kontext außerhalb der Kontrolle des GIL ausführen
(siehe auch das Ende des Abschnitts :ref:`with`).

.. _parallelverarbeitung:

------------------------------
Parallelverarbeitung in Python
------------------------------

Die Verwendung von parallelen Prozessen in Python wollen wir anhand eines
konkreten Beispiels diskutieren, nämlich der Berechnung der Mandelbrotmenge,
die in einer graphischen Darstellung die sogenannten Apfelmännchen ergibt.
Die Mandelbrotmenge ist mathematisch als die Menge der komplexen Zahlen
:math:`c` definiert, für die die durch die Iterationsvorschrift

.. math::

   z_{n+1} = z_n^2+c

gegebene Reihe mit dem Anfangselement :math:`z_0=0` beschränkt bleibt. Da
bekannt ist, dass die Reihe nicht beschränkt ist, wenn :math:`|z| > 2` erreicht
wird, genügt es, die Iteration bis zu diesem Schwellwert durchzuführen. Die
graphische Darstellung wird dann besonders ansprechend, wenn man die Punkte
außerhalb der Mandelbrotmenge farblich in Abhängigkeit von der Zahl der
Iterationsschritte darstellt, die bis zum Überschreiten des Schwellwerts von
:math:`2` erforderlich waren. Da die Iterationen für verschiedene Werte von
:math:`c` vollkommen unabhängig voneinander sind, ist dieses Problem
*embarrassingly parallel* und man kann sehr leicht verschiedenen Prozessen
unterschiedliche Werte von :math:`c` zur Bearbeitung zuordnen. Am Ende muss man
dann lediglich alle Ergebnisse einsammeln und graphisch darstellen.

Wir beginnen zunächst mit einer einfachen Ausgangsversion eines Programms zur
Berechnung der Mandelbrotmenge.

.. sourcecode:: python
   :linenos:

   import matplotlib.pyplot as plt
   import numpy as np
   
   def mandelbrot_iteration(c, nitermax):
       z = 0
       for n in range(nitermax):
           if abs(z) > 2:
               return n
           z = z**2+c
       return nitermax
   
   def mandelbrot(xmin, xmax, ymin, ymax, npts, nitermax):
       data = np.empty(shape=(npts, npts), dtype=np.int)
       dx = (xmax-xmin)/(npts-1)
       dy = (ymax-ymin)/(npts-1)
       for nx in range(npts):
           x = xmin+nx*dx
           for ny in range(npts):
               y = ymin+ny*dy
               data[ny, nx] = mandelbrot_iteration(x+1j*y, nitermax)
       return data
   
   def plot(data):
       plt.imshow(data, extent=(xmin, xmax, ymin, ymax),
                  cmap='jet', origin='bottom', interpolation='none')
       plt.show()
   
   nitermax = 2000
   npts = 1024
   xmin = -2
   xmax = 1
   ymin = -1.5
   ymax = 1.5
   data = mandelbrot(xmin, xmax, ymin, ymax, npts, nitermax)
   # plot(data)

Dabei erfolgt die Auswertung der Iterationsvorschrift in der Funktion
``mandelbrot_iteration`` und die Funktion ``mandelbrot`` dient dazu, alle Punkte
durchzugehen und die Ergebnisse im Array ``data`` zu sammeln. Bei der weiteren
Überarbeitung ist die Funktion ``plot`` nützlich, um die korrekte Funktionsweise
des Programms auf einfache Weise testen zu können. Für die Bestimmung der
Rechenzeit mit Hilfe des ``cProfile``-Moduls kommentieren wir den Aufruf der
``plot``-Funktion jedoch aus. Die Verwendung von ``cProfile`` ist im Kapitel
:ref:`cProfile` beschrieben. Im Folgenden sind die wesentlichen Beiträge zur
Rechenzeit für zwei verschiedene Prozessoren gezeigt, nämlich einen i7-3770::

      ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1048576  306.599    0.000  528.491    0.001 m1.py:4(mandelbrot_iteration)
   357051172  221.893    0.000  221.893    0.000 {built-in method builtins.abs}
           1    1.892    1.892  530.383  530.383 m1.py:12(mandelbrot)

und einen i5-4690::

      ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1048576   95.877    0.000  114.408    0.000 m1.py:4(mandelbrot_iteration)
   357051172   18.530    0.000   18.530    0.000 {built-in method builtins.abs}
           1    0.424    0.424  114.832  114.832 m1.py:12(mandelbrot)

Es zeigen sich deutliche Unterschiede, wobei aber in beiden Fällen die
Berechnung des Absolutbetrags der komplexen Variable ``z`` für einen
wesentlichen Beitrag zur Rechenzeit verantwortlich ist. Besonders deutlich ist
dies im ersten Fall, wo dieser Beitrag über 40 Prozent ausmacht. Bevor man zur
Parallelisierung des Codes übergeht, bietet es sich an, erst die Ausgangsversion
zu optimieren. Die Berechnung des Absolutbetrags lässt sich vermeiden, wenn man
nicht mit einer komplexen Variable rechnet, sondern Real- und Imaginärteil
separat behandelt, wie die folgende Version der Funktionen
``mandelbrot_iteration`` und ``mandelbrot`` zeigt.

.. sourcecode:: python
   :linenos:

   def mandelbrot_iteration(cx, cy, nitermax):
       x = 0
       y = 0
       for n in range(nitermax):
           x2 = x*x
           y2 = y*y
           if x2+y2 > 4:
               return n
           x, y = x2-y2+cx, 2*x*y+cy
       return nitermax
   
   def mandelbrot(xmin, xmax, ymin, ymax, npts, nitermax):
       data = np.empty(shape=(npts, npts), dtype=np.int)
       dx = (xmax-xmin)/(npts-1)
       dy = (ymax-ymin)/(npts-1)
       for nx in range(npts):
           x = xmin+nx*dx
           for ny in range(npts):
               y = ymin+ny*dy
               data[ny, nx] = mandelbrot_iteration(x, y, nitermax)
       return data

Durch diese Umschreibung verkürzt sich die Rechenzeit insbesondere für den
i7-3770-Prozessor drastisch::

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   1048576  121.770    0.000  121.770    0.000 m2.py:4(mandelbrot_iteration)
         1    1.984    1.984  123.754  123.754 m2.py:15(mandelbrot)

Aber auch für den i5-4690-Prozessor ergibt sich eine Verkürzung der Rechenzeit::

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   1048576   85.981    0.000   85.981    0.000 m2.py:4(mandelbrot_iteration)
         1    0.330    0.330   86.312   86.312 m2.py:15(mandelbrot

Man kann jedoch vermuten, dass sich die Rechenzeit noch weiter verkürzen
lässt, wenn man NumPy verwendet. In diesem Fall ist eine separate Behandlung
der Iteration nicht mehr sinnvoll, so dass wir statt der Funktionen
``mandelbrot_iteration`` und ``mandelbrot`` nur noch eine Funktion
``mandelbrot`` haben, die folgendermaßen aussieht.

.. sourcecode:: python
   :linenos:

   def mandelbrot(xmin, xmax, ymin, ymax, npts, nitermax):
       cy, cx = np.mgrid[ymax:ymin:npts*1j, xmin:xmax:npts*1j]
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
       return data

Hierbei benutzen wir *fancy indexing*, da nicht alle Elemente des Arrays
bis zum Ende iteriert werden müssen. Es ergibt sich nochmal eine signifikante
Reduktion der Rechenzeit. Der i7-3770-Prozessor mit ::

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1   21.066   21.066   21.088   21.088 m3.py:4(mandelbrot)

und der i5-4690-Prozessor mit ::

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1   20.173   20.173   20.191   20.191 m3.py:4(mandelbrot)

unterscheiden sich kaum noch in der benötigten Rechenzeit. Bereits ohne
Parallelisierung haben wir die Rechenzeit für den i7-3770-Prozessor um
einen Faktor 25 reduziert, für den i5-4690-Prozessor bei einer deutlich
geringeren anfänglichen Rechenzeit immerhin fast um einen Faktor 6.

Nun können wir daran gehen, die Berechnung dadurch weiter zu beschleunigen,
dass wir die Aufgabe in mehrere Teilaufgaben aufteilen und verschiedenen
Prozessen zur parallelen Bearbeitung übergeben.

Seit Python 3.2 stellt die Python-Standardbibliothek hierfür das
``concurrent.futures``-Modul zur Verfügung. Der Name ``concurrent`` deutet
hier auf das gleichzeitige Abarbeiten von Aufgaben hin, während sich
``futures`` auf Objekte beziehen, die zu einem späteren Zeitpunkt das
gewünschte Resultat bereitstellen.


.. image:: images/parallel/parallel_time.*
           :height: 6cm
           :align: center

.. image:: images/parallel/parallel.*
           :width: 100%
           :align: center

.. image:: images/parallel/mandelbrot_tiles.*
           :width: 6cm
           :align: center

-----
Numba
-----

.. [#CPython] Wenn wir hier von Python sprechen, meinen wir immer die
        CPython-Implementation. Eine Implementation von Python ohne GIL
        ist zum Beispiel das in Java geschriebene Jython.
.. [#cython] Cython sollte nicht mit CPython verwechselt werden.
