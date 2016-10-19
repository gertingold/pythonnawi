.. _advanced:

***********************************
Fortgeschrittene Aspekte von Python
***********************************

In diesem Kapitel sollen einige Sprachelemente von Python besprochen
werden, auf die in der Vorlesung »Einführung in das Programmieren für Physiker
und Materialwissenschaftler« nicht oder nur nur sehr kurz eingegangen
wurde. Aus Platz- und Zeitgründen muss allerdings auch hier eine Auswahl
getroffen werden.

====
Sets
====

In der Vorlesung »Einführung in das Programmieren für Physiker und
Materialwissenschaftler« hatten wir uns im Kapitel über zusammengesetzte
Datentypen vor allem mit Listen, Tupeln, Zeichenketten und Dictionaries
beschäftigt. Sets wurden dagegen nur kurz erwähnt und sollen hier etwas
ausführlicher besprochen werden.

Ein Set ist eine Menge von Python-Objekten, denen ein Hashwert zugeordnet
werden kann. Insofern ist es mit einem Dictionary vergleichbar, das nur
Schlüssel, aber nicht die zugehörigen Werte enthält. Die Einträge eines
Sets können nicht mehrfach auftreten, so dass die Bildung eines Sets
geeignet ist, um aus einer Liste Duplikate zu entfernen. Dies wird im
Folgenden demonstriert.

.. sourcecode:: ipython

   In [1]: list_pts = [(0, 0), (-1, 2), (0, 0), (1, 2), (-1, 2), (0,0)]

   In [2]: set_pts = set(list_pts)
   
   In [3]: set_pts
   Out[3]: {(-1, 2), (0, 0), (1, 2)}
   
   In [4]: uniq_list_pts = list(set_pts)
   
   In [5]: uniq_list_pts
   Out[5]: [(1, 2), (0, 0), (-1, 2)]

Zunächst wird eine Liste erstellt, die hier Tupel enthält, um beispielsweise
Punkte in der Ebene zu beschreiben. In der Eingabe 2 wird ein Set erstellt,
in dem, wie man in der Ausgabe 3 sieht, tatsächlich keine Duplikate mehr
vorkommen. Dabei liegen die Elemente im Set nicht in einer bestimmten Ordnung vor, 
ganz so wie wir es von Dictionaries kennen. Bei Bedarf kann man das Set auch
wieder in eine Liste umwandeln, wie die Eingabe 4 und die Ausgabe 5 zeigen.

Statt wie im vorigen Beispiel ein Set durch Umwandlung aus einer Liste zu
erzeugen, kann man die Elemente des Sets auch direkt in einer Notation mit
geschweiften Klammern, die an die Verwandtschaft mit Dictionaries erinnert,
eingeben.

.. sourcecode:: ipython

   In [1]: set_of_ints = {1, 3, 2, 5, 2, 1, 3, 4}
   
   In [2]: set_of_ints
   Out[2]: {1, 2, 3, 4, 5}

Auch hier werden natürlich eventuelle Dubletten entfernt.

Ähnlich wie Listen oder Dictionaries sind Sets auch veränderbar (*mutable*) und
damit selbst nicht als Elemente von Sets oder als Schlüssel von Dictionaries
verwendbar. Dafür kann man Elemente hinzufügen oder entfernen, wobei der
Versuch, ein nicht vorhandenes Element zu entfernen, eine ``KeyError``-Ausnahme
auslöst.

.. sourcecode:: ipython

   In [1]: data = {1, 2, 4}
   
   In [2]: data.add(3)
   
   In [3]: data
   Out[3]: {1, 2, 3, 4}
   
   In [4]: data.remove(1)
   
   In [5]: data
   Out[5]: {2, 3, 4}

   In [6]: data.remove(10)
   ---------------------------------------------------------------------------
   KeyError                                  Traceback (most recent call last)
   <ipython-input-13-6610e4562113> in <module>()
   ----> 1 data.remove(10)

   KeyError: 10

Will man ein Set als Schlüssel verwenden und ist man dafür bereit, auf die gerade
beschriebenen Möglichkeiten, ein Set zu verändern, zu verzichten, so greift man
auf das ``frozenset`` zurück, das wie der Name schon andeutet unveränderlich
(*immutable*) ist.

.. sourcecode:: ipython

   In [1]: evens = frozenset([2, 4, 6, 8])
   
   In [2]: evens.add(10)
   ---------------------------------------------------------------------------
   AttributeError                            Traceback (most recent call last)
   <ipython-input-15-2c352b4e8a10> in <module>()
   ----> 1 evens.add(10)

   AttributeError: 'frozenset' object has no attribute 'add'
   
   In [3]: odds = frozenset([1, 3, 5, 7])
   
   In [4]: numbers = {evens: "some even numbers", odds: "some odd numbers"}
   
   In [5]: numbers.keys()
   Out[5]: dict_keys([frozenset({8, 2, 4, 6}), frozenset({1, 3, 5, 7})])

Um zu überprüfen, ob ein Objekt Element einer Menge ist, ist es günstig,
statt einer Liste ein Set zu verwenden, wie die folgenden Tests zeigen.
[#ipython]_

.. sourcecode:: ipython

   In [1]: nmax = 1000000

   In [2]: xlist = list(range(nmax))

   In [3]: xset = set(xlist)

   In [4]: %timeit 1 in xlist
   10000000 loops, best of 3: 37 ns per loop

   In [5]: %timeit 1 in xset
   10000000 loops, best of 3: 32.1 ns per loop

   In [6]: %timeit nmax-1 in xlist
   100 loops, best of 3: 10.6 ms per loop

   In [7]: %timeit nmax-1 in xset
   10000000 loops, best of 3: 85.4 ns per loop

Hier liegen eine Liste und ein Set mit einer Million Elementen vor. Prüft man
auf Mitgliedschaft eines der ersten Listenelemente ab, so gibt es keinen
wesentlichen Unterschied zwischen Liste und Set. Ganz anders sieht es aus,
wenn man ein Element vom Ende der Liste auswählt. In diesem Fall muss die
ganze Liste durchsucht werden und die Ausführungszeit ist in unserem Beispiel
mehr als hunderttausendmal langsamer als für das Set. Dieser Unterschied ist
vor allem auch dann relevant, wenn das gewählte Element nicht vorhanden ist,
so dass auf jeden Fall die gesamte Liste durchsucht werden muss. Natürlich
ist die Erzeugung eines Sets mit einigem Zeitaufwand verbunden. Muss man aber
häufig auf Mitgliedschaft in einer bestimmten Liste testen, so kann die Umwandlung
in ein Set die Ausführung entscheidend beschleunigen.

Neben dem Test auf Mitgliedschaft lässt ein Set auch noch eine Reihe von
Operationen auf Mengen zu, wie zum Beispiel das Vereinigen zweier Mengen (``union``
oder ``|``), das Bilden der Schnittmenge (``intersection`` oder ``&``) und deren
Komplement (``symmetric_difference`` oder ``^``) sowie das Bilden der Differenzmenge
(``difference`` oder ``-``). Zudem lässt sich auf Unter- und Obermenge (``issubset``
bzw. ``issuperset``) sowie Schnittmengenfreiheit (``isdisjoint``) testen. Diese
Möglichkeiten sind im Folgenden illustriert.

.. sourcecode:: ipython

   In [1]: a = set([1, 2, 3])
   
   In [2]: b = set([4, 5, 6])
   
   In [3]: a.union(b)
   Out[3]: {1, 2, 3, 4, 5, 6}
   
   In [4]: c = set([1, 3, 6])
   
   In [5]: a.intersection(c)
   Out[5]: {1, 3}
   
   In [6]: a.symmetric_difference(c)
   Out[6]: {2, 6}
   
   In [7]: a.difference(c)
   Out[7]: {2}
   
   In [8]: d = set([1, 3])
   
   In [9]: a.issuperset(d)
   Out[9]: True
   
   In [10]: a.issubset(d)
   Out[10]: False
   
   In [11]: a.isdisjoint(b)
   Out[11]: True

.. _listcomprehensions:

===================
List comprehensions
===================

Um eine Liste aufzubauen, kann man sich zum Beispiel der folgenden Konstruktion
bedienen.

.. sourcecode:: ipython

   In [1]: squares = []
   
   In [2]: for n in range(10):
      ...:     squares.append(n*n)
      ...:     
   
   In [3]: squares
   Out[3]: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

Hierbei wird zunächst eine leere Liste angelegt, an die anschließend in einer
Schleife die Quadratzahlen angefügt werden. Etwas kompakter und damit auch
übersichtlicher kann man diese Funktionalität mit Hilfe einer so genannten
*list comprehension* [#listcomprehension]_ erreichen. 

.. sourcecode:: ipython

   In [1]: squares = [n*n for n in range(10)]
   
   In [2]: squares
   Out[2]: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

Liest man den Text in den eckigen Klammern in Eingabe 1, so bekommt man eine
sehr klare Vorstellung davon, was dieser Code bewirken soll. Vor der
``for``-Anweisung kann auch eine andere Anweisung stehen, die die Listenelemente
erzeugt.

.. sourcecode:: ipython

   In [1]: from math import pi, sin
   
   In [2]: [(0.1*pi*n, sin(0.1*pi*n)) for n in range(6)]
   Out[2]: [(0.0, 0.0),
    (0.3141592653589793, 0.3090169943749474),
    (0.6283185307179586, 0.5877852522924731),
    (0.9424777960769379, 0.8090169943749475),
    (1.2566370614359172, 0.9510565162951535),
    (1.5707963267948966, 1.0)]

List comprehensions sind nicht nur häufig übersichtlicher, sondern in der
Ausführung auch etwas schneller. [#timeit]_

.. sourcecode:: ipython

   In [1]: %%timeit result = []
      ...: for n in range(1000):
      ...:     result.append(n*n)
      ...: 
   10000 loops, best of 3: 91.8 µs per loop
   
   In [2]: %timeit result = [n*n for n in range(1000)]
   10000 loops, best of 3: 54.4 µs per loop

In unserem Fall ist die list comprehension also um fast einen Faktor 1,7 schneller.

Die Syntax von list comprehensions ist nicht auf die bisher beschriebenen
einfachen Fälle beschränkt. Sie lässt zum Beispiel auch das Schachteln von
Schleifen zu.

.. sourcecode:: ipython

   In [1]: [x**y for y in range(1, 4) for x in range(2, 5)]
   Out[1]: [2, 3, 4, 4, 9, 16, 8, 27, 64]
   
   In [2]: result = []
   
   In [3]: for y in range(1, 4):
      ...:     for x in range(2, 5):
      ...:         result.append(x**y)
      ...:      
   
   In [4]: result
   Out[4]: [2, 3, 4, 4, 9, 16, 8, 27, 64]

Wie man sieht, sind die ``for``-Schleifen in der list comprehension von der
äußersten zur innersten Schleife anzugeben, wobei man auch mehr als zwei Schleifen
schachteln kann.

Man kann das Hinzufügen zur Liste zusätzlich noch von Bedingungen abhängig machen.
Im folgenden Beispiel wird das Tupel nur in die Liste aufgenommen, wenn die erste
Zahl ohne Rest durch die zweite Zahl teilbar ist.

.. sourcecode:: ipython

   In [1]: [(x, y) for x in range(1, 11) for y in range(2, x) if x % y == 0]
   Out[1]: [(4, 2), (6, 2), (6, 3), (8, 2), (8, 4), (9, 3), (10, 2), (10, 5)]

Als kleines Anwendungsbeispiel betrachten wir den Quicksort-Algorithmus zur
Sortierung von Listen. Die Idee hierbei besteht darin, ein Listenelement zu
nehmen und die kleineren Elemente in einer rekursiv sortierten Liste diesem
Element voranzustellen und die anderen Elemente sortiert anzuhängen.

.. sourcecode:: ipython

   In [1]: def quicksort(x):
      ...:     if len(x) < 2: return x
      ...:     return (quicksort([y for y in x[1:] if y < x[0]])
      ...:             +x[0:1]
      ...:             +quicksort([y for y in x[1:] if x[0] <= y]))
   
   In [2]: import random
   
   In [3]: liste = [random.randint(1, 100) for n in range(10)]
   
   In [4]: liste
   Out[4]: [51, 93, 66, 62, 46, 87, 91, 41, 3, 40]
   
   In [5]: quicksort(liste)
   Out[5]: [3, 40, 41, 46, 51, 62, 66, 87, 91, 93]

Das Konzept der list comprehension lässt sich auch auf Sets und Dictionaries
übertragen. Letzteres ist im folgenden Beispiel gezeigt.

.. sourcecode:: ipython

   In [25]: s = 'Augsburg'

   In [26]: {x: s.count(x) for x in s}
   Out[26]: {'A': 1, 'b': 1, 'r': 1, 's': 1, 'u': 2, 'g': 2}

Wie wir gesehen haben, kann eine list comprehension zum einen aus einer Liste
durch Anwendung einer Funktion eine andere Liste machen und zum anderen
Listenelemente zur Aufnahme in die neue Liste mit Hilfe einer Bedingung
auswählen. Diese beiden Komponenten können gemeinsam oder auch einzeln
vorkommen.  In letzterem Fall kann man alternativ die ``map``-Funktion bzw. die
``filter``-Funktion verwenden. Beide sind zentrale Elemente des so genannten
funktionalen Programmierens. 

``map`` wendet die im ersten Argument angegebene Funktion auf die im zweiten
Argument angegebene Liste an. Um eine Liste von Quadratzahlen zu erzeugen,
kann man statt einer expliziten ``for``-Schleife auch eine der beiden
folgenden Möglichkeiten verwenden:

.. sourcecode:: ipython

   In [1]: [x*x for x in range(1, 11)]
   Out[1]: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
   
   In [2]: quadrate = map(lambda x: x*x, range(1, 11))

   In [3]: list(quadrate)
   Out[3]: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

Eine nützliche Anwendung der ``map``-Funktion besteht darin, die nach dem
Einlesen numerischer Daten zunächst vorhandenen Strings in Floats umzuwandeln:

.. sourcecode:: ipython

   In [1]: s = "0.1 0.2 0.4 -0.5"
   
   In [2]: zeilenelemente = map(float, s.split())

   In [3]: list(zeilenelemente)
   Out[3]: [0.1, 0.2, 0.4, -0.5]

Bei der ``filter``-Funktion muss die als erstes Argument angegebene Funktion
einen Wahrheitswert zurückgeben, der darüber entscheidet, ob ein Element
der Sequenz im zweiten Argument übernommen wird oder nicht.

.. sourcecode:: ipython

   In [1]: initialen = filter(lambda x: x.isupper(), 'Albert Einstein')

   In [2]: "".join(initialen)
   Out[2]: 'AE'

Zur Abwechslung haben wir hier statt einer Liste eine Zeichenkette verwendet,
die Zeichen für Zeichen abgearbeitet wird. Das Ergebnis enthält die Großbuchstaben
der Zeichenkette.

Zu den wesentlichen Elementen des funktionalen Programmierens gehört auch die
``reduce``-Funktion. Während sie in Python 2 noch zum normalen Sprachumfang
gehörte, muss sie in Python 3 aus dem ``functools``-Modul importiert werden
[#gvrblog]_. Tatsächlich gibt es für viele Anwendungsfälle angepasste
Funktionen als Ersatz, wie wir gleich noch sehen werden.

Als erstes Argument muss ``reduce`` eine Funktion bekommen, die
zwei Argumente verarbeitet. ``reduce`` wendet dann die Funktion auf die ersten
beiden Elemente der als zweites Argument angegebenen Liste an, verarbeitet dann
entsprechend das Ergebnis und das dritte Element der Liste und fährt so fort
bis das Ende der Liste erreicht ist. Die folgende Implementation der Fakultät
illustriert dies.

.. sourcecode:: ipython

   In [1]: import functools
   
   In [2]: factorial = lambda n: functools.reduce(lambda x, y: x*y, range(1, n+1))
   
   In [3]: factorial(6)
   Out[3]: 720

Entsprechend lässt sich auch die Summe der Elemente einer Liste bestimmen.

.. sourcecode:: ipython

   In [1]: reduce(lambda x, y: x+y, [0.1, 0.3, 0.7])
   Out[1]: 1.1
   
   In [2]: sum([0.1, 0.3, 0.7])
   Out[2]: 1.1

Wie die zweite Eingabe zeigt, stellt Python zu diesem Zweck auch direkt die
``sum``-Funktion zur Verfügung. Ähnliches gilt für die Verwendung der Oder- und
der Und-Verknüpfung in der ``reduce``-Funktion, die direkt durch die ``any``-
bzw. ``all``-Funktion abgedeckt werden.

.. sourcecode:: ipython

   In [1]: any([x % 2 for x in [2, 5, 6]])
   Out[1]: True
   
   In [2]: all([x % 2 for x in [2, 5, 6]])
   Out[2]: False

In der ersten Eingabe wird überprüft, ob mindestens ein Element der Liste
ungerade ist, während die zweite Eingabe überprüft, ob alle Elemente ungerade
sind.

Zum Abschluss dieses Kapitels wollen wir noch zwei äußerst praktische
eingebaute Funktionen erwähnen, die, falls sie nicht existieren würden, mit
list comprehensions realisiert werden könnten. Häufig benötigt man bei der
Iteration über eine Liste in einer ``for``-Schleife noch den Index des
betreffenden Eintrags. Dies lässt sich mit Hilfe der ``enumerate``-Funktion
sehr einfach realisieren.

.. sourcecode:: ipython

   In [1]: for nr, text in enumerate(['eins', 'zwei', 'drei']):
      ...:     print(nr+1, text)
      ...:     
   1 eins
   2 zwei
   3 drei

Die ``enumerate``-Funktion gibt also für jedes Element der Liste ein Tupel
zurück, das aus dem Index und dem entsprechenden Element besteht. Dabei beginnt
die Zählung wie immer in Python bei Null.

Es kommt auch immer wieder vor, dass man zwei oder mehr Listen parallel in einer
``for``-Schleife abarbeiten möchte. Dann ist die ``zip``-Funktion von Nutzen,
die aus den Einträgen mit gleichem Index nach dem Reißverschlussprinzip Tupel
zusammenbaut.

.. sourcecode:: ipython

   In [1]: a = [1, 2, 3]
   
   In [2]: b = [4, 5, 6]
   
   In [3]: ab = zip(a, b)

   In [4]: list(ab)
   Out[4]: [(1, 4), (2, 5), (3, 6)]

Sollten die beteiligten Listen verschieden lang sein, so ist die Länge der
neuen Liste durch die kürzeste der eingegebenen Listen bestimmt.

Man kann die ``zip``-Funktion zum Beispiel dazu verwenden, um elegant
Mittelwerte aus aufeinanderfolgenden Listenelementen zu berechnen.

.. sourcecode:: ipython

   In [1]: data = [1, 4, 5, 3, -1, 2]
   
   In [2]: for x, y in zip(data[:-1], data[1:]):
      ...:     print((x+y)/2)
      ...:     
   2.5
   4.5
   4.0
   1.0
   0.5

.. _generatoren:

==========================
Generatoren und Iteratoren
==========================

Es kommt häufig vor, dass man Listen mit einer list comprehension erzeugt, nur
um anschließend über diese Liste zu iterieren. Dabei reicht es völlig aus, wenn
die jeweiligen Elemente erst bei Bedarf erzeugt werden. Somit ist es nicht mehr
erforderlich, die ganze Liste im Speicher bereitzuhalten, was bei großen Listen
durchaus zum Problem werden könnte.

Will man die Listenerzeugung vermeiden, so kann man statt einer
list comprehension einen Generatorausdruck verwenden. Die beiden unterscheiden
sich syntaktisch dadurch, dass die umschließenden eckigen Klammern der
list comprehension durch runde Klammern ersetzt werden.

.. sourcecode:: ipython

   In [1]: quadrate = (x*x for x in xrange(4))
   
   In [2]: quadrate
   Out[2]: <generator object <genexpr> at 0x39e4a00>
   
   In [3]: for q in quadrate:
      ...:     print q
      ...:     
   0
   1
   4
   9

Man kann die Werte des Generatorausdruck auch explizit durch Verwendung der
zugehörigen ``__next__``-Methode abrufen. Allerdings sind die Werte nach dem obigen
Beispiel bereits abgearbeitet, so dass die ``__next__``-Methode in einer
``StopIteration``-Ausnahme resultiert. Damit wird angezeigt, dass bereits alle
Wert ausgegeben wurden. Die ``StopIteration``-Ausnahme war auch in der
``for``-Schleife verantwortlich dafür, dass diese beendet wurde.

.. sourcecode:: ipython

   In [4]: next(quadrate)
   ---------------------------------------------------------------------------
   StopIteration                             Traceback (most recent call last)
   <ipython-input-4-ec579e92187a> in <module>()
   ----> 1 quadrate.next()
   
   StopIteration: 
   
   In [5]: quadrate = (x*x for x in xrange(4))
   
   In [6]: next(quadrate)
   Out[6]: 0
   
   In [7]: next(quadrate)
   Out[7]: 1
   
   In [8]: next(quadrate)
   Out[8]: 4
   
   In [9]: next(quadrate)
   Out[9]: 9


   In [10]: next(quadrate)
   ---------------------------------------------------------------------------
   StopIteration                             Traceback (most recent call last)
   <ipython-input-10-ec579e92187a> in <module>()
   ----> 1 quadrate.next()
   
   StopIteration: 

In Eingabe 5 wurde der Generatorausdruck neu initialisiert, so dass er wieder
vier Werte liefern konnte. Am Ende wird dann wiederum die
``StopIteration``-Ausnahme ausgelöst. Natürlich kann man diese Ausnahme auch
abfangen, wie in folgendem Beispiel gezeigt wird.

.. sourcecode:: ipython

   In [1]: def q():
      ...:     try:
      ...:         return quadrate.next()
      ...:     except StopIteration:
      ...:         return "Das war's mit den Quadratzahlen."
      ...:     
   
   In [2]: quadrate = (x*x for x in xrange(4))
   
   In [3]: [q() for n in range(5)]
   Out[3]: [0, 1, 4, 9, "Das war's mit den Quadratzahlen."]

Aus Sequenzen kann man mit Hilfe der eingebauten ``iter``-Funktion Iteratoren
konstruieren.

.. sourcecode:: ipython

   In [1]: i = iter([1, 2, 3])
   
   In [2]: next(i)
   Out[2]: 1
   
   In [3]: next(i)
   Out[3]: 2
   
   In [4]: next(i)
   Out[4]: 3
   
   In [5]: next(i)
   ---------------------------------------------------------------------------
   StopIteration                             Traceback (most recent call last)
   <ipython-input-5-e590fe0d22f8> in <module>()
   ----> 1 next(i)
   
   StopIteration:

In der Eingabe 1 wird ein Iterator erzeugt, der über eine ``__next__``-Methode
verfügt und nach dem Abarbeiten der Liste eine ``StopIteration``-Ausnahme
auslöst. Iteratoren kann man auch über eine Klassendefinition erhalten, wie im
folgenden Beispiel für die Fibonacci-Zahlen gezeigt ist.

.. sourcecode:: ipython

   In [1]: class Fibonacci(object):
      ...:     def __init__(self, nmax):
      ...:         self.nmax = nmax 
      ...:         self.a = 0
      ...:         self.b = 1
      ...:     def __iter__(self):    
      ...:         return self
      ...:     def __next__(self):
      ...:         if self.nmax == 0:
      ...:             raise StopIteration
      ...:         self.b, self.a = self.b+self.a, self.b
      ...:         self.nmax = self.nmax-1
      ...:         return self.a
      ...:     
   
   In [2]: for n in Fibonacci(10):
      ...:     print(n, end=' ')
      ...:     
   1 1 2 3 5 8 13 21 34 55

Die ``__iter__``-Methode dieser Klasse gibt sich selbst zurück, während die
``__next__``-Methode das jeweils nächste Element zurückgibt. Nachdem die
ersten ``nmax`` Elemente der Fibonacci-Reihe erzeugt wurden, wird eine
``StopIteration``-Ausnahme ausgelöst, die zur Beendung der ``for``-Schleife in
Eingabe 2 führt.

Normalerweise wird es einfacher sein, statt einer solchen Klassendefinition
einen Generator zu schreiben. Dieser sieht auf den ersten Blick wie eine
Funktionsdefinition aus. Allerdings ist die ``return``-Anweisung durch eine
``yield``-Anweisung ersetzt, die dafür verantwortlich ist, den jeweils nächsten
Wert zurückzugeben. Bemerkenswert ist im Vergleich zu Funktionen außerdem, dass
die Werte der Funktionsvariablen nicht verlorengehen. Das folgende Beispiel
erzeugt die ersten Zeilen eines pascalschen Dreiecks.

.. sourcecode:: ipython

   In [1]: def pascaltriangle(n):
      ...:     coeff = 1
      ...:     yield coeff
      ...:     for m in range(n):
      ...:         coeff = coeff*(n-m)/(m+1)
      ...:         yield coeff
      ...:     raise StopIteration
   
   In [2]: for n in range(11):
      ...:     print " ".join(str(p).center(3) for p in pascaltriangle(n)).center(50)
      ...:     
                           1                         
                         1   1                       
                       1   2   1                     
                     1   3   3   1                   
                   1   4   6   4   1                 
                 1   5   10  10  5   1               
               1   6   15  20  15  6   1             
             1   7   21  35  35  21  7   1           
           1   8   28  56  70  56  28  8   1         
         1   9   36  84 126 126  84  36  9   1       
       1   10  45 120 210 252 210 120  45  10  1

In der letzten Zeile fungieren die Klammern der ``join``-Methode gleichzeitig als Klammern
für den Generatorausdruck.

|weiterfuehrend| Man kann ``yield`` auch benutzen, um Werte in die Funktion
einzuspeisen.  Auf diese Weise erhält man eine Koroutine. Dieses Konzept soll
hier jedoch nicht weiter diskutiert werden.

Abschließend sei noch erwähnt, dass das ``itertools``-Modul eine ganze Reihe von
nützlichen Iteratoren zur Verfügung stellt. Als Beispiel mögen Permutationen dienen.

.. sourcecode:: ipython

   In [1]: import itertools
   
   In [2]: for s in itertools.permutations("ABC"):
      ...:     print s
      ...:     
   ('A', 'B', 'C')
   ('A', 'C', 'B')
   ('B', 'A', 'C')
   ('B', 'C', 'A')
   ('C', 'A', 'B')
   ('C', 'B', 'A')


===========
Dekoratoren
===========

Dekoratoren sind ein Programmierkonstrukt, das man gelegentlich gewinnbringend
einsetzen kann, wie wir im Folgenden sehen werden. Aber selbst wenn man keine
eigenen Dekoratoren programmieren möchte, sollte man zumindest das Konzept
kennen. Es kommt immer wieder vor, dass bei der Verwendung von fremden
Python-Paketen Dekoratoren zum Einsatz kommen. Dies kann dann zum Beispiel
folgendermaßen aussehen:

.. code-block:: python

   @login_required
   def myfunc():
       """this function should only be executable by users properly logged in"""
       pass

Der Operator ``@`` weist hier auf die Verwendung eines Dekorators hin.

Bevor wir uns aber mit Dekoratoren beschäftigen, ist es nützlich, so genannte
Closures [#closure]_ zu diskutieren. Das Konzept soll an einem einfachen Beispiel
erläutert werden.

.. sourcecode:: ipython

   In [1]: def add_tax(taxrate):
      ...:     def _add_tax(value):
      ...:         return value*(1+0.01*taxrate)
      ...:     return _add_tax
      ...: 
   
   In [2]: add_mwst = add_tax(19)
   
   In [3]: add_reduzierte_mwst = add_tax(7)
   
   In [4]: for f in [add_mwst, add_reduzierte_mwst]:
      ...:     print('{:.2f}'.format(f(10)))
      ...:     
   11.90
   10.70

Mit ``add_tax`` haben wir hier eine Funktion definiert, die wiederum eine
Funktion zurückgibt. Das Interessante an dieser Konstruktion ist, dass die
zurückgegebene Funktion sich den Kontext merkt, in dem sie erzeugt wurde. In
unserem Beispiel bedeutet das, dass die Funktion ``_add_tax`` auf den Wert der
Variable ``taxrate``, also den Steuersatz, auch später noch zugreifen kann.
Dies wird deutlich, wenn wir zur Addition des vollen Mehrwertsteuersatzes die
Funktion ``add_mwst`` definieren.  Hierbei wird der Variable ``taxrate`` der
Wert 19 mitgegeben, der später beim Aufruf von ``add_mwst`` noch zur Verfügung
steht. Entsprechend definieren wir eine Funktion zur Addition des reduzierten
Mehrwertsteuersatzes. Am Beispiel der abschließenden Schleife wird deutlich,
dass die Funktionen wie gewünscht funktionieren.

Kommen wir nun zurück zu den Dekoratoren. Diese erlauben es, Funktionen oder
Klassen mit Zusatzfunktionalität zu versehen oder diese zu modifizieren. Wir
wollen uns hier auf Funktionen beschränken. Betrachten wir als ein erstes
Beispiel den folgenden Code:

.. sourcecode:: ipython

   In [1]: def register(func):
      ...:     print('{} registered'.format(func.__name__))
      ...:     return func
      ...: 
   
   In [2]: @register
      ...: def myfunc():
      ...:     print('executing myfunc')
      ...:     
   myfunc registered
   
   In [3]: myfunc()
   executing myfunc
   
   In [4]: @register
      ...: def myotherfunc():
      ...:     print('executing myotherfunc')
      ...:     
   myotherfunc registered
   
   In [5]: myotherfunc()
   executing myotherfunc

Hier haben wir zunächst einen Dekorator ``register`` definiert, der als
Argument eine Funktion erhält. Bevor er sie unverändert zurückgibt, registriert
er die Funktion, was hier durch eine einfache Ausgabe nur angedeutet wird. Der
Dekorator kann nun verwendet werden, indem vor der gewünschten Funktion die
Zeile ``@register`` eingefügt wird. Wie schon erwähnt, gibt der Operator ``@``
an, dass hier ein Dekorator verwendet wird, die folgende Funktion also
dekoriert wird. In der Eingabe 2 wird ``myfunc`` als Argument an ``register``
übergeben. Bei der Auswertung der Funktionsdefinition wird nun der
Ausgabebefehl ausgeführt. Später erfolgt dies nicht mehr, da der Dekorator
``register`` die Funktion ja unverändert zurückgegeben hat. Die Eingabe 4
zeigt, dass der Dekorator mit einer beliebigen Funktion verwendet werden kann.

Wenden wir uns nun einem etwas komplexeren Beispiel zu.
Wir haben in dem untenstehenden Code-Beispiel in den Zeilen 17-21 die
Minimalvariante einer rekursiven Funktion für die Berechnung der Fakultät
programmiert. Diese Funktion soll nun so modifiziert werden, dass
Logging-Information ausgegeben wird. Zu Beginn der Funktion soll ausgegeben
werden, mit welchem Argument die Funktion aufgerufen wurde und am Ende sollen
zusätzlich das Ergebnis und die seit dem Aufruf verstrichene Zeit ausgegeben
werden.

Natürlich könnte die entsprechende Funktionalität direkt in die Funktion
programmiert werden, aber es spricht einiges dagegen, so vorzugehen.  Die
Fähigkeit, Logging-Information auszugeben, hat nichts mit der Berechnung der
Fakultät zu tun, und daher ist es besser, die beiden Funktionalitäten sauber zu
trennen. Dies wird deutlich, wenn man bedenkt, dass die Ausgabe von
Logging-Information vor allem in der Entwicklungsphase erforderlich ist und
später wahrscheinlich entfernt werden soll. Dann müsste man wieder in das
Innere der Funktion eingreifen und die richtigen Zeilen identifizieren, die
entfernt werden müssen. Außerdem ist die Ausgabe von Logging-Information etwas,
was nicht nur für unsere spezielle Funktion nützlich ist, sondern auch in
anderen Fällen verwendet werden kann. Dies spricht wiederum dafür, diese
Funktionalität aus der eigentlichen Funktion fernzuhalten.

Genau dieses Ziel ist in dem folgenden Code realisiert, in dem die Funktion
``factorial`` mit einem Dekorator versehen ist.

.. code-block:: python
   :linenos:
   
   import time
   from itertools import chain

   def logging(func):
       def func_with_log(*args, **kwargs):
           argumente = ', '.join(map(repr, chain(args, kwargs.items())))
           print('calling {}({})'.format(func.__name__, argumente))
           start = time.time()
           result = func(*args, **kwargs)
           elapsed = time.time()-start
           print('got {}({}) = {} in {:5.3f} ms'.format(
                   func.__name__, argumente, result, elapsed*1000
                                                       ))
           return result
       return func_with_log
           
   @logging
   def factorial(n):
       if n == 1:
           return 1
       else:
           return n*factorial(n-1)

   factorial(5)

Sehen wir uns nun also den Dekorator ``logging`` in den Zeilen 4-14 an. Wie
schon angedeutet, wird die Funktion ``factorial`` als Argument ``func`` an die
Funktion ``logging`` übergeben. Der wesentliche Teil von ``logging`` besteht
darin, eine neue Funktion, die hier den Namen ``func_with_log`` trägt, zu
definieren, die die Funktion ``func`` ersetzen wird. Die Definition in den Zeilen
5-13 ist absichtlich allgemeiner gehalten als es für uns Beispiel notwendig
wäre. So lässt sich der Dekorator auch in anderen Fällen direkt einsetzen.
Daher lassen wir in Zeile 5 eine allgemeine Übergabe von Variablen in einem
Tupel ``args`` und einem Dictionary ``kwargs`` zu.

Die zugehörigen Werte werden in der Zeile 6 durch Kommas separiert zu einem
String zusammengebaut. Dabei übernimmt die aus dem ``itertools``-Modul
importierte Funktion ``chain`` die Aufgabe, die Elemente des Tupels ``args`` und der
Schlüssel-Wert-Tupel des Dictionaries ``kwargs`` zu einer einzigen Sequenz
zusammenzufassen. Mit Hilfe der ``map``-Funktion wird zu jedem Element mit
Hilfe der ``repr``-Funktion die zugehörige Darstellung erzeugt. Die
``join``-Funktion baut diese Darstellung schließlich zu einem String zusammen.
Nachdem dieses Verfahren etwas komplexer ist, sei angemerkt, dass dieses
Vorgehen nichts mit dem Dekorator an sich zu tun hat. Vielmehr ist es durch
unsere Anforderung bedingt, Logging-Information einschließlich der
Aufrufparameter ausgeben zu können, und dies nicht nur für die
``factorial``-Funktion, sondern in einem möglichst allgemeinen Fall. Die
Ausgabe der Logging-Information erfolgt in Zeile 7. Zeile 8 bestimmt den
Startzeitpunkt. In diesem Zusammenhang wurde in Zeile 1 das ``time``-Modul
importiert.

Nach diesen Vorarbeiten wird in Zeile 9 die eigentliche Funktion, die die
Fakultät berechnen soll, aufgerufen. Typischerweise wird die ursprüngliche
Funktion tatsächlich aufgerufen. Allerdings ist dies nicht unbedingt notwendig.
Man könnte stattdessen hier einfach einen Hinweis ausgeben, dass nun die Fakultät
zu berechnen wäre. Auf diese Weise würde man jedoch kein Ergebnis für die 
Fakultät erhalten.

Nachdem die ``factorial``-Funktion ihr Ergebnis zurückgegeben hat, wird in
Zeile 10 die verstrichene Zeit bestimmt und in Zeile 11 in Millisekunden
gemeinsam mit dem Ergebnis ausgegeben. Abschließend soll die dekorierte
Funktion das berechnete Resultat zurückgeben. Damit ist die Definition der
dekorierten Funktion beendet und der Dekorator gibt diese Funktion in Zeile 14
zurück.

Ruft man in Zeile 24 nun die Funktion ``factorial`` auf, so wird wegen des
``logging``-Dekorators in Wirklichkeit die gerade besprochene, dekorierte
Funktion ausgeführt. Man erhält somit die folgende Ausgabe:


.. code-block:: python

   calling factorial(5)
   calling factorial(4)
   calling factorial(3)
   calling factorial(2)
   calling factorial(1)
   got factorial(1) = 1 in 0.004 ms
   got factorial(2) = 2 in 0.085 ms
   got factorial(3) = 6 in 0.163 ms
   got factorial(4) = 24 in 0.281 ms
   got factorial(5) = 120 in 0.524 ms

In dieser Ausgabe ist gut zu sehen, wie durch die rekursive Abarbeitung
nacheinander die Fakultät von 5, von 4, von 3, von 2 und von 1 berechnet
wird. Die Ausführungen sind geschachtelt, denn die Berechnung der Fakultät
von 2 kann erst beendet werden, wenn die Fakultät von 1 bestimmt wurde.
Entsprechend benötigt die Berechnung der Fakultät von 5 auch mehr Zeit
als die Berechnung der Fakultät von 4 usw. Der ``logging``-Dekorator erlaubt
somit Einblicke in die Abarbeitung der rekursiven Funktion ohne dass
wir in diese Funktion direkt eingreifen mussten.

Abschließend betrachten wir noch ein weiteres Anwendungsbeispiel, das besonders
dann von Interesse ist, wenn die Ausführung einer Funktion relativ aufwändig
ist. Dann kann es sinnvoll sein, Ergebnisse aufzubewahren und auf diese bei
einem erneuten Aufruf mit den gleichen Argumenten wieder zuzugreifen. Dies
setzt natürlich eine deterministische Funktion voraus, also eine Funktion,
deren Ergebnis nur von den übergebenen Argumenten abhängt. Außerdem wird der
Gewinn an Rechenzeit mit Speicherplatz bezahlt.  Dies ist jedoch normalerweise
unproblematisch, so lange sich die Zahl verschiedener Argumentwerte in Grenzen
hält.

.. code-block:: python
   :linenos:
   
   import functools

   def memoize(func):
       cache = {}
       @functools.wraps(func)
       def _memoize(*args):
           if args in cache:
               return cache[args]
           result = func(*args)
           cache[args] = result
           return result
       return _memoize
           
   @logging
   @memoize
   def factorial(n):
       if n == 1:
           return 1
       else:
           return n*factorial(n-1)

Im ``memoize``-Dekorator ist hier eine Closure realisiert, die es der Funktion
``_memoize`` erlaubt, auch später auf das Dictionary ``cache`` zuzugreifen, in
dem die Ergebnisse gespeichert werden. Hierzu eignet sich ein Dictionary, weil
man die Argumente in Form des Tupels ``args`` als Schlüssel hinterlegen kann.
Allerdings ist es nicht möglich, auch ein eventuelles Dictionary ``kwargs``
im Schlüssel unterzubringen. Argumente, die mit Schlüsselworten übergeben
werden, sind hier somit nicht erlaubt.

Aus den Zeilen 14 und 15 ersieht man, dass Dekoratoren auch geschachtelt werden
können. Die Funktion ``factorial`` wird zunächst mit dem ``memoize``-Dekorator
versehen. Die so dekorierte Funktion wird dann mit dem ``logging``-Dekorator
versehen. Eine Schwierigkeit besteht hier allerdings darin, dass der 
``logging``-Dekorator für ein korrektes Funktionieren den Namen der ursprünglichen
Funktion, also ``factorial`` benötigt. Aus diesem Grunde verwendet man in Zeile 5
den ``wraps``-Dekorator aus dem ``functools``-Modul, der dafür sorgt, dass Name
und Dokumentationsstring diejenigen der Funktion ``func`` und nicht der Funktion
``_memoize`` sind.

Im Folgenden ist die Funktionsweise des ``memoize``-Dekorators gezeigt.

.. sourcecode:: ipython

   In [1]: factorial(4)
   calling factorial(4)
   calling factorial(3)
   calling factorial(2)
   calling factorial(1)
   got factorial(1) = 1 in 0.005 ms
   got factorial(2) = 2 in 0.063 ms
   got factorial(3) = 6 in 0.252 ms
   got factorial(4) = 24 in 0.369 ms
   Out[2]: 24
   
   In [2]: factorial(3)
   calling factorial(3)
   got factorial(3) = 6 in 0.007 ms
   Out[3]: 6

Beim ersten Aufruf der Funktion ``factorial`` wird die Fakultät rekursiv
ausgewertet wie wir das schon weiter oben gesehen haben. Dabei werden aber die
berechneten Werte im Dictionary ``cache`` gespeichert. Ruft man nun die
Funktion mit einem Argument auf, dessen Fakultät bereits berechnet wurde,
kann direkt auf das Ergebnis im Cache zugegriffen werden. Dies zeigt sich
daran, dass keine rekursive Berechnung mehr durchgeführt wird und die
benötigte Zeit bis zur Rückgabe des Ergebnisses sehr kurz ist.

Abschließend sei noch kurz erwähnt, dass Dekoratoren auch ein Argument haben
können, das wie üblich in Klammern angegeben wird. Dabei ist zu beachten, dass
dem Dekorator dann nicht mehr wie in den hier diskutierten Beispielen die zu
dekorierende Funktion übergeben wird, sondern das angegebene Argument. Die zu
dekorierende Funktion wird dafür dann an die im Dekorator definierte Funktion
übergeben.

=========
Ausnahmen
=========

Bereits in der »Einführung in das Programmieren« hatten wir Ausnahmen (*exceptions*)
kennengelernt und gesehen, wie man mit einem ``except``-Block auf eine Ausnahme
reagieren kann. Zudem haben wir im Abschnitt :ref:`generatoren` eine Anwendung
gesehen, in der wir selbst eine Ausnahme ausgelöst haben, nämlich eine
``StopIteration``-Ausnahme. Im Folgenden sollen noch einige Aspekte von Ausnahmen
diskutiert werden, die bis jetzt zu kurz kamen.

Grundsätzlich ist es sinnvoll, möglichst spezifisch auf Ausnahmen zu reagieren.
Daher sollte zum einen der ``try``-Block kurz gehalten werden, um einen
möglichst direkten Zusammenhang zwischen Ausnahme und auslösendem Code zu
garantieren. Zum anderen sollten nicht unnötig viele Ausnahmen gleichzeitig in
einem ``except``-Block abgefangen werden.

.. sourcecode:: ipython

   In [1]: try:
      ...:     datei = open('test.dat')
      ...: except IOError as e:
      ...:     print('abgefangener Fehler:', e)
      ...: else:
      ...:     content = datei.readlines()
      ...:     datei.close()
      ...:     
   
   In [2]: content
   Out[2]: ['Das ist der Inhalt der Test-Datei.\n']
   
   In [3]: try:
      ...:     datei = open('test.dat')
      ...: except IOError as e:
      ...:     print('abgefangener Fehler:', e)
      ...: else:
      ...:     content = datei.readlines()
      ...:     datei.close()
      ...:     
   abgefangener Fehler: [Errno 2] No such file or directory: 'test.dat'

Bei der ersten Eingabe ist die Datei ``test.dat`` vorhanden und kann geöffnet
werden.  Der ``except``-Block wird daher übersprungen und der ``else``-Block
ausgeführt. Im Prinzip hätte man den Inhalt des ``else``-Blocks auch im
``try``-Block unterbringen können. Die hier gezeigte Variante hat jedoch den
Vorteil, dass der Zusammenhang zwischen dem Versuch, eine Datei zu öffnen, und
der eventuellen ``IOError``-Ausnahme eindeutig ist. In der Eingabe 3 ist die
Datei ``test.dat`` nicht vorhanden, und es wird der ``except``-Block
ausgeführt. Die Variable ``e`` nach dem Schlüsselwort ``as`` enthält dabei
Informationen, die beim Auslösen der Ausnahme übergeben wurden und hier im
``except``-Block zur Information des Benutzers ausgegeben werden. Der
``else``-Block wird hier im Gegensatz zum ersten Fall nicht ausgeführt.

Wenn die Ausführung des Codes im ``try``-Block potentiell zu verschiedenen Ausnahmen
führen kann, ist es sinnvoll, mehrere ``except``-Blöcke vorzusehen, wie das folgende
Beispiel zeigt.

.. code-block:: python
   :linenos:

   def myfunc(x):
       mydict = {1: 'eins', 2: 'zwei'}
       try:
           print(mydict[int(x)])
       except KeyError as e:
           print('KeyError:', e)
       except TypeError as e:
           print('TypeError:', e)
   
   myfunc(1.5)
   myfunc(5.5)
   myfunc(1+3j)

Während der Funktionsaufruf in Zeile 10 keine Ausnahme auslöst, führen die
Aufrufe in den Zeilen 11 und 12 zu einem ``KeyError``, da es den Schlüssel ``5``
in ``mydict`` nicht gibt, bzw. zu einem ``TypeError`` weil sich die komplexe
Zahl ``1+3j`` nicht in einen Integer umwandeln lässt. Die Ausgabe sieht
dementsprechend folgendermaßen aus::

   eins
   KeyError: 5
   TypeError: can't convert complex to int

In diesem Beispiel wird Code wiederholt. Dies lässt sich verhindern, wenn
man die Funktion wie folgt definiert.

.. code-block:: python
   :linenos:

   def myfunc(x):
       mydict = {1: 'eins', 2: 'zwei'}
       try:
           print(mydict[int(x)])
       except (KeyError, TypeError) as e:
           print(": ".join([type(e).__name__, str(e)]))

Möchte man alle Ausnahmen abfangen, so kann man das Tupel in Zeile 5 zum
Beispiel durch ``Exception`` oder gar ``BaseException`` ersetzen. Auf den
Hintergrund hierfür kommen wir etwas später noch zurück.

Einer Folge von ``except``-Blöcken könnte sich natürlich auch wieder ein
``else``-Block anschließen, wie wir dies weiter oben gesehen hatten.
Allerdings gibt es nicht nur Situationen, wo abhängig vom Auftreten einer
Ausnahme der eine oder andere Block abgearbeitet wird, sondern es kann
auch vorkommen, dass am Ende auf jeden Fall ein gewisser Codeblock ausgeführt
werden soll. Ein typischer Fall ist das Schreiben in eine Datei. Dabei muss am
Ende sichergestellt werden, dass die Datei geschlossen wird. Hierzu dient
der ``finally``-Block. Betrachten wir ein Beispiel.

.. code-block:: python
   
   def myfunc(nr, x):
       datei = open('test_%i.dat' % nr, 'w')
       datei.write('ANFANG\n')
       try:
           datei.write('%g\n' % (1/x))
       except ZeroDivisionError as e:
           print('ZeroDivisionError:', e)
       finally:
           datei.write('ENDE\n')
           datei.close()
   
   for nr, x in enumerate([1.5, 0, 'Test']):
       myfunc(nr, x)

In der Funktion ``myfunc`` soll der Kehrwert des Arguments in die Datei
``test.dat`` geschrieben werden. Es ergibt sich die folgende Ausgabe::

   --- test_0.dat ---
   ANFANG
   0.666667
   ENDE

   --- test_1.dat ---
   ANFANG
   ENDE

   --- test_2.dat ---
   ANFANG
   ENDE

Dabei wird im zweiten Fall wegen der Division durch Null kein Kehrwert ausgeben,
während im dritten Fall ein ``TypeError`` auftritt, weil versucht wird, durch
einen String zu dividieren. Diese Ausnahme wird zwar nicht abgefangen, aber
es ist immerhin garantiert, dass die Ausgabedatei ordnungsgemäß geschlossen wird.

Was würde passieren, wenn man das Schließen der Datei nicht in einem ``finally``-Block
unterbringt, sondern einfach am Ende der Funktion ausführen lässt? Wir modifizieren
unseren Code entsprechend:

.. code-block:: python
   :linenos:

   def myfunc(nr, x):
       datei = open('test_%i.dat' % nr, 'w')
       datei.write('ANFANG\n')
       try:
           datei.write("%g\n" % (1/x))
       except ZeroDivisionError as e:
           print('ZeroDivisionError:', e)
       datei.write('ENDE\n')
       datei.close()
   
   for nr, x in enumerate([1.5, 0, 'Test']):
       myfunc(nr, x)

Nun erhält man die folgenden Dateiinhalte::

   --- test_0.dat ---
   ANFANG
   0.666667
   ENDE

   --- test_1.dat ---
   ANFANG
   ENDE

   --- test_2.dat ---
   ANFANG

Wie man sieht, ist die letzte Datei unvollständig. Die nicht abgefangene
``TypeError``-Ausnahme führt zu einem Programmabbruch, der sowohl die
Ausführung des ``write``-Befehls in Zeile 10 als auch das Schließen der Datei
verhindert. In der ersten Variante des Programms dagegen gehört der
``finally``-Block zum ``try...except``-Block und wird somit auf jeden Fall
ausgeführt. Erst danach führt der ``TypeError`` in diesem Fall zum
Programmabbruch.

Selbst in obigem Beispiel ohne ``finally``-Block wurde die Datei geschlossen,
da dies spätestens durch das Betriebssystem beim Programmende veranlasst wird.
Es ist aber dennoch kein guter Stil, sich hierauf zu verlassen. Eine Datei
nicht zu schließen, kann in Python Schwierigkeiten bereiten, wenn man die Datei
anschließend wieder zum Lesen öffnen will. Auch wenn man auf eine große Zahl
von Dateien schreiben möchte, kann es zu Problemen kommen, wenn man Dateien
nicht schließt, da die Zahl der offenen Dateien beschränkt ist. In diesem
Zusammenhang gibt es Unterschiede zwischen verschiedenen Implementationen von
Python. In CPython, also der standardmäßig verwendeten, in der
Programmiersprache C implementierten Version von Python, sorgt ein als »garbage
collection« bezeichneter Prozess, also das Einsammeln von (Daten-)Müll, dafür,
dass überflüssige Objekte entfernt werden. Hierbei werden auch Dateien
geschlossen, auf die nicht mehr zugegriffen wird. Allerdings wird dies nicht
durch die Sprachdefinition garantiert. In Jython, einer Python-Implementation
für die Java Virtual Machine, ist dies tatsächlich nicht der Fall.

Python stellt standardmäßig bereits eine große Zahl von Ausnahmen zur Verfügung,
die alle als Unterklassen von einer Basisklasse, der ``BaseException`` abgeleitet
sind. Die folgende Klassenhierarchie der Ausnahmen ist der Python-Dokumentation
entnommen, wo die einzelnen Ausnahmen auch genauer beschrieben sind. [#exceptiondoc]_

::

   BaseException
    +-- SystemExit
    +-- KeyboardInterrupt
    +-- GeneratorExit
    +-- Exception
         +-- StopIteration
         +-- StandardError
         |    +-- BufferError
         |    +-- ArithmeticError
         |    |    +-- FloatingPointError
         |    |    +-- OverflowError
         |    |    +-- ZeroDivisionError
         |    +-- AssertionError
         |    +-- AttributeError
         |    +-- EnvironmentError
         |    |    +-- IOError
         |    |    +-- OSError
         |    |         +-- WindowsError (Windows)
         |    |         +-- VMSError (VMS)
         |    +-- EOFError
         |    +-- ImportError
         |    +-- LookupError
         |    |    +-- IndexError
         |    |    +-- KeyError
         |    +-- MemoryError
         |    +-- NameError
         |    |    +-- UnboundLocalError
         |    +-- ReferenceError
         |    +-- RuntimeError
         |    |    +-- NotImplementedError
         |    +-- SyntaxError
         |    |    +-- IndentationError
         |    |         +-- TabError
         |    +-- SystemError
         |    +-- TypeError
         |    +-- ValueError
         |         +-- UnicodeError
         |              +-- UnicodeDecodeError
         |              +-- UnicodeEncodeError
         |              +-- UnicodeTranslateError
         +-- Warning
              +-- DeprecationWarning
              +-- PendingDeprecationWarning
              +-- RuntimeWarning
              +-- SyntaxWarning
              +-- UserWarning
              +-- FutureWarning
          +-- ImportWarning
          +-- UnicodeWarning
          +-- BytesWarning

Will man gleichzeitig Ausnahmen abfangen, die Unterklassen einer gemeinsamen
Klasse sind, so kann man stattdessen auch direkt die entsprechende Ausnahmeklasse
abfangen. Somit sind beispielsweise

.. code-block:: python

   except (IndexError, KeyError) as e:

und

.. code-block:: python

   except LookupError as e:

äquivalent. Man kann die vorhandenen Ausnahmeklassen, sofern sie von der
Fehlerart her passend sind, auch direkt für eigene Zwecke verwenden oder
Unterklassen programmieren. Beim Auslösen einer Ausnahme kann dabei auch
eine entsprechende Fehlermeldung mitgegeben werden.

.. sourcecode:: ipython

   In [1]: raise ValueError('42 ist keine erlaubte Eingabe!')
   ---------------------------------------------------------------------------
   ValueError                                Traceback (most recent call last)
   <ipython-input-1-c6e93f8997ca> in <module>()
   ----> 1 raise ValueError("42 ist keine erlaubte Eingabe!")

   ValueError: 42 ist keine erlaubte Eingabe!

Hat man eine Ausnahme abgefangen, so hat man die Möglichkeit, nach einer
adäquaten Reaktion die Ausnahme erneut auszulösen. Geschieht dies in einer
Funktion, so hat das aufrufende Programm wiederum die Möglichkeit, entsprechend
zu reagieren. Dies ist im folgenden Beispiel illustriert.

.. code-block:: python

   def reciprocal(x):
       try:
           return 1/x
       except ZeroDivisionError:
           msg = 'Maybe the main program knows what to do...'
           raise ZeroDivisionError(msg)
   
   try:
       reciprocal(0)
   except ZeroDivisionError as e:
       print(e)
       print("Let's just continue!")
   
   print("That's the end of the program.")

Dieses Programm erzeugt die folgende Ausgabe::

   Maybe the main program knows what to do...
   Let's just continue!
   That's the end of the program.

Die Funktion ``reciprocal`` fängt die Division durch Null ab. Sie verhindert
damit den vorzeitigen Programmabbruch und gibt dem Hauptprogramm die Chance,
in geeigneter Weise zu reagieren. Dies geschieht hier, indem wiederum der
``ZeroDivisionError`` abgefangen wird.

==============================
Kontext mit ``with``-Anweisung
==============================

Im vorigen Abschnitt hatten wir im Zusammenhang mit dem Zugriff auf eine Datei
ein typisches Szenario kennengelernt, bei dem die eigentliche Funktionalität
zwischen zwei Schritte eingebettet ist, in denen zunächst Vorbereitungen getroffen
werden und am Ende notwendige Aufräumarbeiten durchgeführt werden. In unserem
Beispiel wäre dies das Öffnen der Datei zu Beginn und das Schließen der Datei am
Ende. Eine solche Situation kann in Python mit Hilfe eines Kontextmanagers
elegant bewältigt werden. Dies ist im folgenden Beispiel gezeigt.

.. code-block:: python

   with open('test.dat', 'w') as file:
       for n in range(4, -1, -1):
           file.write('{:g}\n'.format(1/n))

Dies entspricht einem ``try...finally``-Konstrukt, bei dem im ``finally``-Block
unabhängig vom Auftreten einer Ausnahme die Datei wieder geschlossen wird.
Die Ausgabedatei hat dann den folgenden Inhalt::

   0.25
   0.333333
   0.5
   1

Sie wurde explizit beim Verlassen des ``with``-Blocks geschlossen, nachdem zuvor
die Variable ``n`` den Wert Null erreicht hat und die Division eine
``ZeroDivisionError``-Ausnahme ausgelöst hat. Um dies zu überprüfen, muss man die
Ausnahme abfangen.

.. code-block:: python

   try:
       with open('test.dat', 'w') as file:
           for n in range(4, -1, -1):
               file.write('{:g}\n'.format(1/n))
   except ZeroDivisionError:
       print('division by zero')

   print('file is closed: {}'.format(file.closed))

Die zugehörige Ausgabe lautet dann wie erwartet::

   division by zero
   file is closed: True 

Kontextmanager können unter anderem beim Arbeiten mit Cython [#cython]_
nützlich sein.  Cython ermöglicht die Optimierung von Python-Skripten, indem es
C-Erweiterungen anbietet. Dazu gehört unter anderem die Möglichkeit, den
Datentyp von Variablen festzulegen.  In Python werden Listenindizes
normalerweise darauf überprüft, ob sie innerhalb des zulässigen Bereichs liegen,
und es werden negative Indizes entsprechend behandelt. Dies kostet natürlich
Zeit. Ist man sich sicher, dass man weder negative Indizes benutzt noch die
Listengrenzen überschreitet, so kann man bei der Benutzung von Cython auf die
genannte Funktionalität verzichten. Will man dies in einem begrenzten
Code-Block tun, so bietet sich die Verwendung von ``with
cython.boundscheck(False)`` an.  Eine andere Anwendung besteht im Ausschalten
des *Global Interpreter Locks* [#gil]_ von Python mit Hilfe des
``nogil``-Kontextmanagers.

.. [#ipython] Hier verwenden wir ``%timeit``, eine der so genannten magischen
              Funktionen der verbesserten Python-Shell ``IPython``, die es erlaubt,
              Ausführungszeiten einzelner Befehle oder (ab Version 0.13) von
              Befehlsblöcken zu bestimmen. Wie werden hierauf im Abschnitt :ref:`timeit`
              zurückkommen.
.. [#listcomprehension] Wir belassen es hier bei dem üblicherweise verwendeten
              englischen Begriff. Gelegentlich findet man den Begriff
              »Listenabstraktion« als deutsche Übersetzung.
.. [#timeit] Will man die Ausführungszeit eines ganzen Befehlsblocks bestimmen,
             so muss die magische ``%%timeit``-Funktion mit zwei Prozentzeichen
             verwendet werden. Bei Einzeilern genügt ``%timeit`` mit einem
             Prozentzeichen. ``%%timeit`` wurde der ``IPython``-Version 0.13
             eingeführt. Wir werden hierauf im Abschnitt :ref:`timeit` zurückkommen.
.. [#gvrblog] Guido von Rossum begründet das in einem `Blog
           <http://www.artima.com/weblogs/viewpost.jsp?thread=98196>`_ 
           mit dem Titel *The fate of reduce() in Python 3000* aus dem Jahr 2005.
.. [#closure] Wir belassen es auch hier wieder bei dem häufig verwendeten 
           englischen Begriff, der als »Funktionsabschluss« zu übersetzen wäre.
.. [#exceptiondoc] Siehe 
          `6. Built-in Exceptions <http://docs.python.org/library/exceptions.html#exceptions.BaseException/>`_
          in der Dokumentation der Standardbibliothek von Python.
.. [#cython] Weitere Informationen zu Cython findet man unter `www.cython.org <http://www.cython.org/>`_.
          Cython sollte nicht mit CPython verwechselt werden, der C-Implementation von Python, die
          man standardmäßig beim ``python``-Aufruf verwendet.
.. [#gil] Siehe das `Glossar der Python-Dokumentation <http://docs.python.org/2/glossary.html#term-global-interpreter-lock>`_
          für eine kurze Erläuterung des GIL.

.. |weiterfuehrend| image:: images/symbols/weiterfuehrend.*
           :height: 1em
