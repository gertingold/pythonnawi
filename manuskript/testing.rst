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
eines Programms ergeben. Im Rahmen des so genannten *test-driven developments*
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
Wir beginnen mit dem folgenden einfachen Beispiel.

.. code-block:: python

   def welcome(name):
       """
       be nice and greet somebody
       name: name of the person
   
       """
       return 'Hallo {}!'.format(name)

Mit ``help(welcome)`` wird dann bekanntermaßen der Dokumentationsstring
ausgegeben, also

.. code-block:: ipython

   In [1]: help(welcome)

   Help on function welcome in module __main__:

   welcome(name)
       be nice and greet somebody
       name: name of the person

Wir erweitern nun den Dokumentationsstring um ein Anwendungsbeispiel, das
einerseits dem Benutzer die Verwendung der Funktion illustriert und andererseits
zu Testzwecken dienen kann.

.. code-block:: python
   :linenos:

   def welcome(name):
       """
       be nice and greet somebody
       name: name of the person
   
       >>> welcome('Guido')
       'Hallo Guido!'
   
       """
       return 'Hallo {}!'.format(name)
   
   if __name__ == "__main__":
       import doctest
       doctest.testmod()

Der im Beispiel verwendete Name ist eine Referenz an den Schöpfer von Python,
Guido van Rossum. Das Anwendungsbeispiel in den Zeilen 6 und 7 verwendet die
Formatierung der Python-Shell nicht nur, weil sich der Code auf diese Weise
direkt nachvollziehen lässt, sondern weil das ``doctest``-Modul dieses Format
erwartet. Gegebenenfalls sind auch mit ``...`` eingeleitete Fortsetzungszeilen
erlaubt. Folgt nach der Ausgabe noch anderer Text, so muss dieser durch eine
Leerzeile abgetrennt sein.

Der Code in den letzten drei Zeilen unseres Beispiels führt dazu, dass die Ausführung
des Skripts den in der Dokumentation enthaltenen Code testet::

   $ python example.py
   $

Der Umstand, dass hier keine Ausgabe erzeugt wird, ist ein gutes Zeichen, denn
er bedeutet, dass es bei der Durchführung der Tests keine Fehler gab. Das
Auftreten eines Fehlers hätte dagegen zu einer entsprechenden Ausgabe geführt.
Vielleicht will man aber wissen, ob und, wenn ja, welche Tests durchgeführt wurden.
Hierzu verwendet man die Kommandozeilenoption ``-v`` für *verbose*, die hier
nach dem Namen des Skripts stehen muss::

   gert@teide:[...]/manuskript: python example.py -v
   Trying:
       welcome('Guido')
   Expecting:
       'Hallo Guido!'
   ok
   1 items had no tests:
       __main__
   1 items passed all tests:
      1 tests in __main__.welcome
   1 tests in 2 items.
   1 passed and 0 failed.
   Test passed.

Der Ausgabe entnimmt man, dass ein Test erfolgreich durchgeführt wurde und zu
dem erwarteten Ergebnis geführt habt. Will man diese ausführliche Ausgabe
unabhängig von einer Kommandozeilenoption erzwingen, kann man beim Aufruf von
``testmod`` die Variable ``verbose`` auf ``True`` setzen.

Alternativ zu der bisher beschriebenen Vorgehensweise könnte man die letzten
drei Zeilen unseres Beispielcodes weglassen und das ``doctest``-Modul beim
Aufruf des Skripts laden. Will man eine ausführliche Ausgabe erhalten, so hätte
der Aufruf die folgende Form::

   $ python -m doctest -v example.py

Den Fehlerfall illustriert ein Beispiel, in dem eine englischsprachige Ausgabe
erwartet wird

.. code-block:: python

   def welcome(name):
       """
       be nice and greet somebody
       name: name of the person
   
       >>> welcome('Guido')
       'Hello Guido!'
   
       """
       return 'Hallo {}!'.format(name)

und das zu folgendem Resultat führt::

   $ python -m doctest example.py
   **********************************************************************
   File "example.py", line 6, in example.welcome
   Failed example:
       welcome('Guido')
   Expected:
       'Hello Guido!'
   Got:
       'Hallo Guido!'
   **********************************************************************
   1 items had failures:
      1 of   1 in example.welcome
   ***Test Failed*** 1 failures.

Bei Fehlern werden die Details auch ohne die Option ``-v`` ausgegeben.

Im Rahmen des *test-driven developments* könnte man als eine Art Wunschliste
noch weitere Tests einbauen. Zum Beispiel soll auch ohne Angabe eines Namens
eine sinnvolle Ausgabe erfolgen, und es soll auch eine Ausgabe in anderen
Sprachen möglich sein.

.. code-block:: python

   def welcome(name):
       """
       be nice and greet somebody
       name: name of the person
   
       >>> welcome()
       'Hello!'
   
       >>> welcome(lang='de')
       'Hallo!'
   
       >>> welcome('Guido')
       'Hello Guido!'
   
       """
       return 'Hallo {}!'.format(name)

Die im Dokumentationsstring formulierten Anforderungen führen natürlich
zunächst zu Fehlern::

   $ python -m doctest example.py
   **********************************************************************
   File "example.py", line 6, in example.welcome
   Failed example:
       welcome()
   Exception raised:
       Traceback (most recent call last):
         File "/opt/anaconda3/lib/python3.6/doctest.py", line 1330, in __run
           compileflags, 1), test.globs)
         File "<doctest example.welcome[0]>", line 1, in <module>
           welcome()
       TypeError: welcome() missing 1 required positional argument: 'name'
   **********************************************************************
   File "example.py", line 9, in example.welcome
   Failed example:
       welcome(lang='de')
   Exception raised:
       Traceback (most recent call last):
         File "/opt/anaconda3/lib/python3.6/doctest.py", line 1330, in __run
           compileflags, 1), test.globs)
         File "<doctest example.welcome[1]>", line 1, in <module>
           welcome(lang='de')
       TypeError: welcome() got an unexpected keyword argument 'lang'
   **********************************************************************
   File "example.py", line 12, in example.welcome
   Failed example:
       welcome('Guido')
   Expected:
       'Hello Guido!'
   Got:
       'Hallo Guido!'
   **********************************************************************
   1 items had failures:
      3 of   3 in example.welcome
   ***Test Failed*** 3 failures.

Der Code muss nun so lange angepasst werden, bis alle Tests korrekt durchlaufen,
wie dies für das folgende Skript der Fall ist.

.. code-block:: python

   def welcome(name='', lang='en'):
       """
       be nice and greet somebody
       name: name of the person, may be empty
       lang: two character language code
   
       >>> welcome()
       'Hello!'
   
       >>> welcome(lang='de')
       'Hallo!'
   
       >>> welcome('Guido')
       'Hello Guido!'
   
       """
       greetings = {'de': 'Hallo',
                    'en': 'Hello',
                    'fr': 'Bonjour'}
       try:
           greeting = greetings[lang]
       except KeyError:
           errmsg = 'unknown language: {}'.format(lang)
           raise ValueError(errmsg)
       if name:
           greeting = ' '.join([greeting, name])
       return greeting+'!'

Da dieser Code zu einer ``ValueError``-Ausnahme führt, wenn eine nicht implementierte
Sprache angefordert wird, stellt sich die Frage, wie dieses Verhalten getestet werden
kann. Das Problem besteht hier darin, dass die Ausgabe recht komplex sein kann. Der
Aufruf ``welcome('Guido', lang='nl')`` führt zu::

   Traceback (most recent call last):
     File "example.py", line 21, in welcome
       greeting = greetings[lang]
   KeyError: 'nl'
   
   During handling of the above exception, another exception occurred:
   
   Traceback (most recent call last):
     File "example.py", line 29, in <module>
       welcome('Guido', lang='nl')
     File "example.py", line 24, in welcome
       raise ValueError(errmsg)
   ValueError: unknown language: nl

Für den Test im Dokumentationsstring müssen allerdings nur die erste Zeile, die die
Ausnahme ankündigt, sowie die letzte Zeile, die die Ausnahme spezifiziert, angegeben 
werden, wie dies die Zeilen 16-18 im folgenden Code zeigen.

.. code-block:: python
   :linenos:

   def welcome(name='', lang='en'):
       """
       be nice and greet somebody
       name: name of the person, may be empty
       lang: two character language code
   
       >>> welcome()
       'Hello!'
   
       >>> welcome(lang='de')
       'Hallo!'
   
       >>> welcome('Guido')
       'Hello Guido!'
   
       >>> welcome('Guido', 'nl')
       Traceback (most recent call last):
       ValueError: unknown language: nl
   
       """
       greetings = {'de': 'Hallo',
                    'en': 'Hello',
                    'fr': 'Bonjour'}
       try:
           greeting = greetings[lang]
       except KeyError:
           errmsg = 'unknown language: {}'.format(lang)
           raise ValueError(errmsg)
       if name:
           greeting = ' '.join([greeting, name])
       return greeting+'!'

In diesem Zusammenhang ist auch eine der Direktiven nützlich, die das
``doctest``-Modul bereitstellt. Gibt man die Direktive ``+ELLIPSIS`` an, so
kann ``...`` beliebigen Text in der betreffenden Zeile ersetzen. Wenn uns also
die Fehlermeldung nicht genauer interessiert, können wir folgenden Test
verwenden:

.. code-block:: python

   """
   >>> welcome('Guido', 'nl')  # doctest: +ELLIPSIS
   Traceback (most recent call last):
   ValueError: ...

   """

Tests, die nicht oder vorläufig nicht durchgeführt werden sollen, kann man mit
der ``+SKIP``-Direktive wie folgt markieren:

.. code-block:: python

   """
   >>> welcome('Guido', 'nl')  # doctest: +SKIP
   'Goedendag Guido!'

   """

Weitere Direktiven, wie das gelegentlich nützliche ``+NORMALIZE_WHITESPACE``,
sind in der `Dokumentation <https://docs.python.org/3/library/doctest.html>`_
des ``doctest``-Moduls zu finden.

Interessant ist, dass diese Art der Tests nicht nur in Dokumentationsstrings
verwendet werden kann, sondern in beliebigen Texten. So lässt sich der Code
in dem Text ::

   Eine einfache Verzweigung in Python:
   >>> x = 1
   >>> if x < 0:
   ...    print('x ist negativ')
   ... else:
   ...    print('x ist nicht negativ')
   x ist nicht negativ
   
   Am Ende des Tests muss sich eine
   Leerzeile befinden.

leicht testen::

   $ python -m doctest -v example.txt
   Trying:
       x = 1
   Expecting nothing
   ok
   Trying:
       if x < 0:
          print('x ist negativ')
       else:
          print('x ist nicht negativ')
   Expecting:
       x ist nicht negativ
   ok
   1 items passed all tests:
      2 tests in example.txt
   2 tests in 1 items.
   2 passed and 0 failed.
   Test passed.

*Doctests* sind für einfachere Testsituationen sehr nützlich, da sie leicht zu
schreiben sind und gleichzeitig die Dokumentation von Code unterstützen.
Allerdings sind sie für komplexere Testszenarien, insbesondere im numerischen
Bereich, weniger gut geeignet. Dann greift man eher auf *unit tests* zurück, die
im folgenden Abschnitt beschrieben werden.

.. _unittest:

----------------------
Das ``unittest``-Modul
----------------------

Beim Erstellen von Tests stellt sich zum einen die Frage nach der technischen
Umsetzung, zum anderen aber auch danach, was ein Test sinnvollerweise überprüft.
Da *unit tests* potentiell komplexer sein können als *doctests* rückt die zweite
Frage hier etwas stärker in den Vordergrund. Wir wollen beide Aspekte, den
technischen und den konzeptionellen, am Beispiel eines Programms zur Berechnung
von Zeilen eines pascalschen Dreiecks diskutieren. Das Skript ``pascal.py``

.. code-block:: python
   :linenos:
   :name: code-pascal_int
   :caption: Code zur Berechnung von Zeilen eines pascalschen Dreiecks.

   def pascal_line(n):
       x = 1
       yield x
       for k in range(n):
           x = x*(n-k)//(k+1)
           yield x
   
   if __name__ == '__main__':
       for n in range(7):
           line = ' '.join(map(lambda x: '{:2}'.format(x), pascal_line(n)))
           print(str(n)+line.center(25))
           
erzeugt mit Hilfe der Zeilen 8-11 die Ausgabe ::

   0             1
   1           1  1          
   2          1  2  1        
   3        1  3  3  1       
   4       1  4  6  4  1     
   5     1  5 10 10  5  1    
   6    1  6 15 20 15  6  1 

wobei jede Zeile durch einen Aufruf der Funktion ``pascal_line`` bestimmt wird.
Getestet werden soll nur diese in den ersten sechs Zeilen definierte Funktion.

Ein offensichtlicher Weg, die Funktion zu testen, besteht darin, ausgewählte Zeilen des
pascalschen Dreiecks zu berechnen und mit dem bekannten Ergebnis zu vergleichen.
Hierzu erstellt man ein Testskript, das wir ``test_pascal.py`` nennen wollen:

.. code-block:: python
   :linenos:

   from unittest import main, TestCase
   from pascal import pascal_line
   
   class TestExplicit(TestCase):
       def test_n0(self):
           self.assertEqual(list(pascal_line(0)), [1])
   
       def test_n1(self):
           self.assertEqual(list(pascal_line(1)), [1, 1])
   
       def test_n5(self):
           self.assertEqual(list(pascal_line(5)), [1, 5, 10, 10, 5, 1])
   
   if __name__ == '__main__':
       main()

Da dieses Testskript zunächst unabhängig von dem zu testenden Skript ist, muss
die zu testende Funktion in Zeile 2 importiert werden. Die verschiedenen
Testfälle sind als Methoden einer von ``unittest.TestCase`` abgleiteten Klasse
implementiert. Dabei ist wichtig, dass der Name der Methoden mit ``test``
beginnen, um sie von eventuell vorhandenen anderen Methoden zu unterscheiden.
Wie wir später noch sehen werden, können mehrere Testklassen, wie hier
``TestExplicit``, implementiert werden, um auf diese Weise eine Gliederung der
Testfälle zu erreichen. Der eigentliche Test erfolgt in diesem Fall mit einer
Variante der ``assert``-Anweisung, die das ``unittest``-Modul zur Verfügung
stellt. Dabei wird auf Gleichheit der beiden Argumente getestet. Wir
werden später noch sehen, dass auch andere Test möglich sind.

Die Ausführung der Tests wird durch die letzten beiden Zeilen des Testskripts
veranlasst. Man erhält als Resultat::

   $ python test_pascal.py
   ...
   ----------------------------------------------------------------------
   Ran 3 tests in 0.000s
   
   OK

Offenbar sind alle drei Tests erfolgreich durchgeführt worden. Dies wird unter anderem auch
durch die drei Punkte in der zweiten Zeile angezeigt.

Um einen Fehlerfall zu illustrieren, bauen wir nun einen Fehler ein, und zwar der Einfachheit
halber in das Testskript. Üblicherweise wird sich der Fehler zwar im zu testenden Skript befinden,
aber das spielt hier keine Rolle. Das Testskript mit der fehlerhaften Zeile 12

.. code-block:: python
   :linenos:

   from unittest import main, TestCase
   from pascal import pascal_line
   
   class TestExplicit(TestCase):
       def test_n0(self):
           self.assertEqual(list(pascal_line(0)), [1])
   
       def test_n1(self):
           self.assertEqual(list(pascal_line(1)), [1, 1])
   
       def test_n5(self):
           self.assertEqual(list(pascal_line(5)), [1, 4, 6, 4, 1])
   
   if __name__ == '__main__':
       main()

liefert nun die Ausgabe::

   $ python test_pascal.py
   ..F
   ======================================================================
   FAIL: test_n5 (__main__.TestExplicit)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "test_pascal.py", line 12, in test_n5
       self.assertEqual(list(pascal_line(5)), [1, 4, 6, 4, 1])
   AssertionError: Lists differ: [1, 5, 10, 10, 5, 1] != [1, 4, 6, 4, 1]
   
   First differing element 1:
   5
   4
   
   First list contains 1 additional elements.
   First extra element 5:
   1
   
   - [1, 5, 10, 10, 5, 1]
   + [1, 4, 6, 4, 1]
   
   ----------------------------------------------------------------------
   Ran 3 tests in 0.003s
   
   FAILED (failures=1)

Einer der drei Tests schlägt erwartungsgemäß fehl, wobei genau beschrieben wird,
wo der Fehler aufgetreten ist und wie er sich manifestiert hat. In der zweiten Zeile
deutet das ``F`` auf einen fehlgeschlagenen Test hin. Wenn erwartet wird, dass ein
Test fehlschlägt, kann man ihn mit einem ``@expectedFailure``-Dekorator versehen. Dann
würde die Ausgabe folgendermaßen aussehen::

   $ python test_pascal.py 
   ..x
   ----------------------------------------------------------------------
   Ran 3 tests in 0.003s
   
   OK (expected failures=1)

Wenn wir die Testmethode ``test_n5`` wieder korrigieren, würden wir stattdessen ::

   gert@teide:[...]/manuskript: python test_pascal.py 
   ..u
   ----------------------------------------------------------------------
   Ran 3 tests in 0.000s
   
   FAILED (unexpected successes=1)

erhalten.

Während das Testen auf die beschriebene Weise noch praktikabel ist, ändert sich das für
große Argumente. Das Testen für größere Argumente sollte man vor allem dann in Betracht
ziehen, wenn man solche Argumente in der Praxis verwenden möchte, da es dort eventuell
zu unerwarteten Problemen kommen kann. 

Als Alternative zur Verwendung des expliziten Resultats bietet es sich an
auszunutzen, dass die Summe aller Einträge einer Zeile im pascalschen Dreieck
gleich :math:`2^n` ist, während die alternierende Summe verschwindet. Diese
beiden Tests haben die Eigenschaft, dass sie unabhängig von dem verwendeten
Algorithmus sind und somit etwaige Fehler, zum Beispiel durch eine fehlerhafte
Verwendung der Integerdivision, aufdecken. Der zusätzliche Code in unserem
Testskript könnte folgendermaßen aussehen:

.. code-block:: python

   class TestSums(TestCase):
       def test_sum(self):
           for n in (10, 100, 1000, 10000):
               self.assertEqual(sum(pascal_line(n)), 2**n)
   
       def test_alternate_sum(self):
           for n in (10, 100, 1000, 10000):
               self.assertEqual(sum(alternate(pascal_line(n))), 0)
   
   def alternate(g):
       sign = 1
       for elem in g:
           yield sign*elem
           sign = -sign

Dabei haben wir einen Generator definiert, der wechselnde Vorzeichen erzeugt. Auf
diese Weise lässt sich der eigentliche Testcode kompakt und übersichtlich halten.

Eine weitere Möglichkeit für einen guten Test besteht darin, das Konstruktionsverfahren
einer Zeile aus der vorhergehenden Zeile im pascalschen Dreieck zu implementieren. Dies
leistet der folgende zusätzliche Code:

.. code-block:: python 

   from itertools import chain
   
   class TestAdjacent(TestCase):
       def test_generate_next_line(self):
           for n in (10, 100, 1000, 10000):
               expected = [a+b for a, b
                           in zip(chain(zero(), pascal_line(n)),
                                  chain(pascal_line(n), zero()))]
               result = list(pascal_line(n+1))
               self.assertEqual(result, expected)
   
   def zero():
       yield 0

Hier wird die ``chain``-Funktion aus dem ``itertools``-Modul verwendet, um die Ausgabe
zweier Generatoren aneinanderzufügen.

Bei den *doctests* hatten wir gesehen, dass es sinnvoll sein kann zu überprüfen, ob eine
Ausnahme ausgelöst wird. In unserem Beispiel sollte dies geschehen, wenn das Argument
der Funktion ``pascal_line`` eine negative ganze Zahl ist, da dann der verwendete 
Algorithmus versagt. Die notwendige Ergänzung ist in dem folgenden Codestück gezeigt.

.. code-block:: python
   :linenos:

   def pascal_line(n):
       if n < 0:
           raise ValueError('n may not be negative')
       x = 1
       yield x
       for k in range(n):
           x = x*(n-k)//(k+1)
           yield x

Der zugehörige Test könnte folgendermaßen aussehen:

.. code-block:: python
   :linenos:

   class TestParameters(TestCase):
       def test_negative_int(self):
           with self.assertRaises(ValueError):
               next(pascal_line(-1))

Die Verwendung von ``assertRaises`` muss nicht zwingend in einem ``with``-Kontext erfolgen,
macht den Code aber sehr übersichtlich. Da die Ausnahme erst dann ausgelöst wird, wenn
ein Wert von dem Generator angefordert wurde, ist in der letzten Zeile die Verwendung
von ``next`` erforderlich.

Bisher hatten wir es weder bei *doctests* noch bei *unit tests* mit
Gleitkommazahlen zu tun, die jedoch beim numerischen Arbeiten häufig vorkommen
und eine besondere Schwierigkeit beim Testen mit sich bringen. Um dies zu
illustrieren, lassen wir in unserer Funktion ``pascal_line`` auch
Gleitkommazahlen als Argument zu. So lassen sich zum Beispiel mit
``pascal_line(1/3)`` die Taylorkoeffizienten von

.. math::

   \sqrt[3]{1+x} = 1+\frac{1}{3}x-\frac{1}{9}x^2+\frac{5}{81}x^3+\dots

bestimmen. Ist das Argument keine nichtnegative ganze Zahl, so wird der
Generator potentiell unendlich viele Werte erzeugen. Die angepasste Version
unserer Funktion sieht folgendermaßen aus:

.. code-block:: python
   :name: code-pascal_float
   :caption: Erweiterung der Funktion aus :numref:`code-pascal_int` für
      das pascalsche Dreieck auf Gleitkommaargumente.

   def pascal_line(n):
       x = 1
       yield x
       k = 0
       while n-k != 0:
           x = x*(n-k)/(k+1)
           k = k+1
           yield x

Die Koeffizienten der obigen Taylorreihe erhalten wir dann mit

.. code-block:: python

   p = pascal_line(1/3)
   for n in range(4):
       print(n, next(p))

zu ::

   0 1
   1 0.3333333333333333
   2 -0.11111111111111112
   3 0.0617283950617284

Wir erweitern unsere Tests entsprechend:

.. code-block:: python

   class TestParameters(TestCase):
       @skip('only for integer version')
       def test_negative_int(self):
           with self.assertRaises(ValueError):
               next(pascal_line(-1))
   
   class TestFractional(TestCase):
       def test_one_third(self):
           p = pascal_line(1/3)
           result = [next(p) for _ in range(4)]
           expected = [1, 1/3, -1/9, 5/81]
           self.assertEqual(result, expected)

Der erste Block zeigt beispielhaft, wie man eine Testfunktion mit Hilfe des
``@skip``-Dekorators markieren kann, so dass diese nicht ausgeführt wird. Dazu
muss allerdings zunächst ``skip`` aus dem ``unittest``-Modul importiert werden.
Auch die Testfunktionen ``test_sum``, ``test_alternate_sum`` und
``test_generate_next_line`` sollten für die Gleitkommaversion auf diese Weise
deaktiviert werden, da sie nicht mehr korrekt funktionieren, zum Beispiel weil
ein Überlauf auftritt. Als Testergebnis erhält man dann::

   s...Fsss
   ======================================================================
   FAIL: test_one_third (__main__.TestFractional)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "test_pascal.py", line 47, in test_one_third
       self.assertEqual(result, expected)
   AssertionError: Lists differ: [1, 0.3333333333333333, -0.11111111111111112, 0.0617283950617284] != [1, 0.3333333333333333, -0.1111111111111111, 0.06172839506172839]
   
   First differing element 2:
   -0.11111111111111112
   -0.1111111111111111
   
   - [1, 0.3333333333333333, -0.11111111111111112, 0.0617283950617284]
   ?                                            -                   ^
   
   + [1, 0.3333333333333333, -0.1111111111111111, 0.06172839506172839]
   ?                                                               ^^
   
   
   ----------------------------------------------------------------------
   Ran 8 tests in 0.004s
   
   FAILED (failures=1, skipped=4)

Neben den vier nicht ausgeführten Tests, die wir mit dem ``@skip``-Dekorator versehen hatten,
wird hier noch ein fehlgeschlagener Test aufgeführt, bei dem es sich um unseren neuen Test
der Gleitkommaversion handelt. Der Vergleich des erhaltenen und des erwarteten Resultats zeigt,
dass die Ursache in Rundungsfehlern liegt. 

Es gibt verschiedene Möglichkeiten, mit solchen Rundungsfehlern umzugehen. Das ``unittest``-Modul
bietet die Methode ``assertAlmostEqual`` an, die allerdings den Nachteil hat, nicht auf Listen
anwendbar zu sein. Außerdem lässt sich dort nur die Zahl der Dezimalstellen angeben, die bei der
Rundung zu berücksichtigen sind. Standardmäßig sind dies 7 Stellen. Eine mögliche Lösung wäre also:

.. code-block:: python

   class TestFractional(TestCase):
       def test_one_third(self):
           p = pascal_line(1/3)
           result = [next(p) for _ in range(4)]
           expected = [1, 1/3, -1/9, 5/81]
           for r, e in zip(result, expected):
               self.assertAlmostEqual(r, e)

Seit Python 3.5 gibt es auch die Möglichkeit, die Funktion ``isclose`` aus dem ``math``-Modul
zu verwenden, die es erlaubt, den absoluten und relativen Fehler mit ``abs_tol`` bzw. ``rel_tol``
bequem zu spezifizieren. Standardmäßig ist der absolute Fehler auf Null und der relative Fehler
auf :math:`10^{-9}` gesetzt. Der Test könnte dann folgendermaßen aussehen:

.. code-block:: python

   class TestFractional(TestCase):
       def test_one_third(self):
           p = pascal_line(1/3)
           result = [next(p) for _ in range(4)]
           expected = [1, 1/3, -1/9, 5/81]
           for r, e in zip(result, expected):
               self.assertTrue(math.isclose(r, e, rel_tol=1e-10))

Auch in diesem Fall muss man alle Elemente explizit durchgehen, was den Testcode unnötig
kompliziert macht. Abhilfe kann hier NumPy mit seinem ``testing``-Modul schaffen, auf das
wir im nächsten Abschnitt eingehen werden.

Zuvor wollen wir aber noch kurz eine Testsituation ansprechen, bei der der
eigentliche Test eine Vorbereitung sowie Nacharbeit erfordert. Dies ist zum
Beispiel beim Umgang mit Datenbanken der Fall, wo Tests nicht an Originaldaten
durchgeführt werden. Stattdessen müssen zunächst Datentabellen für den Test
angelegt und am Ende wieder entfernt werden.

In dem folgenden Beispiel soll eine Funktion zum Einlesen von Gleitkommazahlen
getestet werden. Dazu müssen wir zunächst eine temporäre Datei erzeugen, die
dann im Test eingelesen werden kann. Am Ende soll die temporäre Datei gelöscht
werden.

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
Beispiel wird dort die temporäre Datei erzeugt, von der im Laufe des Tests Daten gelesen
werden. Die Methode ``tearDown`` wird nach dem Test ausgeführt und dient hier dazu, die
temporäre Datei wieder zu entfernen.

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
Möglichkeiten man in einem solchen Fall besitzt.

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

   In [6]: np.all(LA.eigvalsh(a) > 0)
   Out[6]: True

Dies lässt sich in Ausgabe 5 direkt verifizieren. Für einen automatisierten
Test ist es günstig, die Positivitätsbedingung für jedes Element auszuwerten
und zu überprüfen, ob sie für alle Elemente erfüllt ist. Dies geschieht in
Eingabe 6 mit Hilfe der ``all``-Funktion, die man in einem Test in der
``assert``-Anweisung verwenden würde.

Im letzten Abschnitt hatten wir darauf hingewiesen, dass man bei Tests von
Gleitkommazahlen die Möglichkeit von Rundungsfehlern bedenken muss. Dies gilt
natürlich genauso, wenn man ganze Arrays von Gleitkommazahlen erzeugt und testen
will. In diesem Fall ist es sinnvoll, auf die Unterstützung zurückzugreifen, die
NumPy durch sein ``testing``-Modul [#numpytest]_ gibt.

Als Beispiel betrachten wir unseren auf Gleitkommaargumente verallgemeinerten
Code für das pascalsche Dreieck (:numref:`code-pascal_float`). Da wir dort
gleich mehrere Werte vergleichen müssen, können wir wie folgt vorgehen:

.. code-block:: ipython

   class TestFractional(TestCase):
       def test_one_third(self):
           p = pascal_line(1/3)
           result = [next(p) for _ in range(4)]
           expected = [1, 1/3, -1/9, 5/81]
           np.testing.assert_allclose(result, expected, rtol=1e-10)

Hierbei haben wir wie üblich NumPy als ``np`` importiert. Die Funktion
``assert_allclose`` erlaubt es ähnlich wie ``math.isclose``, bequem den
absoluten und relativen Fehler zu spezifizieren, wobei die entsprechenden
Variablen hier ``atol`` bzw. ``rtol`` lauten. Dabei wird der Unterschied
zwischen dem tatsächlichen und dem erwarteten Ergebnis mit der Summe aus
``atol`` und dem mit ``rtol`` multiplizierten erwarteten Ergebnis verglichen.
Defaultmäßig ist ``atol`` auf Null gesetzt, so dass nur der relative Fehler
von Bedeutung ist, der defaultmäßig den Wert :math:`10^{-7}` hat. Gegenüber
unseren früheren Tests der verallgemeinerten Funktion ``pascal_line`` hat
der obige Test den Vorteil, dass nicht explizit über die Liste iteriert werden
muss und der Testcode somit einfacher und übersichtlicher ist.

.. [#coverage] Zur Überprüfung der Codeabdeckung durch Tests kann ``coverage.py``
   dienen, dessen Dokumentation unter `<http://coverage.readthedocs.io>`_ zu finden ist.
.. [#numpytest] Eine detaillierte Liste der verschiedenen Funktionen findet man in der 
            `Dokumentation zum Test Support <http://docs.scipy.org/doc/numpy-dev/reference/routines.testing.html>`_.

.. |weiterfuehrend| image:: images/symbols/weiterfuehrend.*
           :height: 1em
