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
parallel ausführen kann. Es ist zwar durchaus möglich, in Python [#CPython]_
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
umgehen, bietet Cython [#cython]_, mit dem C-Erweiterungen aus Python-Code
erzeugt werden können. Dabei lassen sich Code-Teile, die keine Python-Objekte
verwenden, in einem ``nogil``-Kontext außerhalb der Kontrolle des GIL ausführen
(siehe auch das Ende des Abschnitts :ref:`with`).

.. _parallelverarbeitung:

------------------------------
Parallelverarbeitung in Python
------------------------------


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
