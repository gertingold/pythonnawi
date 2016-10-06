=====
NumPy
=====

In der Vorlesung »Einführung in das Programmieren für Physiker und Naturwissenschaftler«
wurde am Beispiel von NumPy und SciPy eine kurze Einführung in die Benutzung numerischer
Programmbibliotheken gegeben. Dabei wurde an einigen wenigen Beispielen gezeigt, wie man
in Python mit Vektoren und Matrizen arbeiten und einfache Problemstellungen der linearen
Algebra lösen kann. Im Folgenden wollen wir uns etwas genauer mit NumPy beschäftigen ohne
dabei eine vollständige Beschreibung anzustreben. Bei Bedarf sollte daher die
`NumPy Referenzdokumentation <http://docs.scipy.org/doc/numpy/reference/>`_ herangezogen
werden. Als Informationsquelle sind zudem die `Python Scientific Lecture Notes
<http://scipy-lectures.github.com/>`_ empfehlenswert. Dort werden auch andere
Programmbibliotheken diskutiert, die in naturwissenschaftlichen Anwendungen hilfreich
sein können.

.. _pythonlisten:

------------------------------
Python-Listen und NumPy-Arrays
------------------------------

Viele naturwissenschaftliche Problemstellungen lassen sich in natürlicher Weise mit Hilfe
von Vektoren und Matrizen formulieren. Dies kann entweder eine Eigenschaft des ursprünglichen
Problems sein, beispielsweise bei der Beschreibung eines gekoppelten schwingenden Systems
mit Hilfe von gekoppelten Differentialgleichungen. Es kann aber auch vorkommen, dass erst
die numerische Umsetzung zu einer Formulierung in Vektoren und Matrizen führt, zum Beispiel
bei der Diskretisierung einer partiellen Differentialgleichung.

Will man solche Problemstellungen mit den Standardmitteln bearbeiten, die von
Python zur Verfügung gestellt werden, so wird man auf Listen zurückgreifen
müssen. Um eine zweidimensionale Matrix zu definieren, würde man eine Liste von
Listen anlegen und könnte dann durch eine doppelte Indizierung auf ein einzelnes Element 
zugreifen.

.. sourcecode:: ipython

   In [1]: matrix = [[1.1, 2.2, 3.3], [4.4, 5.5, 6.6], [7.7, 8.8, 9.9]]

   In [2]: matrix[0]
   Out[2]: [1.1, 2.2, 3.3]

   In [3]: matrix[0][2]
   Out[3]: 3.3

Das Beispiel erklärt die doppelte Indizierung. Durch den ersten Index, hier ``[0]``, wird
die erste Unterliste ausgewählt aus der wiederum ein einzelnes Element, hier das dritte,
ausgewählt werden kann. Somit besteht hier, ganz im Gegensatz zu zweidimensionalen Matrizen,
ein grundsätzlicher Unterschied zwischen Zeilen und Spalten. Eine Zeile kann man entweder
wie oben in der Eingabe 2 erhalten oder auch etwas umständlicher mit

.. sourcecode:: ipython

   In [4]: matrix[0][:]
   Out[4]: [1.1, 2.2, 3.3]

Hier ist explizit angegeben, dass wir alle Elemente der ersten Zeile haben wollen. Ein
enstprechender Zugriff auf eine Spalte funktioniert jedoch nicht:

.. sourcecode:: ipython

   In [5]: matrix[:][0]
   Out[5]: [1.1, 2.2, 3.3]

Hier gibt ``matrix[:]`` eine Liste mit allen Unterlisten, also einfach die ursprüngliche
Liste zurück. Somit ist ``matrix[:][0]`` nichts anderes als die erste Unterliste. Wir
erhalten also wiederum die erste Zeile und keineswegs die erste Spalte. Allgemein ist
die Extraktion einer Untermatrix aus einer durch Listen dargestellten Matrix nicht ohne
einen gewissen Aufwand möglich.

Ein weiterer Nachteil besteht in der Flexibilität von Listen, die ja bekanntlich beliebige
Objekte enthalten können. Python muss daher einen erheblichen Aufwand bei der Verwaltung
von Listen treiben. Dies betrifft alleine schon die Adressierung eines einzelnen Elements.
Andererseits wird diese Flexibilität bei Matrizen überhaupt nicht benötigt, da dort alle
Einträge vom gleichen Datentyp sind. Es sollte also möglich sein, erheblich effizientere
Programme zu schreiben, indem man Matrizen nicht durch Listen darstellt, sondern durch
einen auf diese Aufgabe zugeschnittenen Datentypen. Hierzu greift man auf das von NumPy
zur Verfügung gestellte ``ndarray``-Objekt, also ein N-dimensionales Array, zurück.

Ein Array [#array]_ besitzt als wesentliche Bestandteile die Daten im eigentlichen Sinne, also die
Werte der einzelnen Matrixelemente, sowie Information darüber, wie auf ein spezifisches
Matrixelement zugegriffen werden kann. Die Daten sind im Speicher einfach hintereinander,
also in eindimensionaler Form, abgelegt. Dabei gibt es die Möglichkeit, die Matrix zeilenweise
oder spaltenweise abzuspeichern. Ersteres wird von der Programmiersprache C verwendet,
während die zweite Variante von Fortran verwendet wird.

Nachdem die Daten strukturlos im Speicher abgelegt sind, müssen ``ndarray``-Objekte, wie
schon erwähnt, neben den Daten auch Informationen darüber besitzen, wie auf einzelne
Matrixelemente zugegriffen wird. Auf diese Weise lässt sich sehr leicht die Adresse der
Daten eines Matrixelements bestimmen. Zudem ist es möglich, die gleichen Daten im Speicher
auf verschiedene Weise anzusehen. Damit ist es häufig möglich, unnötige Kopiervorgänge im
Speicher zu vermeiden. Andererseits ist es aus diesem Grunde wichtig zu wissen, ob NumPy
im Einzelfall nur eine andere Sicht auf die Daten zur Verfügung stellt oder tatsächlich
ein neues Array erzeugt.

Um die Informationen über die Struktur eines Arrays besser zu verstehen, betrachten wir
ein Beispiel. 

.. sourcecode:: ipython

   In [1]: import numpy as np

   In [2]: matrix = np.arange(16)

   In [3]: matrix
   Out[3]: array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])

   In [4]: matrix.dtype, matrix.itemsize, matrix.size, matrix.nbytes
   Out[4]: (dtype('int64'), 8, 16, 128)

   In [5]: matrix.shape
   Out[5]: (16,)

   In [6]: matrix.strides
   Out[6]: (8,)

Wir laden zunächst das ``numpy``-Modul, für das üblicherweise die Abkürzung
``np`` verwendet wird. Dieser Schritt wird in allen folgenden Beispielen
vorausgesetzt.  Dann erzeugen wir uns auf möglichst einfache Weise ein Array
mit 16 Elementen. Die Funktionsweise von ``arange`` werden wir später noch
etwas ausführlicher diskutieren. Wir erhalten somit ein eindimensionales Array,
das die Zahlen von 0 bis 15 als Integers enthält.  Das Objekt ``matrix`` hat
nun einige Eigenschaften. Der Datentyp ``dtype`` ist hier ``int64``, also ein
Integer mit einer Länge von 64 Bit oder 8 Bytes. Letzteres wird auch durch das
Attribut ``itemsize`` angegeben. Die Größe des Arrays, also ``size``, ist 16,
so dass sich insgesamt ein Speicherbedarf ``nbytes`` von 128 Bytes ergibt. Das
Tupel ``shape`` gibt die Form des Arrays an. In unserem Fall gibt es nur eine
Dimension, die 16 Elemente enthält. Das Tupel ``strides`` schließlich gibt an,
wie weit benachbarte Elemente in einer bestimmten Dimension voneinander
entfernt sind. Bei einem eindimensionalen Array ist dies gerade die Zahl der
Bytes, die ein Dateneintrag benötigt.

Mit Hilfe der Attribute ``shape`` und ``strides`` kann man nun eine andere
Sicht auf das gleiche Array erhalten. 

.. sourcecode:: ipython

   In [7]: matrix.shape = (4, 4)

   In [8]: matrix
   Out[8]: 
   array([[ 0,  1,  2,  3],
          [ 4,  5,  6,  7],
          [ 8,  9, 10, 11],
          [12, 13, 14, 15]])

   In [9]: matrix.strides
   Out[9]: (32, 8)

   In [10]: matrix.shape = (2, 2, 2, 2)

   In [11]: matrix
   Out[11]: 
   array([[[[ 0,  1],
            [ 2,  3]],

           [[ 4,  5],
            [ 6,  7]]],


          [[[ 8,  9],
            [10, 11]],

           [[12, 13],
            [14, 15]]]])

   In [12]: matrix.strides
   Out[12]: (64, 32, 16, 8)

Wir interpretieren zunächst die 16 Matrixelemente als ein 4×4-Array, ohne dabei
die eigentlichen Array-Daten im Speicher in irgendeiner Weise zu modifizieren.
Lediglich das Attribut ``shape`` haben wir neu gesetzt. Das Attribut
``strides`` gibt uns nun an, dass der Abstand der Daten in der ersten
Dimension, also innerhalb einer Spalte, 32 Bytes beträgt, während der Abstand in
der zweiten Dimension, also innerhalb einer Zeile, nach wie vor 8 ist. So lange
das Produkt der Dimensionen der Gesamtzahl der Matrixelemente entspricht,
können wir auch andere Matrixdimensionen wählen. So können wir unsere Daten
auch als ein 2×2×2×2-Array ansehen, wie der zweite Teil der obigen Ausgabe
zeigt.

Mit Hilfe der Attribute ``shape`` und ``strides`` lässt sich die Sicht auf ein
Array auf sehr flexible Weise festlegen. Allerdings ist der Benutzer selbst für
die Folgen verantwortlich, wie der zweite Teil des folgenden Beispiels zeigt.
Dazu gehen wir zum 4×4-Array zurück und verändern das Attribut ``strides`` mit
Hilfe der ``as_strided``-Methode.

.. sourcecode:: ipython

   In [13]: matrix.shape = (4, 4)

   In [14]: matrix1 = np.lib.stride_tricks.as_strided(matrix, strides=(16, 16))

   In [15]: matrix1
   Out[15]:
   array([[ 0,  2,  4,  6],
          [ 2,  4,  6,  8],
          [ 4,  6,  8, 10],
          [ 6,  8, 10, 12]])

   In [16]: matrix2 = np.lib.stride_tricks.as_strided(matrix, shape=(4, 4), strides=(16, 4))

   In [17]: matrix2
   Out[17]: 
   array([[            0,  4294967296,            1,  8589934592],
          [            2, 12884901888,            3, 17179869184],
          [            4, 21474836480,            5, 25769803776],
          [            6, 30064771072,            7, 34359738368]])

Im ersten Fall ist der Wert der *strides* gerade das Doppelte der
Datenbreite, so dass in einer Zeile von einem Wert zum nächsten jeweils ein
Wert im Array übersprungen wird. Beim Übergang von einer Zeile zur nächsten
wird gegenüber dem Beginn der vorherigen Zeile auch nur um zwei Werte
vorangeschritten, so dass sich das gezeigte Resultat ergibt.

Im zweiten Beispiel wurde ein *stride* gewählt, der nur die Hälfte einer
Datenbreite beträgt. Der berechnete Beginn eines neuen Werts im Speicher liegt
damit nicht an einer Stelle, die einem tatsächlichen Beginn eines Werts
entspricht. Python interpretiert dennoch die erhaltene Information und erzeugt
so das obige Array. In unserem Beispiel erreicht man bei jedem zweiten Wert
wieder eine korrekte Datengrenze. Die Manipulation von *strides* erfordert also
eine gewisse Sorgfalt, und man ist für eventuelle Fehler selbst verantwortlich.

Für die Anwendung ist es wichtig zu wissen, dass die Manipulation der Attribute
``shape`` und ``strides`` nicht die Daten im Speicher verändert. Es wird also
nur eine neue Sicht auf die vorhandenen Daten vermittelt. Dies ist insofern von
Bedeutung als das Kopieren von größeren Datenmengen durchaus mit einem größeren
Zeitaufwand verbunden sein kann. Ein Beispiel für die Durchführung einer
häufigen Matrixoperation durch Anpassung der *strides* werden wir gleich sehen.
Zuvor wollen wir uns aber überzeugen, dass in den obigen Beispielen tatsächlich
kein neues Array erzeugt wurde. 

Dazu setzen wir den oberen linken Eintrag im ursprünglichen Array auf einen neuen
Wert und zeigen, dass diese Änderung auch in den Arrays mit veränderten *strides*
zu sehen ist.

.. sourcecode:: ipython

   In [18]: matrix[0, 0] = 99

   In [19]: matrix
   Out[19]: 
   array([[99,  1,  2,  3],
          [ 4,  5,  6,  7],
          [ 8,  9, 10, 11],
          [12, 13, 14, 15]])

   In [20]: matrix1
   Out[20]: 
   array([[99,  2,  4,  6],
          [ 2,  4,  6,  8],
          [ 4,  6,  8, 10],
          [ 6,  8, 10, 12]])

Eine Matrix lässt sich nun transponieren, ohne dass Matrixelemente im Speicher hin
und her kopiert werden müssen. Dies zeigt das folgende Beispiel, in welchem einfach
die zwei Werte der *strides* vertrauscht werden:

.. sourcecode:: ipython

   In [21]: matrix, matrix.strides
   Out[21]: 
   (array([[99,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]]), (32, 8))


   In [22]: np.lib.stride_tricks.as_strided(matrix, strides=(8, 32))
   Out[22]: 
   array([[99,  4,  8, 12],
          [ 1,  5,  9, 13],
          [ 2,  6, 10, 14],
          [ 3,  7, 11, 15]])

Obwohl die Daten im Speicher nicht verändert wurden, kann man jetzt mit der
transponierten Matrix arbeiten.

.. _arrayerzeugung:

--------------------------
Erzeugung von NumPy-Arrays
--------------------------

NumPy-Arrays lassen sich je nach Bedarf auf verschiedene Arten erzeugen. Die
Basis bildet die ``ndarray``-Methode, auf die man immer zurückgreifen kann.
In den meisten Fällen wird es aber praktischer sein, auf angepasstere Methoden
zurückgreifen, die wir im Folgenden besprechen wollen. 

Um ein mit Nullen aufgefülltes 2×2-Array zu erzeugen, geht man folgendermaßen
vor:

.. sourcecode:: ipython

   In [1]: matrix1 = np.zeros((2, 2))

   In [2]: matrix1, matrix1.dtype
   Out[2]: 
   (array([[ 0.,  0.],
          [ 0.,  0.]]), dtype('float64'))

Das Tupel im Argument gibt dabei die Form des Arrays vor. Wird der Datentyp der
Einträge nicht weiter spezifiziert, so werden Gleitkommazahlen mit einer Länge
von 8 Byte verwendet. Man kann aber auch explizit zum Beispiel Integereinträge
verlangen:

.. sourcecode:: ipython

   In [3]: np.zeros((2, 2), dtype=np.int)
   Out[3]: 
   array([[0, 0],
          [0, 0]])

Will man alle Elemente eines Arrays mit einem konstanten Wert ungleich Null
füllen, so kann man ``ones`` verwenden und das sich ergebende Array mit einem
Faktor multiplizieren.

.. sourcecode:: ipython

   In [4]: 2*np.ones((2, 3))
   Out[4]: 
   array([[ 2.,  2.,  2.],
          [ 2.,  2.,  2.]])

Häufig benötigt man eine Einheitsmatrix, die man mit Hilfe von ``identity``
erhält:

.. sourcecode:: ipython

   In [5]: np.identity(3)
   Out[5]: 
   array([[ 1.,  0.,  0.],
          [ 0.,  1.,  0.],
          [ 0.,  0.,  1.]])

Hierbei wird immer eine Diagonalmatrix erzeugt. Will man dies nicht, so kann
man ``eye`` verwenden, das nicht nur nicht quadratische Arrays erzeugen kann,
sondern auch die Diagonale nach oben oder unten verschieben lässt.

.. sourcecode:: ipython

   In [6]: np.eye(2, 4)
   Out[6]: 
   array([[ 1.,  0.,  0.,  0.],
          [ 0.,  1.,  0.,  0.]])

Zu beachten ist hier, dass die Form des Arrays nicht als Tupel vorgegeben wird,
da ohnehin nur zweidimensionale Arrays erzeugt werden können. Lässt man das
zweite Argument weg, so wird ein quadratisches Array erzeugt. Will man die
Diagonaleinträge verschieben, so gibt man dies mit Hilfe des Parameters ``k`` an:

.. sourcecode:: ipython

   In [7]: np.eye(4, k=1)-np.eye(4, k=-1)
   Out[7]: 
   array([[ 0.,  1.,  0.,  0.],
          [-1.,  0.,  1.,  0.],
          [ 0., -1.,  0.,  1.],
          [ 0.,  0., -1.,  0.]])

Hat man, wie zu Beginn des vorigen Abschnitts beschrieben, eine Matrix in Form
einer Liste mit Unterlisten vorliegen, so kann man diese in ein Array umwandeln:

.. sourcecode:: ipython

   In [8]: np.array([[1, 2], [3, 4]])
   Out[8]: 
   array([[1, 2],
          [3, 4]])

Dies geht zum Beispiel auch, wenn man statt Listen Tupel vorliegen hat.

Lassen sich die Arrayeinträge als Funktion der Indizes ausdrücken, so kann
man die ``fromfunction``-Funktion verwenden, wie in dem folgenden Beispiel
zu sehen ist, das eine Multiplikationstabelle erzeugt.

.. sourcecode:: ipython

   In [9]: np.fromfunction(lambda i, j: (i+1)*(j+1), (6, 6), dtype=np.int)
   Out[9]: 
   array([[ 1,  2,  3,  4,  5,  6],
          [ 2,  4,  6,  8, 10, 12],
          [ 3,  6,  9, 12, 15, 18],
          [ 4,  8, 12, 16, 20, 24],
          [ 5, 10, 15, 20, 25, 30],
          [ 6, 12, 18, 24, 30, 36]])

Diese Funktion ist nicht auf zweidimensionale Arrays beschränkt. 

Bei der Konstruktion von Arrays sind auch Funktionen interessant, die als
Verallgemeinerung der in Python eingebauten Funktion ``range`` angesehen werden
können. Ihr Nutzen ergibt sich vor allem aus der Tatsache, dass man gewissen
Funktionen, den universellen Funktionen oder ufuncs in NumPy, die wir später
noch besprechen werden, ganze Arrays als Argumente übergeben kann. Damit wird
eine besonders effiziente Auswertung dieser Funktionen möglich. 

Eindimensionale Arrays lassen sich mit Hilfe von ``arange``, ``linspace`` und
``logspace`` erzeugen:

.. sourcecode:: ipython

   In [10]: np.arange(1, 2, 0.1)
   Out[10]: array([ 1. ,  1.1,  1.2,  1.3,  1.4,  1.5,  1.6,  1.7,  1.8,  1.9])

   In [11]: np.linspace(1, 2, 11)
   Out[11]: array([ 1. ,  1.1,  1.2,  1.3,  1.4,  1.5,  1.6,  1.7,  1.8,  1.9,  2. ])

   In [12]: np.linspace(1, 2, 4, retstep=True)
   Out[12]: 
   (array([ 1.        ,  1.33333333,  1.66666667,  2.        ]),
    0.3333333333333333)

   In [13]: np.logspace(0, 3, 6)
   Out[13]: 
   array([    1.        ,     3.98107171,    15.84893192,    63.09573445,
            251.18864315,  1000.        ])

   In [14]: np.logspace(0, 3, 4, base=2)
   Out[14]: array([ 1.,  2.,  4.,  8.])

Ähnlich wie bei ``range`` erzeugt ``arange`` aus der Angabe eines Start- und
eines Endwerts sowie einer Schrittweite eine Folge von Werten. Allerdings
können diese auch Gleitkommazahlen sein. Zudem wird statt einer Liste ein Array
erzeugt. Wie bei ``range`` ist der Endwert hierin nicht enthalten.

Häufig möchte man aber statt einer Schrittweite eine Anzahl von Punkten
vorgeben. Dafür ist ``linspace`` eine geeignete Funktion, sofern die
Schrittweite konstant sein soll. Bei Bedarf kann man sich neben dem Array auch
noch die Schrittweite ausgeben lassen. Benötigt man eine logarithmische Skala,
so verwendet man ``logspace``, das den Exponenten linear zwischen einem Start-
und einem Endwert verändert. Die Basis ist standardmäßig 10, sie kann aber durch
Setzen des Parameters ``base`` an spezielle Erfordernisse angepasst werden.

Möchte man eine Funktion auf einem Gitter auswerten und benötigt man dazu
separate Arrays für die x- und y-Werte, so hilft ``meshgrid`` weiter.

.. sourcecode:: ipython

   In [15]: xvals, yvals = np.meshgrid([-1, 0, 1], [2, 3, 4])

   In [16]: xvals
   Out[16]: 
   array([[-1,  0,  1],
          [-1,  0,  1],
          [-1,  0,  1]])

   In [17]: yvals
   Out[17]: 
   array([[2, 2, 2],
          [3, 3, 3],
          [4, 4, 4]])

In diesem Zusammenhang sind auch die Funktionen ``mgrid`` und ``ogrid`` von
Interesse, die wir besprechen werden, wenn wir die Adressierung von Arrays
genauer angesehen haben.

Abschließend wollen wir noch kurz andeuten, wie man ein Array durch Einlesen
von Daten aus einer Datei erhalten kann. Die Datei heiße ``x_von_t.dat``
und habe den folgenden Inhalt::

   # Zeit  Ort
      0.0  0.0
      0.1  0.1
      0.2  0.4
      0.3  0.9

Hierbei zeigt das ``#``-Zeichen in der ersten Zeile an, dass es sich um eine
Kommentarzeile handelt, die nicht in das Array übernommen werden soll. Unter
Verwendung von ``loadtxt`` kann man die Daten nun einlesen:

.. sourcecode:: ipython

   In [18]: np.loadtxt("x_von_t.dat")
   Out[18]: 
   array([[ 0. ,  0. ],
          [ 0.1,  0.1],
          [ 0.2,  0.4],
          [ 0.3,  0.9]])

Bei der ``loadtxt``-Funktion lassen sich zum Beispiel das Kommentarzeichen oder
die Trennzeichen zwischen Einträgen konfigurieren. Noch wesentlich flexibler
ist ``genfromtxt``, das es unter anderem erlaubt, Spaltenüberschriften aus der
Datei zu entnehmen oder mit fehlenden Einträgen umzugehen. Für Details wird auf
die `zugehörige Dokumentation
<http://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html>`_
verwiesen.

-----------------------------
Adressierung von NumPy-Arrays
-----------------------------

Die Adressierungsmöglichkeiten für NumPy-Arrays basieren auf der so genannten
*slice*-Syntax, die wir von Python-Listen her kennen und uns hier noch einmal
kurz in Erinnerung rufen wollen. Einen Ausschnitt aus einer Liste, ein *slice*,
erhält man durch die Notation ``[start:stop:step]``. Hierbei werden ausgehend
von dem Element mit dem Index ``start``  die Elemente bis vor das Element mit dem
Index ``stop`` mit einer Schrittweite ``step`` ausgewählt. Wird die Schrittweite
nicht angegeben, so nimmt ``step`` den Defaultwert ``1`` an. Negative Schrittweiten
führen in der Liste von hinten nach vorne. Fehlen ``start`` und/oder
``stop`` so beginnen die ausgewählten Elemente mit dem ersten Element bzw. enden
mit dem letzten Element. Negative Indexwerte werden vom Ende der Liste her genommen.
Das letzte Element kann also mit dem Index ``-1``, das vorletzten Element mit
dem Index ``-2`` usw. angesprochen werden. Diese Indizierung funktioniert so auch
für NumPy-Arrays wie die folgenden Beispiele zeigen.

.. sourcecode:: ipython

   In [19]: a = np.arange(10)

   In [20]: a
   Out[20]: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

   In [21]: a[:]
   Out[21]: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

   In [22]: a[::2]
   Out[22]: array([0, 2, 4, 6, 8])

   In [23]: a[1:4]
   Out[23]: array([1, 2, 3])

   In [24]: a[6:-2]
   Out[24]: array([6, 7])

   In [25]: a[::-1]
   Out[25]: array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])

Für mehrdimensionale Arrays wird die Notation direkt verallgemeinert. Im Gegensatz
zu der im Abschnitt :ref:`pythonlisten` beschriebenen Notation für Listen von Listen
werden hier die diversen Indexangaben durch Kommas getrennt zusammengefasst. Einige
Beispiele für zweidimensionale Arrays sollen das illustrieren.

.. sourcecode:: ipython

   In [26]: a = np.arange(36).reshape(6, 6)

   In [27]: a
   Out[27]: 
   array([[ 0,  1,  2,  3,  4,  5],
          [ 6,  7,  8,  9, 10, 11],
          [12, 13, 14, 15, 16, 17],
          [18, 19, 20, 21, 22, 23],
          [24, 25, 26, 27, 28, 29],
          [30, 31, 32, 33, 34, 35]])

   In [28]: a[:, :]
   Out[28]: 
   array([[ 0,  1,  2,  3,  4,  5],
          [ 6,  7,  8,  9, 10, 11],
          [12, 13, 14, 15, 16, 17],
          [18, 19, 20, 21, 22, 23],
          [24, 25, 26, 27, 28, 29],
          [30, 31, 32, 33, 34, 35]])

   In [29]: a[2:4, 2:4]
   Out[29]: 
   array([[14, 15],
          [20, 21]])

   In [30]: a[2:4, 3:5]
   Out[30]: 
   array([[15, 16],
          [21, 22]])

   In [31]: a[::2, ::2]
   Out[31]: 
   array([[ 0,  2,  4],
          [12, 14, 16],
          [24, 26, 28]])

   In [32]: a[2::2, ::2]
   Out[32]: 
   array([[12, 14, 16],
          [24, 26, 28]])

   In [33]: a[2:4]
   Out[33]: 
   array([[12, 13, 14, 15, 16, 17],
          [18, 19, 20, 21, 22, 23]])

Wie das letzte Beispiel zeigt, ergänzt NumPy bei fehlenden Indexangaben jeweils
einen Doppelpunkt, so dass alle Elemente ausgewählt werden, die mit den explizit
gemachten Indexangaben konsistent sind.

Will man eine Spalte (oder auch eine Zeile) in einer zweidimensionalen Array auswählen,
so hat man zwei verschiedene Möglichkeiten:

.. sourcecode:: ipython

   In [34]: a[:, 0:1]
   Out[34]: 
   array([[ 0],
          [ 6],
          [12],
          [18],
          [24],
          [30]])

   In [35]: a[:, 0]
   Out[35]: array([ 0,  6, 12, 18, 24, 30])

Im ersten Fall sorgt die für beide Dimensionen vorhandene Indexnotation dafür,
dass ein zweidimensionales Array erzeugt wird, das die Elemente der ersten
Spalte enthält. Im zweiten Fall wird für die zweite Dimension ein fester Index
angegeben, so dass nun ein eindimensionales Array erzeugt wird, die wiederum
aus den Elementen der ersten Spalte besteht.

In einigen NumPy-Methoden gibt es einen Parameter ``axis``, der die Richtung
in dem Array angibt, in der die Methode ausgeführt werden soll. Die Achsennummer
ergibt sich aus der Position der zugehörigen Indexangabe. Wie man aus den obigen
Beispielen entnehmen kann, verläuft die Achse 0 von oben nach unten, während die
Achse 1 von links nach rechts verläuft. Das Aufsummieren von Elementen unserer
Beispielmatrix erfolgt dann mit Hilfe der ``sum``-Methode entweder von oben nach
unten, von links nach rechts oder über alle Elemente.

.. sourcecode:: ipython

   In [36]: a.sum(axis=0)
   Out[36]: array([ 90,  96, 102, 108, 114, 120])

   In [37]: a.sum(axis=1)
   Out[37]: array([ 15,  51,  87, 123, 159, 195])

   In [38]: a.sum()
   Out[38]: 630

Zur Verdeutlichung betrachten wir noch ein dreidimensionales Array.

.. sourcecode:: ipython

   In [39]: b = np.arange(27).reshape(3, 3, 3)

   In [40]: b
   Out[40]: 
   array([[[ 0,  1,  2],
           [ 3,  4,  5],
           [ 6,  7,  8]],

          [[ 9, 10, 11],
           [12, 13, 14],
           [15, 16, 17]],

          [[18, 19, 20],
           [21, 22, 23],
           [24, 25, 26]]])

   In [41]: b[0:1]
   Out[41]: 
   array([[[0, 1, 2],
           [3, 4, 5],
           [6, 7, 8]]])

   In [42]: b[:, 0:1]
   Out[42]: 
   array([[[ 0,  1,  2]],

          [[ 9, 10, 11]],

          [[18, 19, 20]]])

   In [43]: b[:, :, 0:1]
   Out[43]: 
   array([[[ 0],
           [ 3],
           [ 6]],

          [[ 9],
           [12],
           [15]],

          [[18],
           [21],
           [24]]])

   In [44]: b[..., 0:1]
   Out[44]: 
   array([[[ 0],
           [ 3],
           [ 6]],

          [[ 9],
           [12],
           [15]],

          [[18],
           [21],
           [24]]])

Man sieht hier deutlich, wie je nach Wahl der Achse ein entsprechender Schnitt
durch das als Würfel vorstellbare Array gemacht wird. Das letzte Beispiel zeigt
die Benutzung des Auslassungszeichens ``...`` (im Englischen *ellipsis* genannt).
Es steht für die Anzahl von Doppelpunkten, die nötig sind, um die Indizes für
alle Dimensionen zu spezifizieren. Allerdings funktioniert dies nur beim ersten
Auftreten des Auslassungszeichens, da sonst nicht klar ist, wie viele Indexspezifikation
für jedes Auslassungszeichen einzusetzen sind. Alle weiteren Auslassungszeichen
werden daher durch einen einzelnen Doppelpunkt ersetzt.

Weiter oben hatten wir in einem Beispiel gesehen, dass die Angabe eines festen
Index die Dimension des Arrays effektiv um Eins vermindert. Umgekehrt ist es
auch möglich, eine zusätzliche Dimension der Länge Eins hinzuzufügen. Hierzu
dient ``newaxis``, das an der gewünschten Stelle als Index eingesetzt werden kann.
Die folgenden Beispiele zeigen, wie aus einem eindimensionalen Array so zwei
verschiedene zweidimensionale Arrays konstruiert werden können.

.. sourcecode:: ipython

   In [45]: c = np.arange(5)

   In [46]: c
   Out[46]: array([0, 1, 2, 3, 4])

   In [47]: c[:, np.newaxis]
   Out[47]: 
   array([[0],
          [1],
          [2],
          [3],
          [4]])

   In [48]: c[np.newaxis, :]
   Out[48]: array([[0, 1, 2, 3, 4]])

Eine Anwendung hiervon werden wir weiter unten in diesem Kapitel kennenlernen, wenn wir
uns mit der Erweiterung von Arrays auf eine Zielgröße, dem so genannten *broadcasting*
beschäftigen.

Zunächst wollen wir aber noch eine weitere Indizierungsmethode, das so genannte
*fancy indexing*, ansprechen. Obwohl es sich hierbei um ein sehr flexibles und
mächtiges Verfahren handelt, sollte man bedenken, dass hier immer eine Kopie des
Arrays erzeugt wird und nicht einfach nur eine neue Sicht auf bereits vorhandene
Daten. Da Letzteres effizienter ist, sollte man *fancy indexing* in erster Linie in
Situationen einsetzen, in denen das normale Indizieren nicht ausreicht.

Beim *fancy indexing* werden die möglichen Indizes als Arrays oder zum Beispiel als
Liste, nicht jedoch als Tupel, angegeben. Die Elemente können dabei *Integer* oder
*Boolean* sein. Beginnen wir mit dem ersten Fall, wobei wir zunächst von einem
eindimensionalen Array ausgehen.

.. sourcecode:: ipython

   In [49]: a = np.arange(10, 20)

   In [50]: a[[0, 3, 0, 5]]
   Out[50]: array([10, 13, 10, 15])

   In [51]: a[np.array([[0, 2], [1, 4]])]
   Out[51]: 
   array([[10, 12],
          [11, 14]])

Im ersten Fall werden einzelne Arrayelemente durch Angabe der Indizes ausgewählt,
wobei auch Wiederholungen sowie eine nichtmonotone Wahl von Indizes möglich sind.
Sind die Indizes als Array angegeben, so wird ein Array der gleichen Form erzeugt.

Bei der Auswahl von Elementen aus einem mehrdimensionalen Arrays muss man gegebenenfalls
weitere Indexlisten oder -arrays angeben.

.. sourcecode:: ipython

   In [52]: a = np.arange(16).reshape(4, 4)

   In [53]: a
   Out[53]: 
   array([[ 0,  1,  2,  3],
          [ 4,  5,  6,  7],
          [ 8,  9, 10, 11],
          [12, 13, 14, 15]])

   In [54]: a[[0, 1, 2]]
   Out[54]: 
   array([[ 0,  1,  2,  3],
          [ 4,  5,  6,  7],
          [ 8,  9, 10, 11]])

   In [55]: a[[0, 1, 2], [1, 2, 3]]
   Out[55]: array([ 1,  6, 11])

Interessant ist die Verwendung von Indexarrays mit Elementen vom Typ *Boolean*.
Ein solches Indexarray lässt sich zum Beispiel mit Hilfe einer logischen Operation
auf einem Array erzeugen, wie das folgende Beispiel demonstriert. Eine Reihe
von Zufallszahlen soll dabei bei einem Schwellenwert nach unten abgeschnitten
werden.

.. sourcecode:: python
   :linenos:

   threshold = 0.3
   a = np.random.random(12)
   print a
   print "-"*30
   indexarray = a<threshold
   print indexarray
   print "-"*30
   a[indexarray] = threshold
   print a


Damit ergibt sich beispielsweise die folgende Ausgabe::

   [ 0.11859559  0.49034494  0.08552061  0.69204077  0.18406457  0.06819091
     0.36785529  0.16873423  0.44615435  0.57774615  0.54327126  0.57381642]
   ------------------------------
   [ True False  True False  True  True False  True False False False False]
   ------------------------------
   [ 0.3         0.49034494  0.3         0.69204077  0.3         0.3
     0.36785529  0.3         0.44615435  0.57774615  0.54327126  0.57381642]

In Zeile 5 wird ein Array ``indexarray`` erzeugt, das an den Stellen, an denen die Elemente
des Arrays ``a`` kleiner als der Schwellwert sind, den Wahrheitswert ``True``
besitzt. In Zeile 8 werden die auf diese Weise indizierten Elemente dann auf
den Schwellwert gesetzt.  Es sei noch angemerkt, dass sich diese Funktionalität
auch direkt mit der ``clip``-Funktion erreichen lässt.

Im vorigen Beispiel haben wir in der Vergleichsoperation in Zeile 5 ein
Array und ein Skalar miteinander verglichen. Wie kann dies funktionieren? Den
Vergleich zweier Arrays derselben Form kann man sinnvoll elementweise definieren.
Soll ein Array mit einem Skalar verglichen werden, so wird der Skalar von NumPy
zunächst mit gleichen Elementen so erweitert, das ein Array mit der benötigten
Form entsteht. Dieser als *broadcasting* bezeichnete Prozess kommt beispielsweise
auch bei arithmetischen Operationen zum Einsatz. Die beiden folgenden Anweisungen
sind daher äquivalent:

.. sourcecode:: ipython

   In [56]: a = np.arange(5)

   In [57]: a*3
   Out[57]: array([ 0,  3,  6,  9, 12])

   In [58]: a*np.array([3, 3, 3, 3, 3])
   Out[58]: array([ 0,  3,  6,  9, 12])

*Broadcasting* ist genau dann möglich, wenn beim Vergleich der Achsen der
beiden beteiligten Arrays von der letzten Achse beginnend die Länge der Achsen
jeweils gleich ist oder eine Achse die Länge Eins besitzt. Eine Achse der Länge
Eins wird durch Wiederholen der Elemente im erforderlichen Umfang verlängert.
Entsprechendes geschieht beim Hinzufügen von Achsen von vorne, um die
Dimensionen der Arrays identisch zu machen. Wir illustrieren dies an einem
Beispiel.

.. sourcecode:: ipython

   In [59]: a = np.arange(20).reshape(4, 5)

   In [60]: a
   Out[60]: 
   array([[ 0,  1,  2,  3,  4],
          [ 5,  6,  7,  8,  9],
          [10, 11, 12, 13, 14],
          [15, 16, 17, 18, 19]])

   In [61]: a*np.arange(5)
   Out[61]: 
   array([[ 0,  1,  4,  9, 16],
          [ 0,  6, 14, 24, 36],
          [ 0, 11, 24, 39, 56],
          [ 0, 16, 34, 54, 76]])

   In [62]: a*np.arange(4)
   ---------------------------------------------------------------------------
   ValueError                                Traceback (most recent call last)

   <ipython console> in <module>()

   ValueError: operands could not be broadcast together with shapes (4,5) (4,)

Das Array ``a`` hat die Form ``(4, 5)`` und kann daher mit einem Array der Form
``(5,)`` multipliziert werden. Von hinten gerechnet stimmen die Achsenlängen überein,
so dass vorne eine Achse der Länge 4 angefügt werden kann. Ein entsprechend erweitertes
Array hätte folgendes Aussehen:

.. sourcecode:: ipython

   In [63]: np.ones(shape=(4, 5), dtype=int)*np.arange(5)
   Out[63]: 
   array([[0, 1, 2, 3, 4],
          [0, 1, 2, 3, 4],
          [0, 1, 2, 3, 4],
          [0, 1, 2, 3, 4]])

Damit ist ein elementweises Multiplizieren möglich. Im zweiten Beispiel oben haben wir
es neben unserem Array ``a`` der Form ``(4, 5)`` mit einem Array der Form ``(4,)`` zu tun.
In diesem Fall ist kein *broadcasting* möglich, und es kommt zu einer ``ValueError``-Ausnahme.
Anders stellt sich die Situation dar, wenn die Achsenlänge 4 zur Achse 0 gehört und die Achse 1
die Länge 1 besitzt. Dies können wir mit Hilfe von ``newaxis`` erreichen:

.. sourcecode:: ipython

   In [64]: b = np.arange(4)[:, np.newaxis]

   In [65]: b
   Out[65]: 
   array([[0],
          [1],
          [2],
          [3]])

   In [66]: b.shape
   Out[66]: (4, 1)

   In [67]: a*b
   Out[67]: 
   array([[ 0,  0,  0,  0,  0],
          [ 5,  6,  7,  8,  9],
          [20, 22, 24, 26, 28],
          [45, 48, 51, 54, 57]])

----------------------
Universelle Funktionen
----------------------

Im vorigen Unterkapitel haben wir bereits begonnen, mathematische Operationen
mit Arrays zu betrachten. Was passiert, wenn wir versuchen, Funktionen von
Arrays auszuwerten? Für die folgenden Betrachtungen importieren wir zusätzlich
zum ``numpy``-Paket, das in diesem Kapitel immer importiert sein sollte, noch
das ``math``-Modul und versuchen dann, den Sinus eines Arrays auszuwerten.

.. sourcecode:: ipython

   In [1]: import math

   In [2]: math.sin(np.linspace(0, math.pi, 11))
   ---------------------------------------------------------------------------
   TypeError                                 Traceback (most recent call last)

   <ipython console> in <module>()

   TypeError: only length-1 arrays can be converted to Python scalars

Dabei scheitern wir jedoch, da der Sinus aus dem ``math``-Modul nur mit skalaren Größen
umgehen kann. Hätte unser Array nur ein Element enthalten, so wären wir noch erfolgreich
gewesen. Im Beispiel hatten wir jedoch mehr als ein Element, genauer gesagt elf Elemente,
und somit kommt es zu einer ``TypeError``-Ausnahme.

Den Ausweg bietet in diesem Fall das ``numpy``-Paket selbst, das eine eigene Sinusfunktion
zur Verfügung stellt, die in der Lage ist, auch mit Arrays umzugehen.

.. sourcecode:: ipython

   In [3]: np.sin(np.linspace(0, math.pi, 11))
   Out[3]: 
   array([  0.00000000e+00,   3.09016994e-01,   5.87785252e-01,
            8.09016994e-01,   9.51056516e-01,   1.00000000e+00,
            9.51056516e-01,   8.09016994e-01,   5.87785252e-01,
            3.09016994e-01,   1.22460635e-16])

   In [4]: np.sin(math.pi/6*np.arange(12).reshape(2, 6))
   Out[4]: 
   array([[  0.00000000e+00,   5.00000000e-01,   8.66025404e-01,
             1.00000000e+00,   8.66025404e-01,   5.00000000e-01],
          [  1.22460635e-16,  -5.00000000e-01,  -8.66025404e-01,
            -1.00000000e+00,  -8.66025404e-01,  -5.00000000e-01]])

Statt die Kreiszahl aus dem ``math``-Modul zu nehmen, hätten wir sie genauso gut aus dem
``numpy``-Paket nehmen können.

Funktionen wie die gerade benutzte Sinusfunktion aus dem ``numpy``-Paket, die
Arrays als Argumente akzeptieren, werden universelle Funktionen (*universal
function* oder kurz *ufunc*) genannt. Die im ``numpy``-Paket verfügbaren
universellen Funktionen sind in der `NumPy-Dokumentation zu ufuncs
<http://docs.scipy.org/doc/numpy/reference/ufuncs.html#available-ufuncs>`_
aufgeführt. Implementationen von speziellen Funktionen als universelle Funktion
sind im ``scipy``-Paket zu finden. Viele Funktionen in ``scipy.special``,
jedoch nicht alle,  sind als *ufuncs* implementiert.  Als nur eines von vielen
möglichen Beispielen wählen wir die Gammafunktion:

.. sourcecode:: ipython

   In [5]: import scipy.special

   In [6]: scipy.special.gamma(np.linspace(1, 5, 9))
   Out[6]: 
   array([  1.        ,   0.88622693,   1.        ,   1.32934039,
            2.        ,   3.32335097,   6.        ,  11.6317284 ,  24.        ])

Gelegentlich benötigt man eine Funktion von zwei Variablen auf einem Gitter.
Man könnte hierzu die ``meshgrid``-Funktion heranziehen, die wir im Abschnitt
:ref:`arrayerzeugung` erwähnt hatten.  Da man dort die einzelnen Gitterpunkte
explizit angegeben muss, ist es häufig bequemer, eine ``mgrid``-Gitter zu
verwenden.

.. sourcecode:: ipython

   In [7]: np.mgrid[0:3, 0:3]
   Out[7]: 
   array([[[0, 0, 0],
           [1, 1, 1],
           [2, 2, 2]],

          [[0, 1, 2],
           [0, 1, 2],
           [0, 1, 2]]])

   In [8]: np.mgrid[0:3:7j, 0:3:7j]
   Out[8]: 
   array([[[ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
           [ 1. ,  1. ,  1. ,  1. ,  1. ,  1. ,  1. ],
           [ 1.5,  1.5,  1.5,  1.5,  1.5,  1.5,  1.5],
           [ 2. ,  2. ,  2. ,  2. ,  2. ,  2. ,  2. ],
           [ 2.5,  2.5,  2.5,  2.5,  2.5,  2.5,  2.5],
           [ 3. ,  3. ,  3. ,  3. ,  3. ,  3. ,  3. ]],

          [[ 0. ,  0.5,  1. ,  1.5,  2. ,  2.5,  3. ],
           [ 0. ,  0.5,  1. ,  1.5,  2. ,  2.5,  3. ],
           [ 0. ,  0.5,  1. ,  1.5,  2. ,  2.5,  3. ],
           [ 0. ,  0.5,  1. ,  1.5,  2. ,  2.5,  3. ],
           [ 0. ,  0.5,  1. ,  1.5,  2. ,  2.5,  3. ],
           [ 0. ,  0.5,  1. ,  1.5,  2. ,  2.5,  3. ],
           [ 0. ,  0.5,  1. ,  1.5,  2. ,  2.5,  3. ]]])

Man beachte, dass im zweiten Fall das dritte Element in der *slice*-Syntax imaginär ist. Damit wird
angedeutet, dass nicht die Schrittweite gemeint ist, sondern die Anzahl der Werte im durch die
ersten beiden Zahlen spezifizierten Intervall. Unter Verwendung des *Broadcasting* genügt auch
ein ``ogrid``-Gitter.

.. sourcecode:: ipython

   In [9]: np.ogrid[0:3:7j, 0:3:7j]
   Out[9]: 
   [array([[ 0. ],
          [ 0.5],
          [ 1. ],
          [ 1.5],
          [ 2. ],
          [ 2.5],
          [ 3. ]]),
    array([[ 0. ,  0.5,  1. ,  1.5,  2. ,  2.5,  3. ]])]

Eine Anwendung bei der Berechnung von Kugelflächenfunktionen könnte folgendermaßen aussehen [#sph_harm]_.

.. sourcecode:: python

   import numpy as np
   import scipy.special

   thetas, phis = np.ogrid[0:np.pi:5j, 0:2*np.pi:9j]
   n, m = 5, 2
   resultat = scipy.special.sph_harm(m, n, phis, thetas)

   print resultat

Wir verzichten darauf, das Ergebnis anzugeben, da es keine weiteren Einsichten
bringt, außer dass tatsächlich ein 5×9-Array erzeugt wird. Abschließend sei
noch angemerkt, dass der Aufruf von ``sph_harm`` nicht funktioniert, wenn man
``phis`` und ``thetas`` folgendermaßen definiert:

.. sourcecode:: python

   thetas = np.linspace(0, np.pi, 5)
   phis = np.linspace(0, 2*np.pi, 9)

Diese Definition würde kein *Broadcasting* erlauben. Hätten beide Arrays die
gleiche Länge, würde die Kugelflächenfunktion zwar ausgewertet werden, aber man
würde kein zweidimensionales Array sondern nur ein eindimensionales Array
erhalten.

Es ist nicht nur praktisch, Funktionen von Arrays direkt berechnen zu können,
sondern es spart häufig auch Rechenzeit. Wir wollen dies an einem Beispiel
illustrieren.

.. sourcecode:: ipython

   In [10]: nmax = 100000
   
   In [11]: %%timeit
      ...: for n in range(nmax):
      ...:     x = 2*math.pi*n/(nmax-1)
      ...:     y = math.sin(x)
      ...: 
   10 loops, best of 3: 33.2 ms per loop
   
   In [12]: %%timeit
      ...: x = np.linspace(0, 2*np.pi, nmax)
      ...: y = np.sin(x)
      ...: 
   100 loops, best of 3: 2.96 ms per loop
   
   In [13]: %%timeit
      ...: prefactor = 2*math.pi/(nmax-1)
      ...: for n in range(nmax):
      ...:     y = math.sin(prefactor*n)
      ...: 
   100 loops, best of 3: 16.5 ms per loop
   
Die angegebenen Rechenzeiten sind natürlich von der Hardware abhängig, auf der
der Code ausgeführt wurde. Daher kommt es statt auf die Absolutwerte auf
Verhältnisse von Rechenzeiten zueinander an. Dabei zeigt sich, dass die im
ersten Codestück programmierte explizite ``for``-Schleife etwa elfmal
langsamer ist als das zweite Codestück, das eine universelle Funktion
verwendet. Ein Anteil dieses Geschwindigkeitsvorteils ergibt sich daraus, dass
in der ``for``-Schleife unnötige Rechenarbeit geleistet wird. Zieht man die
Berechnung des konstanten Faktors ``prefactor`` aus der Schleife heraus, so
wird die Rechenzeit immerhin etwas mehr als halbiert. Dennoch ist die
Verwendung der universellen Funktion deutlich schneller. Der
Geschwindigkeitsvorteil ergibt sich allerdings erst bei hinreichend großen
Arrays. Bei kleinen Arrays kann dagegen der mit der Verwaltung der Arrays
verbundene Aufwand überwiegen.

Abschließend sei noch angemerkt, dass es sich wegen der genannten Rechenzeitvorteile
lohnt, einen Blick in die Liste der von NumPy zur Verfügung gestellten 
`mathematischen Funktionen <http://docs.scipy.org/doc/numpy/reference/routines.math.html>`_
zu werfen. Möchte man zum Beispiel die Summe der Elemente eines Arrays berechnen, so verwendet
man sinnvollerweise die ``sum``-Funktion von NumPy.

---------------
Lineare Algebra
---------------

Physikalische Fragestellungen, die sich mit Hilfe von Vektoren und Matrizen formulieren lassen,
benötigen zur Lösung sehr häufig Methoden der linearen Algebra. NumPy leistet hierbei Unterstützung,
insbesondere mit dem ``linalg``-Paket. Im Folgenden gehen wir auf einige Aspekte ein, ohne 
Vollständigkeit anzustreben. Daher empfiehlt es sich, auch einen Blick in den
`entsprechenden Abschnitt der Dokumentation <http://docs.scipy.org/doc/numpy/reference/routines.linalg.html>`_
zu werfen. Zunächst importieren wir die Module, die wir für die Beispiele dieses Kapitels benötigen:

.. code-block:: ipython

   In [1]: import numpy as np

   In [2]: import numpy.linalg as LA

Beim Arbeiten mit Matrizen und NumPy muss man immer bedenken, dass der Multiplikationsoperator `*`
nicht für eine Matrixmultiplikation steht. Vielmehr wird damit eine elementweise Multiplikation
ausgeführt:

.. code-block:: ipython

   In [3]: a1 = np.array([[1, -3], [-2, 5]])

   In [4]: a1
   Out[4]: 
   array([[ 1, -3],
          [-2,  5]])

   In [5]: a2 = np.array([[3, -6], [2, -1]])

   In [6]: a2
   Out[6]: 
   array([[ 3, -6],
          [ 2, -1]])

   In [7]: a1*a2
   Out[7]: 
   array([[ 3, 18],
          [-4, -5]])

Möchte man dagegen eine Matrixmultiplikation ausführen, so verwendet man das ``dot``-Produkt:

.. code-block:: ipython

   In [8]: np.dot(a1, a2)
   Out[8]: 
   array([[-3, -3],
          [ 4,  7]])

Man könnte die Norm eines Vektors ebenfalls mit Hilfe des ``dot``-Produkts bestimmen. Es bietet
sich jedoch an, hierzu direkt die ``norm``-Funktion zu verwenden:

.. code-block:: ipython

   In [9]: vec = np.array([1, -2, 3])

   In [10]: LA.norm(vec)
   Out[10]: 3.7416573867739413

   In [11]: LA.norm(vec)**2
   Out[11]: 14.0

Als nächstes wollen wir ein inhomogenes lineares Gleichungssystem ``ax = b`` lösen, wobei die
Matrix ``a`` und der Vektor ``b`` gegeben sind und der Vektor ``x`` gesucht ist.

.. code-block:: ipython

   In [12]: a = np.array([[2, -1], [-3, 2]])

   In [13]: b = np.array([1, 2])

   In [14]: LA.det(a)
   Out[14]: 0.99999999999999978

   In [15]: np.dot(LA.inv(a), b)
   Out[15]: array([ 4.,  7.])

In Eingabe 14 haben wir zunächst überprüft, dass die Determinante der Matrix
``a`` ungleich Null ist, so dass die invertierte Matrix existiert. Anschließend
haben wir den Vektor ``b`` von links mit der Inversen von ``a`` multipliziert,
um den Lösungsvektor zu erhalten. Allerdings erfolgt die numerische Lösung
eines inhomogenen linearen Gleichungssystems normalerweise nicht über eine
Inversion der Matrix, sondern mit Hilfe einer geeignet durchgeführten Gauß-Elimination.
NumPy stell hierzu die ``solve``-Funktion zur Verfügung:

.. code-block:: ipython

   In [16]: LA.solve(a, b)
   Out[16]: array([ 4.,  7.])

Eine nicht invertierbare Matrix führt hier wie auch bei der Bestimmung der Determinante
auf eine ``LinAlgError``-Ausnahme mit dem Hinweis auf eine singuläre Matrix.

Eine häufig vorkommende Problemstellung im Bereich der linearen Algebra sind
Eigenwertprobleme. Die ``eig``-Funktion bestimmt rechtsseitige Eigenvektoren und
die zugehörigen Eigenwerte für beliebige quadratische Matrizen:

.. code-block:: ipython

   In [17]: a = np.array([[1, 3], [4, -1]])

   In [18]: evals, evecs = LA.eig(a)

   In [19]: evals
   Out[19]: array([ 3.60555128, -3.60555128])

   In [20]: evecs
   Out[20]: 
   array([[ 0.75499722, -0.54580557],
          [ 0.65572799,  0.83791185]])

   In [21]: for n in range(evecs.shape[0]):
       print(np.dot(a, evecs[:, n]), evals[n]*evecs[:, n])
   Out[21]: 
   [ 2.72218119  2.36426089] [ 2.72218119  2.36426089]
   [ 1.96792999 -3.02113415] [ 1.96792999 -3.02113415]

Die Ausgabe am Ende zeigt, dass die Eigenvektoren und -werte in der Tat korrekt sind.
Benötigt man nur die Eigenwerte einer Matrix, so kann man durch Benutzung der
``eigvals``-Funktion Rechenzeit sparen.

Für die Lösung eines Eigenwertproblems von symmetrischen oder hermiteschen [#hermitesch]_
Matrizen gibt es die Funktionen ``eigh`` und ``eigvalsh``, bei denen es genügt,
nur die obere oder die untere Hälfte der Matrix zu spezifizieren. Viel
wichtiger ist jedoch, dass diese Funktionen einen erheblichen Zeitvorteil
bieten können:

.. code-block:: ipython

   In [22]: a = np.random.random(250000).reshape(500, 500)

   In [23]: a = a+a.T

   In [24]: %timeit LA.eig(a)
   1 loops, best of 3: 736 ms per loop

   In [25]: %timeit LA.eigh(a)
   10 loops, best of 3: 208 ms per loop

Hier wird in Eingabe 23 durch Addition der Transponierten eine symmetrische
Matrix erzeugt, so dass die beiden Funktionen ``eig`` und ``eigh`` mit der
gleichen Matrix arbeiten. Die Funktion ``eigh`` ist in diesem Beispiel immerhin
um mehr als einen Faktor 3 schneller.

.. [#array] Wir verwenden im Folgenden das englische Wort *Array*, um damit den ``ndarray``-Datentyp
            aus NumPy zu bezeichnen. Ein Grund dafür, nicht von Matrizen zu sprechen, besteht darin,
            dass sich Arrays nicht notwendigerweise wie Matrizen verhalten. So entspricht das Produkt
            von zwei Arrays im Allgemeinen nicht dem Matrixprodukt.
.. [#sph_harm] Im ``scipy``-Modul sind die Winkel im Vergleich zur üblichen Konvention gerade vertauscht
            benannt (siehe auch die `Dokumentation zur Funktion sph_harm <http://docs.scipy.org/doc/scipy/reference/generated/scipy.special.sph_harm.html#scipy.special.sph_harm>`_).
.. [#hermitesch] Eine hermitesche Matrix geht beim Transponieren in die konjugiert komplexe Matrix über:
            :math:`a_{ij}=a_{ji}^*`.
