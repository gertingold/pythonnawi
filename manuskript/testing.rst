.. _testing:

=====================
Testen von Programmen
=====================

-----------------------
Wozu braucht man Tests?
-----------------------

Ein offensichtliches Ziel beim Programmieren besteht darin, letztlich ein
funktionierendes Programm zu haben. Funktionierend heißt hierbei, dass das
Programm die gewünschte Funktionalität korrekt bereitstellt.  Im Bereich des
numerischen Rechnens heißt dies insbesondere, dass die erhaltenen Ergebnisse
korrekt sind. Versucht man, mit numerischen Methoden noch ungelöste
naturwissenschaftliche Fragestellungen zu bearbeiten, so lässt sich
normalerweise die Korrektheit nicht direkt überprüfen. Andernfalls wäre das
gesuchte Ergebnis ja bereits bekannt. Immerhin hat man häufig die Möglichkeit,
das Ergebnis auf seine Plausibilität hin zu überprüfen, aber auch hier sind
Grenzen gesetzt. Es kann ja durchaus vorkommen, dass eine Problemstellung zu
einem völlig unerwarteten Ergebnis führt, dessen Hintergründe nicht ohne
Weiteres verständlich sind.

Um die Korrektheit der Ergebnisse möglichst weitgehend abzusichern, sollte man
daher alle sich bietenden Testmöglichkeiten wahrnehmen. Nicht selten geschieht dies
in der Praxis in einer sehr informellen Weise. Tests werden zwar durchgeführt,
aber nicht dokumentiert und auch nicht wiederholt, nachdem der Code geändert
wurde. Als Abhilfe ist es sinnvoll, einen Testrahmen aufzubauen, der es zum einen
erlaubt, Tests zu definieren und damit zu dokumentieren, und zum anderen diese
Tests in einfacher Weise auszuführen.

Beim Formulieren von Tests sollte man sich Gedanken darüber machen, was alles
schief gehen könnte, um möglichst viele Problemfälle detektieren zu können. In
diesem Prozess können sich schon Hinweise auf Möglichkeiten zur Verbesserung
eines Programms ergeben. Im Rahmen des so genannten *test driven developments*
geht man sogar so weit, zunächst die Tests zu formulieren und dann das zugehörige
Programm zu schreiben. Allerdings sind gerade im naturwissenschaftlichen Bereich
die Anforderungen zu Beginn nicht immer so klar zu definieren, dass dieses Verfahren
regelmäßig zur Anwendung kommen kann.

Tests können aber sehr wohl auch während des Entwicklungsprozesses geschrieben werden.
Entdeckt man einen Fehler, der nicht von einem der Tests angezeigt wurde, so sollte
man es sich zur Regel machen, einen Test zu schreiben, der diesen Fehler feststellen
kann. Auf diese Weise kann man verhindern, dass sich dieser Fehler nochmals unbemerkt
in das Programm einschleicht. 

Um von dem Fehlschlagen eines Tests möglichst direkt auf die Fehlerursache
schließen zu können, empfiehlt es sich, den Code in überschaubare Funktionen mit
einer klaren Aufgabe zu zerlegen, die jeweils für sich getestet werden können.
Das Schreiben von Tests kann dabei nicht nur die Korrektheit des Codes
überprüfen helfen, sondern auch dazu beitragen, die logische Gliederung des
Codes zu verbessern. Das Testen einzelner Codeeinheiten nennt man *Unit
testing*, auf das wir uns in diesem Kapitel konzentrieren werden. Zusätzlich
wird man aber auch das Zusammenwirken der einzelnen Teile eines Programms
im Rahmen von Integrationstests überprüfen.

Beim Schreiben von Tests sollte man darauf achten, dass die einzelnen Test
möglichst unabhängig voneinander sind, also jeweils spezifische Aspekte des
Codes überprüfen. Dabei lohnt es sich, auf Randfälle zu achten, also
Situationen, die nicht dem allgemeinen Fall entsprechen und denen beim
Programmieren eventuell nicht die notwendige Aufmerksamkeit zu Teil wird. Als
Beispiel könnte man die Auswertung einer Funktion mit Hilfe einer
Rekursionsformel nennen. Dabei wäre auch auf Argumente zu achten, bei denen die
Rekursionsformel nicht verwendet wird, sondern direkt deren Anfangswert
zurückzugeben ist. 

Außerdem sollte man es sich zum Ziel setzen, den Code möglichst vollständig
durch Tests abzudecken. [#coverage]_ Werden Teile des Codes durch keinen Test ausgeführt, so
könnten sich dort Fehler verstecken. Andererseits ist es nicht nötig,
Bibliotheken, die bereits von Haus aus eigene umfangreiche Testsuites besitzen,
zu testen. Man wird also zum Beispiel darauf verzichten, Funktionen der Python
Standard Library zu testen.

Aus den verschiedenen Möglichkeiten, in Python einen Testrahmen aufzubauen, wollen wir
zwei herausgreifen. Die erste basiert auf dem ``doctest``-Modul, das es erlaubt, einfache
Tests in den Dokumentationsstrings unterzubringen. Diese Tests erfüllen somit neben ihrer
eigentlichen Aufgabe auch noch die Funktion, die Möglichkeiten der Verwendung beispielsweise
einer Funktion oder einer Klasse zu dokumentieren. Die zweite Möglichkeit, die wir
besprechen wollen, basiert auf dem ``unittest``-Modul, das auch komplexere Testszenarien
ermöglicht.

---------------------
Das ``doctest``-Modul
---------------------

In Python ist die Dokumentation von Code nicht nur mit Kommentaren, die mit ``#`` eingeleitet
werden, möglich, sondern auch mit Hilfe von Dokumentationsstrings. So können zum Beispiel
Funktionen dokumentiert werden, indem nach der Kopfzeile ein typischerweise mehrzeiliger
Dokumentationstext eingefügt wird. Dieses Vorgehen wird in Python unter anderem dadurch
belohnt, dass dieser Text mit Hilfe der eingebauten ``help``-Methode verfügbar gemacht wird.
Ein weiterer Bonus besteht darin, dass im Dokumentationsstring Tests untergebracht werden
können, die zugleich die Verwendung des dokumentierten Objekts illustrieren.

Während der Dokumentationsaspekt alleine durch die Anwesenheit des entsprechenden Textteils
im Dokumentationsstring erfüllt wird, benötigen wir für den Test das ``doctest``-Modul.
Die Vorgehensweise soll an dem folgenden Beispiel erläutert werden, das auf dem Quicksort-Code
aus dem Abschnitt :ref:`listcomprehensions` basiert.

.. code-block:: python
   :linenos:

   def quicksort(x):
       """sortiere Liste x mit dem Quicksort-Verfahren
   
          Beispiele:
          >>> quicksort([2, 5, 3, 7, -1])
          [-1, 2, 3, 5, 7]
          >>> quicksort([2.25, -1.5])
          [-1.5, 2.25]
   
          Komplexe Zahlen lassen sich nicht sortieren
          >>> quicksort([2j, 1-3j])
          Traceback (most recent call last):
              ...
          TypeError: unorderable types: complex() < complex()
       """
       if len(x)<2: return x
       return (quicksort([y for y in x[1:] if y<x[0]])
               +x[0:1]
               +quicksort([y for y in x[1:] if x[0]<=y]))
   
   if __name__=="__main__":
       import doctest
       doctest.testmod()

Unsere alte Funktionsdefinition wurde hier um einen Dokumentationsstring in den Zeilen 2-15
erweitert. Die erste Zeile gibt eine kurze Beschreibung dessen, was die Funktion tut.
Danach folgen einige Beispiele, deren Format dem entspricht, was man bei der interaktiven
Arbeit in der Python-Shell vor sich hätte. Auf diese Weise hat man hier zwei
Anwendungsbeispiele illustriert, die in der Python-Shell direkt nachvollzogen werden können.
Das dritte Beispiel dient dazu, auf einen nicht zulässigen Aufruf hinzuweisen und den zugehörigen
Grund kurz zu erläutern.

Die Verwendung des Formats der Python-Shell besitzt jedoch nicht nur einen besonderen
Wiedererkennungswert für den Betrachter, sondern auch für das ``doctest``-Modul, das
genau hiernach in Dokumentationsstrings sucht. Unser Beispiel ist so aufgebaut, dass 
es bei einem direkten Aufruf das ``doctest``-Modul lädt und mit dem Aufruf der ``testmod``-Methode
die Dokumentationsstrings von Funktionen und Klassen nach Testdefinitionen durchsucht und
diese ausführt. Führt man das Skript aus, so erhält man das folgende Ergebnis::

   $ python doctest_example.py
   $

Der Umstand, dass hier keine Ausgabe erzeugt wird, ist ein gutes Zeichen, denn
er bedeutet, dass es bei der Durchführung der Tests keine Fehler gab. Das
Auftreten eines Fehlers hätte dagegen zu einer entsprechenden Ausgabe geführt.
Vielleicht will man aber wissen, ob und, wenn ja, welche Tests durchgeführt wurden.
Hierzu verwendet man die Kommandozeilenoption ``-v`` für *verbose*::

   $ python doctest_example.py -v
   Trying:
       quicksort([2, 5, 3, 7, -1])
   Expecting:
       [-1, 2, 3, 5, 7]
   ok
   Trying:
       quicksort([2.25, -1.5])
   Expecting:
       [-1.5, 2.25]
   ok
   Trying:
       quicksort([2j, 1-3j])
   Expecting:
       Traceback (most recent call last):
           ...
       TypeError: no ordering relation is defined for complex numbers
   ok
   1 items had no tests:
       __main__
   1 items passed all tests:
      3 tests in __main__.quicksort
   3 tests in 2 items.
   3 passed and 0 failed.
   Test passed.

Der Ausgabe entnimmt man, dass in der Tat die erwarteten drei Tests durchgeführt wurden und
zu dem erwarteten Ergebnis geführt haben. Will man diese ausführliche Ausgabe
unabhängig von einer Kommandozeilenoption erzwingen, kann man beim Aufruf von ``testmod``
die Variable ``verbose`` auf ``True`` setzen.

Alternativ zu der bisher beschriebenen Vorgehensweise könnte man die Zeilen 20-23 unseres
Beispielcodes weglassen und das ``doctest``-Modul beim Aufruf des Skripts laden. Will man
eine ausführliche Ausgabe erhalten, so hätte der Aufruf die folgende Form::

   $ python -m doctest -v doctest_example.py

Die Einfachheit, mit der Tests in Dokumentationsstring eingebaut und damit
zugleich auch an andere Nutzer weitergegeben werden können, sollte dazu
ermutigen, sich dieses Verfahrens zu bedienen. Allerdings gibt es bereits in
unserem einfachen Beispiel gewisse Punkte, die zu beachten sind. Der erste der
drei Tests ist unproblematisch, aber bereits beim zweiten Test ergibt sich aus
dem Umstand, dass hier Gleitkommazahlen auftreten, ein potentielles Problem.
Aufgrund von Rundungsfehlern kann es nämlich unter Umständen sein, dass die
Darstellung der entsprechenden Zahlen in der Ein- und Ausgabe voneinander
abweichen und dass dieser Unterschied von der konkreten Rechnerumgebung
abhängt. In diesem Falle würde der Test fehlschlagen. Daher wurden die
Gleitkommazahlen in unserem Beispiel so gewählt, dass die Binärdarstellung nur
wenige Nachkommastellen besitzt, so dass Rundungsfehler ausgeschlossen werden
können.

Der dritte Test im obigen Beispiel bezieht sich auf eine Eingabe, die keine
Sortierung zulässt und somit zu einer ``TypeError``-Ausnahme führt. Die
tatsächliche Ausgabe ist in diesem Fall etwas ausführlicher, wobei die Details
jedoch irrelevant sind. Daher sind in Zeile 13 im Dokumentationsstring drei
Auslassungspunkte, auf Englisch *ellipsis* zu finden, die als Platzhalter für
beliebigen Inhalt fungieren. Man könnte nun auf die Idee kommen, die
Beschreibung nach dem Doppelpunkt in Zeile 14 ebenfalls durch drei Punkte zu
ersetzen. Dies würde jedoch nicht zum Erfolg führen. In diesem Fall müsste man
am Ende von Zeile 11 noch einen Kommentar anfügen, der die Auslassungspunkte
explizit zulässt.

.. code-block:: python

   """
      >>> quicksort([2j, 1-3j]) # doctest: +ELLIPSIS
   """

Für eine detailliertere Diskussion der verschiedenen Optionen und Direktiven im
``doctest``-Modul verweisen wir auf die zugehörige 
`Dokumentation <http://docs.python.org/2/library/doctest.html>`_.

|weiterfuehrend| Das ``doctest``-Modul kann auch eingesetzt werden, um Python-Code
zu testen, der in Textdokumente eingebettet ist, die unter Verwendung von
`reStructuredText <http://docutils.sourceforge.net/rst.html>`_ erstellt wurden.
Letzeres ist unter anderem bei diesem Vorlesungsskript der Fall.

.. _unittest:

----------------------
Das ``unittest``-Modul
----------------------

Für umfangreichere Testszenarien sind die Möglichkeiten, die das
``doctest``-Modul bietet, meistens nicht ausreichend. So hatten wir im vorigen
Abschnitt bereits gesehen, dass Tests mit Gleitkommazahlen Schwierigkeiten
bereiten können. Auch ist es nicht unbedingt sinnvoll, einen
Dokumentationsstring mit einer zu großen Zahl an Tests zu versehen. Ferner kann
man sich Testszenarien vorstellen, die eine Vorbereitung und Abschlussarbeiten
erfordern. In solchen Fällen bietet es sich an, die Möglichkeiten zu nutzen,
die das ``unittest``-Modul bietet. Wie schon im vorigen Abschnitt werden wir
uns auf die wesentlichen Aspekte konzentrieren und verweisen für Details auf
die `Dokumentation <http://docs.python.org/2/library/unittest.html>`_ des
``unittest``-Moduls.

Wir beginnen mit einem Beispiel, das die ``quicksort``-Funktion aus dem vorigen
Abschnitt testet. Dazu nehmen wir an, dass die Funktion in einem Skript ``myquicksort.py``
definiert sei. Der folgende Code befinde sich in einem Skript ``test_quicksort.py``.
Dieses Namenswahl ist sinnvoll, da Testskripten standardmäßig in Dateien gesucht
werden, deren Namen mit ``test`` beginnt. Wir definieren die folgenden vier Tests:

.. code-block:: python

   from myquicksort import quicksort
   from unittest import TestCase
   
   class testQuicksort(TestCase):
       def test_sort_integers(self):
           """test sorting of integers
   
           """
           list_unsorted = [7, 2, 3, 1]
           list_sorted = [1, 2, 3, 7]
           self.assertEqual(quicksort(list_unsorted),
                            list_sorted)
   
       def test_equal_elements(self):
           """test whether equal elements are lost
   
           """
           list_unsorted = [2, 3, 4, -1, 3]
           self.assertEqual(len(quicksort(list_unsorted)),
                            len(list_unsorted))
   
       def test_sort_floats(self):
           """test sorting of floats
   
           """
           list_unsorted = [2.13, 3.12, 2.14, 2.12]
           list_sorted = [2.12, 2.13, 2.14, 3.12]
           self.assertEqual(quicksort(list_unsorted),
                            list_sorted)
   
       def test_sort_complex(self):
           """test sorting failure for complex numbers
   
           """
           with self.assertRaises(TypeError):
               quicksort([3.5+1j, 2+3.5j])

Vier Tests sind hier als Methoden einer Unterklasse der Klasse ``unittest.TestCase``
definiert und werden bei der Ausführung des Testskripts automatisch abgearbeitet.
Jeder Test soll nach Möglichkeit einen unabhängigen Aspekt des zu testenden Skripts
überprüfen. So überprüft zum Beispiel der zweite Test, dass bei der Sortierung
keine Elemente verloren gehen. Die Überprüfung der Testbedingung erfolgt jeweils
mit ``assert``-Anweisungen, von denen das ``unittest``-Modul eine ganze Reihe
für die verschiedensten Zwecke bereitstellt. 

Lässt man die Tests laufen, so erhält man die folgende Ausgabe::

   $ python -m unittest discover
   ....
   ----------------------------------------------------------------------
   Ran 4 tests in 0.000s
   
   OK

Bei diesem Aufruf wird das ``unittest``-Modul geladen und mit dem 
Schlüsselwort ``discover`` aufgefordert, selbst nach Testskripten
zu suchen. Es findet unsere Datei ``test_quicksort.py`` und führt
die vier darin enthaltenen Test aus. Alternativ hätte man statt
``discover`` auch einfach den Namen der Testdatei ohne Endung angeben
können, also::

   $ python -m unittest test_quicksort

Die Ausgabe zeigt die erfolgreiche Ausführung jedes Tests jeweils durch einen
Punkt in der zweiten Zeile an. Das abschließende ``OK`` weist nochmals darauf
hin, dass kein Fehler aufgetreten ist.

Zu Illustration bauen wir nun in unsere ``quicksort``-Funktion einen Fehler ein.

.. code-block:: python

   def quicksort(x):
       if len(x)<2: return x
       return (quicksort([y for y in x[1:] if y<x[0]])
               +x[0:1]
               +quicksort([y for y in x[1:] if x[0]<y]))

In der letzten Zeile lassen wir fälschlicherweise nur ``y``-Werte zu, die größer
als ``x[0]`` sind. Die Ausführung der Tests resultiert in folgender Ausgabe::

   F...
   ======================================================================
   FAIL: test_equal_elements (test_quicksort.testQuicksort)
   test whether equal elements are lost
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "test_quicksort.py", line 20, in test_equal_elements
       len(list_unsorted))
   AssertionError: 4 != 5

   ----------------------------------------------------------------------
   Ran 4 tests in 0.001s

   FAILED (failures=1)

Die erste Zeile gibt an, dass vier Tests ausgeführt wurden, wobei jedoch nur drei davon,
die mit Punkten dargestellt sind, erfolgreich waren. Ein Test schlug fehl und ist daher
mit einem ``F`` gekennzeichnet. Details zu diesem Test sind im Hauptteil der Ausgabe
zu finden. Ganz am Ende wird nochmals darauf hingewiesen, dass ein Test fehlschlug.

In diesem Fall kann es auch hilfreich sein, die Möglichkeit zu nutzen, eine zusätzliche
Nachricht auszugeben. Wir modifizieren dazu den zweiten Test.

.. code-block:: python

   def test_equal_elements(self):
       """test whether equal elements are lost

       """
       list_unsorted = [2, 3, 4, -1, 3]
       list_sorted = quicksort(list_unsorted)
       self.assertEqual(len(list_sorted), len(list_unsorted),
                        msg="\n  ursprüngliche Liste: {}".format(list_unsorted) +
                            "\n  sortierte Liste:     {}".format(list_sorted))

Damit erhalten wir die folgende Fehlerausgabe::

   F...
   ======================================================================
   FAIL: test_equal_elements (test_quicksort.testQuicksort)
   test whether equal elements are lost
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "test_quicksort.py", line 22, in test_equal_elements
       "\n  sortierte Liste:     {}".format(list_sorted))
   AssertionError: 4 != 5 : 
     ursprüngliche Liste: [2, 3, 4, -1, 3]
     sortierte Liste:     [-1, 2, 3, 4]

   ----------------------------------------------------------------------
   Ran 4 tests in 0.001s

   FAILED (failures=1)


Damit wird deutlich, dass die beiden Listen in der Tat ungleich lang sind, weil  
ein doppelt vorkommendes Element nicht mehrfach einsortiert wurde.

Beim Test von Gleitkommazahlen auf Gleichheit oder Ungleichheit ist wegen der Möglichkeit
von Rundungsfehlern immer Vorsicht angebracht. Von numerischen Funktionen
wird man zudem normalerweise nicht verlangen können, dass das Ergebnis bis zur
letzten Stelle korrekt ist. Das ``unittest``-Modul stellt aus diesem Grunde die
``assertAlmostEqual``- und ``assertNotAlmostEqual``-Anweisungen zur Verfügung. Dabei
wird standardmäßig die Differenz zwischen den beiden Vergleichswerten auf sieben
Nachkommastellen gerundet und mit Null verglichen. Bei Bedarf kann die Zahl der
gerundeten Stellen oder eine maximale bzw. minimale Differenz zwischen den Vergleichswerten
vorgegeben werden.

Das folgende Beispiel illustriert das Vorgehen bei Tests für Gleitkommazahlen.

.. code-block:: python

   from unittest import TestCase
   
   def square(x):
       return x*x
   
   class testNumeric(TestCase):
       def test_equal(self):
           xsquare = square(1.3)
           x2 = 1.69
           self.assertEqual(xsquare, x2)
   
       def test_almost_equal(self):
           xsquare = square(1.3)
           x2 = 1.69
           self.assertAlmostEqual(xsquare, x2)

Dabei ergibt sich die folgende Ausgabe::

   .F
   ======================================================================
   FAIL: test_equal (test_square.testNumeric)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "test_square.py", line 10, in test_equal
       self.assertEqual(xsquare, x2)
   AssertionError: 1.6900000000000002 != 1.69

   ----------------------------------------------------------------------
   Ran 2 tests in 0.000s

   FAILED (failures=1)

Tatsächlich schlägt der Test auf Gleichheit wegen des Auftretens von Rundungsfehlern
fehl, während der Vergleich auf sieben Stellen erfolgreich ist.

Gelegentlich kommt es vor, dass ein Test eine Vorbereitung sowie Nacharbeit erfordert.
Dies ist zum Beispiel beim Umgang mit Datenbanken der Fall, wo Tests nicht an Originaldaten
durchgeführt werden. Stattdessen müssen zunächst Datentabellen für den Test angelegt
und am Ende wieder entfernt werden. In dem folgenden Beispiel schreiben wir Daten in
eine temporäre Datei und überprüfen damit eine Funktion zum Einlesen dieser Daten.

.. code-block:: python

   import os
   from unittest import TestCase
   from tempfile import NamedTemporaryFile
   
   def convert_to_float(datalist):
       return list(map(float, datalist.strip("\n").split(";")))
   
   def read_floats(filename):
       with open(filename, "r") as file:
            data = list(map(convert_to_float, file.readlines()))
       return data
       
   class testReadData(TestCase):
       def setUp(self):
           """speichere Testdaten in temporärer Datei
   
           """
           file = NamedTemporaryFile("w", delete=False)
           self.filename = file.name
           self.data = [[1.23, 4.56], [7.89, 0.12]]
           for line in self.data:
               file.write(";".join(map(str, line)))
               file.write("\n")
           file.close()
   
       def test_read_floats(self):
           """teste korrektes Einlesen der Gleitkommazahlen
   
           """
           self.assertEqual(self.data,
                            read_floats(self.filename))
   
       def tearDown(self):
           """lösche temporäre Datei
   
           """
           os.remove(self.filename)

Zunächst werden die beiden zum Einlesen verwendeten Funktionen definiert, wobei aus
dem Test heraus die Funktion ``read_floats`` aufgerufen wird. In der Testklasse gibt
es neben der Methode ``test_read_floats``, die die Korrektheit des Einlesens überprüft,
noch zwei weitere Methoden. Die Methode ``setUp`` bereitet den Test vor. In unserem
Beispiel wird dort eine temporäre Datei erzeugt, von der im Laufe des Tests Daten gelesen
werden. Die Methode ``tearDown`` wird nach dem Test ausgeführt und dient hier dazu, die
temporäre Datei wieder zu entfernen.

Insbesondere wenn man Tests schreibt, bevor die entsprechende Funktionalität implementiert
ist, kann es sein, dass Tests fehlschlagen, ohne dass dies als Problem gewertet werden
muss. In diesem Fall kann man mit Hilfe von Dekoratoren dafür sorgen, dass der betreffende
Test nicht durchgeführt wird (``skip``) oder einen Hinweis auf den erwarteten Fehler
erhält (``expectedFailure``).  Das folgende Beispiel illustriert den zweiten Fall.

.. code-block:: python

   from unittest import expectedFailure, TestCase
   
   def square(x):
       """fehlerhafte Implementierung
   
       """
       return 0.5*x*x
   
   def cube(x):
       """noch nicht implementiert
   
       """
       pass
   
   class testNumeric(TestCase):
       def test_square(self):
           xsquare = square(1.3)
           x2 = 1.69
           self.assertAlmostEqual(xsquare, x2)
   
       @expectedFailure
       def test_cube(self):
           xcube = cube(1.3)
           x3 = 2.197
           self.assertAlmostEqual(xcube, x3)

Von den beiden Funktionen ``square`` und ``cube`` ist die erste fehlerhaft implementiert
und die zweite ist bis jetzt noch überhaupt nicht implementiert. Daher ist zu erwarten,
dass der zweite Test fehlschlagen wird. Er ist entsprechend mit dem ``expectedFailure``-Dekorator
versehen. Lässt man den Test laufen, so erhält man die folgende Ausgabe::

   xF
   ======================================================================
   FAIL: test_square (square.testNumeric)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "test_powers.py", line 19, in test_square
       self.assertAlmostEqual(xsquare, x2)
   AssertionError: 0.8450000000000001 != 1.69 within 7 places
   
   ----------------------------------------------------------------------
   Ran 2 tests in 0.001s
   
   FAILED (failures=1, expected failures=1)

Hier wird also zwischen dem echten Fehler, der in ``test_square`` entdeckt wird, und dem
erwarteten Fehler in ``test_cube`` unterschieden. Letzterer ist in der ersten Zeile mit
einem ``x`` statt einem ``F`` markiert.

Auch ohne dass wir alle Möglichkeiten des ``unittest``-Moduls besprochen haben,
dürfte klar geworden sein, dass diese deutlich über die Möglichkeiten des
``doctest``-Moduls hinausgehen.  Eine Übersicht über weitere
Anwendungsmöglichkeiten des ``unittest``-Moduls findet man in der zugehörigen
`Dokumentation <http://docs.python.org/2/library/unittest.html>`_, wo
inbesondere auch eine vollständige Liste der verfügbaren ``assert``-Anweisungen
angegeben ist.

----------------
Testen mit NumPy
----------------

Das Programmieren von Tests ist gerade beim numerischen Arbeiten sehr wichtig.
Bei der Verwendung von NumPy-Arrays ergibt sich allerdings das Problem, dass
man normalerweise nicht für jedes Arrayelement einzeln die Gültigkeit einer
Testbedingung überprüfen möchte. Wir wollen daher kurz diskutieren, welche
Möglichkeiten man in einem solchen Fall besitzt. Da es in erster Linie auf die
``assert``-Anweisung ankommt, können wir hier darauf verzichten, ganze
Testfälle zu programmieren.

Die im folgenden Beispiel definierte Matrix hat nur positive Eigenwerte:

.. code-block:: ipython

   In [1]: import numpy as np

   In [2]: import numpy.linalg as LA

   In [3]: a = np.array([[5, 0.5, 0.1], [0.5, 4, -0.1], [0.1, -0.1, 3]])

   In [4]: a
   Out[4]: 
   array([[ 5. ,  0.5,  0.1],
          [ 0.5,  4. , -0.1],
          [ 0.1, -0.1,  3. ]])

   In [5]: LA.eigvalsh(a)
   Out[5]: array([ 2.97774394,  3.81381575,  5.20844031])

   In [6]: np.all(LA.eigvalsh(a)>0)
   Out[6]: True

Dies lässt sich in Ausgabe 5 direkt verifizieren. Für einen automatisierten
Test ist es günstig, die Positivitätsbedingung für jedes Element auszuwerten
und zu überprüfen, ob sie für alle Elemente erfüllt ist. Dies geschieht in
Eingabe 6 mit Hilfe der ``all``-Funktion, die man in einem Test in der
``assert``-Anweisung verwenden würde.

Wir hatten im letzten Kapitel darauf hingewiesen, dass man bei Tests von Floats
die Möglichkeit von Rundungsfehlern bedenken muss. Dies gilt natürlich genauso,
wenn man ganze Arrays von Floats erzeugt und testen will. In diesem Fall ist es
sinnvoll, auf die Unterstützung zurückzugreifen, die NumPy durch sein
``testing``-Modul [#numpytest]_ gibt. Wir demonstrieren dies an einem kleinen
Beispiel, das die Berechnung des Sinus für einige Argumente testet.

.. code-block:: ipython

   In [7]: import math

   In [8]: a = np.linspace(0, math.pi, 5)

   In [9]: a
   Out[9]: array([ 0.        ,  0.78539816,  1.57079633,  2.35619449,  3.14159265])

   In [10]: result = np.sin(a)

   In [11]: correct = np.array([0, math.sqrt(0.5), 1, math.sqrt(0.5), 0])

   In [12]: np.testing.assert_array_almost_equal(result, correct, 7)

In Eingabe 10 wird das zu testende Resultat berechnet, während Eingabe 11 die auf
den analytischen Ausdrücken basierende Erwartung an das Ergebnis bestimmt. Mit
der ``assert_array_almost_equal``-Funktion erfolgt dann in Eingabe 12 der Vergleich.
Dabei haben wir die Genauigkeitsanforderung auf 7 Dezimalstellen festgelegt. Die
Tatsache, dass es zu keiner ``AssertionError``-Ausnahme kommt, bedeutet, dass 
alle Arrayelemente im Rahmen der geforderten Genauigkeit übereinstimmen.

.. [#coverage] Zur Überprüfung der Codeabdeckung durch Tests kann ``coverage.py``
   dienen, dessen Dokumentation unter `<http://coverage.readthedocs.io>`_ zu finden ist.
.. [#numpytest] Eine detaillierte Liste der verschiedenen Funktionen findet man in der 
            `Dokumentation zum Test Support <http://docs.scipy.org/doc/numpy-dev/reference/routines.testing.html>`_.

.. |weiterfuehrend| image:: images/symbols/weiterfuehrend.*
           :height: 1em
