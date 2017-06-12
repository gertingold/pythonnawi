**********
Einführung
**********

Die Vorlesung »Python für Naturwissenschaftler« baut auf der Vorlesung
»Einführung in das Programmieren für Physiker und Naturwissenschaftler«, im
Folgenden kurz Einführungsvorlesung genannt, auf. Sie setzt daher Kenntnisse
der Programmiersprache Python, wie Sie in der Einführungsvorlesung vermittelt
werden, voraus. Gegebenenfalls wird empfohlen, sich Grundkenntnisse von Python
mit Hilfe des Manuskripts zur Einführungsvorlesung anzueignen oder das
Manuskript zu verwenden, um Kenntnisse aufzufrischen. 

Die Einführungsvorlesung beschränkt sich bewusst weitestgehend auf
Sprachelemente von Python, die in ähnlicher Form auch in anderen, für den
Naturwissenschaftler wichtigen Programmiersprachen, wie C oder Fortran,
verfügbar sind. Diese Beschränkung wird in der Vorlesung »Python für
Naturwissenschaftler« fallengelassen, so dass einige weitere wichtige
Sprachelemente besprochen werden können. Dabei wird jedoch keine
Vollständigkeit angestrebt. Vielmehr soll auch Raum bleiben, um erstens eine
etwas detailliertere Einführung in die zentrale numerische Bibliothek in
Python, nämlich NumPy, zu geben und zweitens einige für die Codeentwicklung
relevante Werkzeuge zu besprechen. 

Aus Zeitgründen werden wir uns bei Letzteren auf Versionskontrollsysteme,
auf Verfahren zum systematischen und nachvollziehbaren Testen von Programmen und auf
Verfahren zur Bestimmung der Laufzeiten verschiedener Programmteile beschränken.
Einige dieser Techniken werden wir zwar konkret im Zusammenspiel mit Python
kennenlernen, sie sind aber auch auf andere Programmiersprachen übertragbar.
Auch wenn solche Techniken häufig als unnötiger Aufwand empfunden
werden, können sie wesentlich zur Qualität wissenschaftlichen Rechnens beitragen.
[#arxiv1210.0530]_

Die im Manuskript gezeigten Code-Beispiele sind für die Verwendung mit einer
aktuellen Version von Python 3 vorgesehen. Ein Großteil der Beispiele ist
aber auch unter Python 2.7 lauffähig oder lässt sich durch kleinere Anpassungen
lauffähig machen.

==================
Verwendete Symbole
==================

``In [1]:`` stellt den Prompt des IPython-Interpreters dar, wobei statt der ``1``
auch eine andere Eingabenummer stehen kann.

``Out[1]:`` weist auf die Ausgabe des IPython-Interpreters zur Eingabe ``In [1]:`` hin.

``...:`` wird im IPython-Interpreter als Prompt verwendet, wenn die Eingabe fortzusetzen
ist, zum Beispiel im Rahmen einer Schleife. Diese Art der Eingabe kann sich über
mehrere Zeilen hinziehen. Zum Beenden wird die :kbd:`EINGABE`-Taste ohne zuvorige 
Eingabe von Text verwendet.

``$`` steht für den Prompt, also die Eingabeaufforderung, der Shell beim
kommandozeilenbasierten Arbeiten in einem Terminalfenster.

|weiterfuehrend| Dieses Symbol kennzeichnet weiterführende Anmerkungen, die sich unter
anderem auf speziellere Aspekte der Programmiersprache Python beziehen.

==========
Danke an …
==========

* … die Hörerinnen und Hörer der Vorlesung „Python für Naturwissenschaftler“, deren
  Fragen und Anregungen in diesem Manuskript ihren Niederschlag fanden;

* Michael Hartmann, Oliver Kanschat-Krebs und Benjamin Spreng für eine Reihe von
  Kommentaren zu diesem Manuskript.


.. [#arxiv1210.0530] `arXiv:1210.0530 <http://de.arxiv.org/abs/1210.0530/>`_

.. |weiterfuehrend| image:: images/symbols/weiterfuehrend.*
           :height: 1em
