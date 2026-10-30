import json,os
Q=[];n=[0]
def add(goal,level,type,prompt,expl,**k):
    n[0]+=1;q={"id":f"O{n[0]:03d}","goal":goal,"level":level,"type":type,"prompt":prompt};q.update(k);q["explanation"]=expl;Q.append(q)
import random;R=random.Random(9)
def mc(g,l,p,o,a,e):
    c=o[a];o=o[:];R.shuffle(o);add(g,l,"mc",p,e,options=o,answer=o.index(c))
def tf(g,l,p,a,e):add(g,l,"tf",p,e,answer=a)
def num(g,l,p,a,t,u,e):add(g,l,"num",p,e,answer=a,tolerance=t,unit=u)
def order(g,l,p,i,e):add(g,l,"order",p,e,items=i)
def match(g,l,p,pr,e):add(g,l,"match",p,e,pairs=pr)
def cloze(g,l,p,t,gp,e):add(g,l,"cloze",p,e,text=t,gaps=gp)
def sel(o,a):
    c=o[a];o=o[:];R.shuffle(o);return {"options":o,"answer":o.index(c)}
# 1
match(1,"G","Ordne jedem Körper die passende Beschreibung zu.",[["Sonne","selbstleuchtend: ein Stern, der sein Licht selbst erzeugt"],["Mond","beleuchtet: wirft Sonnenlicht zurück"],["Kerzenflamme","selbstleuchtend: eine heisse Flamme"],["Buchseite","beleuchtet: wirft Lampenlicht zurück"]],"Selbstleuchtende Körper erzeugen Licht selbst, beleuchtete werfen fremdes Licht zurück.")
tf(1,"G","Der Planet Venus leuchtet am Abendhimmel selbst.",False,"Falsch. Venus wirft das Sonnenlicht zurück; sie ist ein beleuchteter Körper.")
mc(1,"E","Ein Velorückstrahler leuchtet nachts hell auf. Warum ist er trotzdem ein beleuchteter Körper?",["Er leuchtet nur, solange Licht von aussen auf ihn fällt.","Er speichert tagsüber Licht.","Er ist rot.","Er besteht aus Kunststoff."],0,"Ohne Scheinwerfer bleibt er dunkel. Er wirft nur fremdes Licht zurück.")
mc(1,"G","Welcher Körper ist selbstleuchtend?",["Glühender Draht einer Lampe","Vollmond","Spiegel","Schnee in der Sonne"],0,"Der Draht ist so heiss, dass er selbst Licht aussendet.")
# 2
tf(2,"G","Licht breitet sich in Luft, Wasser oder Glas (immer im gleichen Stoff) geradlinig aus.",True,"Richtig. Deshalb zeichnen wir Licht als Strahlen mit dem Lineal.")
mc(2,"G","Was zeigt ein gezeichneter Lichtstrahl (Linie mit Pfeil)?",["Die Richtung, in die sich das Licht ausbreitet","Die Farbe des Lichts","Die Helligkeit","Die Wärme"],0,"Ein Lichtstrahl ist ein Modell: eine gerade Linie mit Pfeil für die Ausbreitungsrichtung.")
mc(2,"E","Welche Beobachtung zeigt, dass sich Licht geradlinig ausbreitet?",["Schatten haben scharfe Ränder, die zur Form des Körpers passen.","Licht ist schnell.","Licht wird warm.","Spiegel glänzen."],0,"Die äussersten Lichtstrahlen gehen gerade an den Kanten vorbei; so entsteht ein Schatten in der Form des Körpers.")
# 3
cloze(3,"G","Ergänze.","Wir sehen ein Buch, weil es {0} zurückwirft, das dann in unser {1} gelangt.",[sel(["Licht","Wärme","Schatten"],0),sel(["Auge","Ohr","Gehirn"],0)],"Ohne Licht, das ins Auge fällt, sehen wir nichts.")
tf(3,"G","Das Auge schickt Strahlen aus, die auf Gegenstände treffen.",False,"Falsch. Licht gelangt vom Gegenstand ins Auge, nicht umgekehrt.")
mc(3,"E","In einem völlig dunklen Raum siehst du deine weisse Wand nicht. Warum?",["Kein Licht fällt auf die Wand, also wirft sie keines ins Auge.","Die Wand ist zu weit weg.","Weiss leuchtet nur am Tag selbst.","Das Auge ist zu müde."],0,"Beleuchtete Körper sehen wir nur, wenn Licht auf sie fällt und von ihnen ins Auge gelangt.")
# 4
mc(4,"G","Wo entsteht ein Kernschatten?",["Wo von keiner Lichtquelle Licht hinkommt","Wo von einer Lichtquelle Licht hinkommt","Direkt hinter jeder Lampe","Nur bei farbigem Licht"],0,"Im Kernschatten ist es ganz dunkel; im Halbschatten kommt Licht von einer Lampe an.")
tf(4,"G","Bei einer einzigen punktförmigen Lampe (sehr kleiner Lichtpunkt) gibt es keinen Halbschatten.",True,"Richtig. Halbschatten entsteht erst bei mehreren Lampen oder einer grossen Lichtquelle (z. B. Leuchtstoffröhre).")
mc(4,"E","Ein Stab wird von zwei Lampen beleuchtet. Du schiebst die Wand, auf die der Schatten fällt, weiter vom Stab weg. Was passiert mit dem Kernschatten?",["Er wird kleiner.","Er wird grösser.","Er bleibt gleich.","Er wird zum Halbschatten der anderen Lampe."],0,"Die äussersten Lichtstrahlen der beiden Lampen kreuzen sich hinter dem Stab. Darum wird der Kernschatten weiter hinten schmaler.")
mc(4,"E","Ein Stab wird von zwei Lampen beleuchtet: Lampe L1 ist unten, Lampe L2 oben. Welche Lampe beleuchtet den unteren Halbschatten?",["L1, die untere Lampe","L2, die obere Lampe","Beide","Keine"],0,"Licht von L2 fällt schräg nach unten und wird vom Stab blockiert. Das Licht von L1 gelangt von unten am Stab vorbei.")
# 5
order(5,"G","Ordne die Himmelskörper bei einer Sonnenfinsternis von links (Sonne) nach rechts.",["Sonne","Mond","Erde"],"Der Mond steht zwischen Sonne und Erde; sein Schatten fällt auf die Erde.")
mc(5,"G","Bei welcher Mondphase kann eine Mondfinsternis stattfinden?",["Vollmond","Neumond","Halbmond","Bei jeder Phase"],0,"Die Erde steht zwischen Sonne und Mond; dann ist Vollmond.")
mc(5,"E","Warum sieht man eine totale Sonnenfinsternis nur in einem schmalen Streifen der Erde?",["Der Kernschatten des kleinen Mondes ist auf der Erde nur ein kleiner Fleck.","Die Sonne ist kleiner als der Mond.","Nur dort ist Tag.","Die Erde dreht sich zu schnell."],0,"Ausserhalb des Kernschattens liegt man im Halbschatten und sieht nur eine teilweise Sonnenfinsternis: Die Sonne ist nur zum Teil verdeckt.")
tf(5,"E","Bei einer Mondfinsternis liegt der Mond im Kernschatten der Erde.",True,"Richtig. Darum sieht man sie überall auf der Erde, wo gerade Nacht ist.")
# 6
cloze(6,"G","Ergänze das Reflexionsgesetz.","Der Einfallswinkel ist {0} gross wie der Reflexionswinkel. Beide Winkel misst man zum {1}.",[sel(["gleich","doppelt","halb"],0),sel(["Lot","Spiegel","Auge"],0)],"Einfallswinkel α = Reflexionswinkel α’. Das Lot steht senkrecht auf dem Spiegel.")
num(6,"G","Ein Strahl trifft auf einen Spiegel. Der Winkel zwischen Strahl und Lot beträgt 35°. Wie gross ist der Reflexionswinkel?",35,0,"°","Einfallswinkel = Reflexionswinkel.")
num(6,"E","Ein Strahl trifft auf einen Spiegel. Der Winkel zwischen Strahl und Spiegel beträgt 20°. Wie gross ist der Einfallswinkel?",70,0,"°","Gemessen wird zum Lot: 90° − 20° = 70°.")
num(6,"E","Der Winkel zwischen einfallendem und reflektiertem Strahl beträgt 100°. Wie gross ist der Einfallswinkel?",50,0,"°","Das Lot teilt den Winkel in zwei gleiche Hälften: 100° : 2 = 50°.")
# 7
tf(7,"G","Das Spiegelbild liegt gleich weit hinter dem Spiegel wie der Gegenstand davor.",True,"Richtig. Gegenstand und Bild liegen spiegelbildlich, gleich weit vom Spiegel entfernt.")
mc(7,"G","Warum heisst das Bild in einem ebenen Spiegel virtuell (scheinbar)?",["Hinter dem Spiegel kommt kein Licht hin; man kann es nicht auf einer Wand oder einem Blatt auffangen.","Es ist farbig.","Es steht auf dem Kopf.","Es ist kleiner als der Gegenstand."],0,"Die Strahlen sehen nur so aus, als kämen sie von hinter dem Spiegel.")
num(7,"E","Lena ist 1.60 m gross. Wie hoch muss ein Wandspiegel mindestens sein, damit sie sich ganz sieht? Gib die Antwort in cm an.",80,0,"cm","Der Spiegel muss halb so gross sein wie die Person.")
mc(7,"E","Tim geht einige Schritte vom Spiegel weg. Wie ändert sich die nötige Mindestgrösse des Spiegels?",["Sie bleibt gleich.","Sie wird grösser.","Sie wird kleiner.","Sie wird doppelt so gross."],0,"Die Reflexionspunkte liegen immer in der Mitte zwischen dem Auge und dem Kopf bzw. den Füssen.")
# 8
match(8,"G","Ordne zu.",[["Hohlspiegel","nach innen gewölbt, sammelt Licht"],["Wölbspiegel","nach aussen gewölbt, streut Licht"],["Brennpunkt F","Hier treffen sich achsenparallele Strahlen (parallel zur Achse) nach dem Hohlspiegel."]],"Hohlspiegel = Konkavspiegel (nach innen gewölbt), Wölbspiegel = Konvexspiegel (nach aussen gewölbt).")
mc(8,"G","Wo setzt man einen Wölbspiegel ein?",["Als Verkehrsspiegel an unübersichtlichen Kreuzungen","Im Scheinwerfer, um Licht zu bündeln","Als Schminkspiegel zum Vergrössern","In der Taschenlampe"],0,"Ein Wölbspiegel zeigt einen grossen Bereich.")
tf(8,"E","Achsenparallele Strahlen (parallel zur Achse) laufen nach einem Wölbspiegel so auseinander, als kämen sie von einem Punkt hinter dem Spiegel.",True,"Richtig. Dieser Punkt ist der scheinbare Brennpunkt (die Strahlen treffen sich dort nicht wirklich).")
# 9
mc(9,"G","Licht geht schräg von Luft in Wasser. Wie wird es gebrochen?",["Zum Lot hin","Vom Lot weg","Gar nicht","Es wird ganz reflektiert"],0,"Ins optisch dichtere Medium (Stoff) wird der Strahl zum Lot hin gebrochen.")
tf(9,"G","Ein Lichtstrahl, der senkrecht auf eine Wasseroberfläche trifft, wird nicht abgelenkt.",True,"Richtig. Trifft der Strahl senkrecht auf (Einfallswinkel 0°), geht er gerade weiter.")
mc(9,"E","Warum sieht ein Strohhalm im Glas an der Wasseroberfläche geknickt aus?",["Das Licht vom Halm wird beim Übergang Wasser→Luft geknickt; der Teil im Wasser wirkt höher.","Das Wasser biegt den Halm.","Das Glas wirkt wie ein Spiegel.","Licht ist im Wasser schneller."],0,"Das Auge verlängert die Strahlen geradlinig zurück, das Bild liegt höher (Hebung).")
mc(9,"E","Ein Strahl geht durch eine dicke Glasscheibe (Vorder- und Rückseite parallel). Wie verlässt er sie?",["In die gleiche Richtung wie vorher, aber etwas seitlich verschoben","Zum Lot hin geknickt","Senkrecht zur Platte","Gar nicht"],0,"Die zwei Brechungen heben sich auf; der Strahl wird nur seitlich versetzt.")
# 10
cloze(10,"G","Ergänze.","Totalreflexion gibt es nur, wenn Licht vom optisch {0} Medium (Stoff) ins optisch {1} will und der Einfallswinkel gross genug ist.",[sel(["dichteren","dünneren"],0),sel(["dünnere","dichtere"],0)],"Zum Beispiel von Glas in Luft.")
mc(10,"G","Wo wird Totalreflexion technisch genutzt?",["In Glasfaserkabeln","Im Wölbspiegel","In der Lupe","In der Lochkamera"],0,"Das Licht wird in der Faser immer wieder an der Wand total reflektiert.")
mc(10,"E","Warum hat eine Glasfaser einen Mantel?",["Der Mantel ist optisch dünner als der Kern; darum gibt es an der Grenze Totalreflexion.","Der Mantel färbt das Licht.","Der Mantel macht das Kabel warm.","Der Mantel ist ein Spiegel aus Metall."],0,"Totalreflexion braucht den Übergang ins optisch dünnere Medium (Stoff).")
tf(10,"E","Eine Fata Morgana entsteht durch Totalreflexion des Lichts an einer heissen, optisch dünneren Luftschicht über dem Boden.",True,"Richtig. Das Licht vom Himmel wird an der heissen Luftschicht total reflektiert. Darum sieht man den Himmel am Boden, und es wirkt wie eine Wasserfläche.")
# 11
match(11,"G","Ordne zu.",[["Sammellinse","in der Mitte dicker (konvex)"],["Zerstreuungslinse","in der Mitte dünner (konkav)"],["Brennweite f","Abstand Linsenmitte bis Brennpunkt"]],"Konvex sammelt, konkav zerstreut.")
mc(11,"G","Wohin läuft ein achsenparalleler Strahl (parallel zur Achse) nach einer Sammellinse?",["Durch den Brennpunkt F","Parallel weiter","Zurück zur Lampe","Weg von der Achse"],0,"Achsenparallele Strahlen werden im Brennpunkt gesammelt.")
mc(11,"E","Wie kannst du ohne Hilfsmittel eine Sammellinse von einer Zerstreuungslinse unterscheiden?",["Mit den Fingern prüfen, ob die Linse in der Mitte oder am Rand dicker ist","Am Gewicht","An der Farbe","Sie riechen verschieden."],0,"Sammellinsen (konvex) sind in der Mitte dicker, Zerstreuungslinsen (konkav) am Rand.")
tf(11,"E","Je stärker eine Sammellinse gewölbt ist, desto kürzer ist ihre Brennweite.",True,"Richtig. Eine stark gewölbte Linse bricht das Licht stärker.")
# 12
mc(12,"G","Wie verwendet man eine Lupe richtig?",["Den Gegenstand näher an der Lupe halten als der Brennpunkt","Den Gegenstand weiter von der Lupe weg halten als der Brennpunkt","Die Lupe ans Ohr halten","Nur bei Dunkelheit"],0,"Dann entsteht ein vergrössertes Bild, das nicht auf dem Kopf steht.")
match(12,"G","Ordne die Teile der Kamera ihrer Aufgabe zu.",[["Linse (Objektiv)","erzeugt das Bild"],["Blende","regelt, wie viel Licht hineinkommt"],["Bildsensor","nimmt das Bild auf"],["Speicherkarte","speichert die Fotos"]],"Die Linse erzeugt das Bild, die Blende regelt die Lichtmenge, der Sensor nimmt das Bild auf, die Speicherkarte speichert es.")
mc(12,"E","Bei schwachem Licht soll ein Foto hell genug werden. Was stellst du ein?",["Die Blende weiter öffnen","Die Blende schliessen","Den Bildsensor entfernen","Die Linse abdecken"],0,"Ist die Blende weit offen, kommt mehr Licht auf den Sensor.")
# 13
match(13,"G","Ordne die Teile des Auges den Teilen der Kamera zu.",[["Augenlinse","Objektiv"],["Pupille (Loch in der Regenbogenhaut)","Blende"],["Netzhaut","Bildsensor"]],"Auge und Kamera sind ähnlich aufgebaut.")
mc(13,"E","Was macht die Pupille, wenn du aus der Sonne in einen dunklen Raum kommst?",["Sie wird grösser.","Sie wird kleiner.","Sie bleibt gleich.","Sie schliesst sich."],0,"Die Pupille wird grösser, wie eine weit offene Blende. So kommt mehr Licht ins Auge.")
tf(13,"E","Auf der Netzhaut entsteht ein Bild, das auf dem Kopf steht.",True,"Richtig. Das Gehirn dreht es so, dass wir richtig sehen.")
# 14
cloze(14,"G","Ergänze die additive Farbmischung (farbiges Licht überlagert sich).","Rot + Grün = {0}, Rot + Blau = {1}, Rot + Grün + Blau = {2}.",[sel(["Gelb","Cyan (Hellblau)","Magenta (Pink-Lila)"],0),sel(["Magenta (Pink-Lila)","Gelb","Cyan (Hellblau)"],0),sel(["Weiss","Schwarz","Braun"],0)],"Grundfarben des Lichts: Rot, Grün, Blau.")
mc(14,"E","Auf einem Bildschirm leuchtet Gelb. Welche kleinen Leuchtpunkte (Pixel) leuchten?",["Rot und Grün","Rot und Blau","Grün und Blau","Nur Gelb"],0,"Bildschirme mischen alle Farben aus rotem, grünem und blauem Licht.")
mc(14,"E","Ein Bildschirm zeigt Weiss aus Rot, Grün und Blau. Plötzlich sieht die Fläche Cyan (Hellblau) aus. Welche Farbe ist ausgefallen?",["Rot","Grün","Blau","Gelb"],0,"Ohne Rot bleiben Grün und Blau. Zusammen ergeben sie Cyan.")
tf(14,"G","Mischt man rotes, grünes und blaues Licht, entsteht Schwarz.",False,"Falsch. Es entsteht Weiss.")
# 15
order(15,"G","Ordne die Farben des Spektrums so, wie sie nach dem Prisma liegen. Beginne mit der Farbe, die am wenigsten abgelenkt wird.",["Rot","Orange","Gelb","Grün","Blau","Violett"],"Rot wird am wenigsten, Violett am stärksten gebrochen.")
mc(15,"G","Welchen Wellenlängenbereich hat sichtbares Licht?",["Etwa 380 bis 780 nm (Nanometer)","Etwa 1 bis 10 nm","Etwa 1 bis 10 m","Etwa 380 bis 780 mm"],0,"nm = Nanometer, ein Millionstel Millimeter.")
mc(15,"E","Welche Farbe hat Licht mit 700 nm Wellenlänge?",["Rot","Violett","Grün","Blau"],0,"Licht mit langer Wellenlänge ist rot, Licht mit kurzer Wellenlänge violett.")
tf(15,"E","Ein Prisma erzeugt die Farben selbst; im weissen Licht sind sie nicht enthalten.",False,"Falsch. Weisses Licht besteht aus allen Farben. Das Prisma bricht sie verschieden stark und trennt sie.")
goals={"1":"selbstleuchtende und beleuchtete Körper unterscheiden","2":"geradlinige Ausbreitung und Strahlenmodell","3":"Sehen durch Reflexion erklären","4":"Kern- und Halbschatten konstruieren","5":"Sonnen- und Mondfinsternis erklären","6":"Reflexionsgesetz anwenden","7":"Spiegelbild als virtuelles Bild, Mindestgrösse des Spiegels","8":"Hohl- und Wölbspiegel","9":"Brechung und Hebung","10":"Totalreflexion, Glasfaser, Fata Morgana","11":"Linsen, Brennpunkt, Brennweite","12":"Lupe und Kamera","13":"Auge und Kamera vergleichen","14":"additive Farbmischung","15":"Prisma, Spektrum, Wellenlänge"}
topic={"subject":"nt","status":"entwurf","quelle":"/workspace/schule/nt9-optik/quellen/Skript_Optik_Tino.pdf","topic":{"id":"nt9-optik","name":"Optik","goals":goals,"questions":Q}}
json.dump(topic,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'nt9-optik.json'),'w'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(Q),Counter(q['type'] for q in Q),Counter(q['level'] for q in Q))
