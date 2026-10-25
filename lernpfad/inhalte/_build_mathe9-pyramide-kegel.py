import json
from collections import Counter
Q=[];n=[0]
def add(goal,level,type,prompt,expl,**k):
    n[0]+=1;q={"id":f"PK{n[0]:03d}","goal":goal,"level":level,"type":type,"prompt":prompt};q.update(k);q["explanation"]=expl;Q.append(q)
import random
def mc(g,l,p,o,a,e,**k):
    r=random.Random(1000+n[0]);idx=list(range(len(o)));r.shuffle(idx)
    add(g,l,"mc",p,e,options=[o[i] for i in idx],answer=idx.index(a),**k)
def tf(g,l,p,a,e,**k):add(g,l,"tf",p,e,answer=a,**k)
def num(g,l,p,a,tol,unit,e,**k):add(g,l,"num",p,e,answer=a,tolerance=tol,unit=unit,**k)
def order(g,l,p,items,e,**k):add(g,l,"order",p,e,items=items,**k)
def match(g,l,p,pairs,e,**k):add(g,l,"match",p,e,pairs=pairs,**k)
def cloze(g,l,p,t,gaps,e,**k):add(g,l,"cloze",p,e,text=t,gaps=gaps,**k)
def sel(o,a):return {"options":o,"answer":a}
IMG=lambda f,alt:{"src":"img/ma/"+f,"alt":alt,"credit":"Eigene Grafik (SVG)"}
# Hinweis: In Auswahllisten (match rechts, cloze-Optionen) kein KaTeX, dort Unicode.
# LZ1
mc(1,"G","Wie viele Flächen, Kanten und Ecken hat eine quadratische Pyramide? (TH S. 4)",["5 Flächen, 8 Kanten, 5 Ecken","5 Flächen, 8 Kanten, 4 Ecken","4 Flächen, 8 Kanten, 5 Ecken","6 Flächen, 12 Kanten, 8 Ecken"],0,"1 Quadrat + 4 Dreiecke = 5 Flächen; 4 Grundkanten + 4 Seitenkanten = 8 Kanten; 4 Ecken unten + Spitze = 5 Ecken.")
match(1,"G","Welcher Körper passt zu welchem Gegenstand? (TH S. 2, 4, 8, 10)",[["Glacecornet","Kegel"],["Konservendose","Zylinder"],["Milchpackung","Prisma"],["Glasbau vor dem Louvre","Pyramide"],["Basketball","Kugel"]],"Cornet = Kegel, Dose = Zylinder, Packung = Prisma (Quader), Louvre = Pyramide, Ball = Kugel.")
mc(1,"E","Eine Pyramide hat ein Sechseck als Grundfläche. Aus wie vielen Dreiecken besteht ihre Mantelfläche? (TH S. 4)",["5","6","7","12"],1,"Jede Grundkante trägt ein Seitendreieck. Ein Sechseck hat 6 Kanten, also 6 Dreiecke.")
# LZ2
match(2,"G","Ordne den Nummern in der Skizze die Fachbegriffe zu. (TH S. 4)",[["1","Seitenkante k"],["2","Körperhöhe h"],["3","Seitenhöhe hₛ"],["4","Grundkante a"]],"1 führt von einer Ecke zur Spitze ($k$), 2 steht senkrecht auf der Mitte der Grundfläche ($h$), 3 führt von der Mitte einer Grundkante zur Spitze ($h_s$), 4 ist eine Seite des Quadrats ($a$).",image=IMG("pyramide-begriffe.svg","Quadratische Pyramide mit vier nummerierten Strecken"))
mc(2,"G","Welche Strecke in der Skizze ist die Mantellinie $s$ des Kegels? (TH S. 8)",["Strecke A","Strecke B","Strecke C","Keine, die Mantellinie ist gebogen"],0,"A führt vom Rand des Grundkreises schräg zur Spitze: das ist $s$. B ist die Körperhöhe $h$, C der Radius $r$.",image=IMG("kegel-linien.svg","Kegel mit drei markierten Strecken A, B und C"))
mc(2,"G","Was ist die Seitenhöhe $h_s$ einer Pyramide? (TH S. 4)",["Die Höhe eines Seitendreiecks, von der Mitte der Grundkante zur Spitze","Der senkrechte Abstand von der Spitze zur Grundfläche","Die Kante von einer Ecke der Grundfläche zur Spitze","Die Diagonale der Grundfläche"],0,"$h_s$ liegt im Seitendreieck. Der senkrechte Abstand ist die Körperhöhe $h$, die Kante von der Ecke zur Spitze die Seitenkante $k$.")
mc(2,"E","Für einen Kegel ist der Durchmesser $d$ gegeben. Jemand rechnet $G=\\pi\\cdot d^2$. Was stimmt? (TH S. 9)",["Die Rechnung stimmt.","$G$ wird doppelt so gross wie richtig.","$G$ wird 4-mal so gross wie richtig.","$G$ wird halb so gross wie richtig."],2,"Richtig ist $G=\\pi\\cdot r^2$ mit $r=d:2$. Weil $d=2\\cdot r$, ist $d^2=4\\cdot r^2$: das Resultat ist 4-mal zu gross.")
mc(2,"E","Ein Turm bekommt ein Pyramidendach. Welche Fläche muss der Dachdecker eindecken? (TH S. 5)",["Die Oberfläche $O$","Die Mantelfläche $M$","Die Grundfläche $G$","$O+G$"],1,"Ein Dach hat keinen Boden: Dachfläche = Mantelfläche $M$, also nur die Seitendreiecke.")
# LZ3
mc(3,"G","Warum gilt für Prisma und Zylinder $V=G\\cdot h$? (TH S. 2)",["Man stapelt dünne Platten der Grundfläche so hoch, wie der Körper ist.","Man multipliziert alle Kanten miteinander.","Weil die Mantelfläche ein Rechteck ist.","Weil Grund- und Deckfläche zusammen $2\\cdot G$ ergeben."],0,"Stellt man sich $G$ als 1 cm dicke Platte vor, braucht es $h$ solche Platten: Grundfläche mal Höhe.")
tf(3,"E","Rollt man den Mantel eines Zylinders ab, entsteht ein Rechteck mit der Länge $2\\cdot\\pi\\cdot r$ und der Breite $h$. (TH S. 2)",True,"Richtig. Die Länge ist der Umfang $u=2\\cdot\\pi\\cdot r$, darum $M=u\\cdot h=2\\cdot\\pi\\cdot r\\cdot h$.")
# LZ4
match(4,"G","Ordne die gleich grossen Volumen zu. (TH S. 2, 12)",[["1 L","1 dm³"],["1 m³","1’000 L"],["1 mL","1 cm³"],["0.5 L","500 cm³"]],"Faktor 1’000: 1 m³ = 1’000 dm³ = 1’000 L, 1 dm³ = 1’000 cm³ = 1 L, 1 cm³ = 1 mL.")
num(4,"G","Kopfrechnen: Ein Aquarium fasst 0.3 m³. Wie viele Liter sind das? (TH S. 12)",300,0,"L","1 m³ = 1’000 L, also 0.3 · 1’000 = 300 L.")
cloze(4,"G","Rechne um. (TH S. 12)","4’500 cm³ sind {0} dm³, also {1} Liter.",[sel(["0.45","4.5","45","450"],1),sel(["0.45","4.5","45","450"],1)],"4’500 : 1’000 = 4.5 dm³, und 1 dm³ = 1 L, also 4.5 L.")
mc(4,"E","Schätzen: Ein Glacecornet (Kegel) ist innen etwa 12 cm tief, die Öffnung hat etwa 5 cm Durchmesser. Wie viel passt ungefähr hinein? (TH S. 9, 12)",["etwa 8 mL","etwa 80 mL","etwa 0.8 L","etwa 8 L"],1,"$V=\\frac{1}{3}\\cdot\\pi\\cdot 2.5^2\\cdot 12\\approx 78.5$ cm³, also rund 80 mL.")
# LZ5
cloze(5,"G","Ergänze das versteckte rechtwinklige Dreieck im Kegel. (TH S. 8)","Die Strecken $h$, $r$ und $s$ bilden ein rechtwinkliges Dreieck. Der rechte Winkel liegt beim {0}. Die Hypotenuse ist {1}.",[sel(["Mittelpunkt des Grundkreises","Rand des Grundkreises","Spitze"],0),sel(["die Körperhöhe h","der Radius r","die Mantellinie s"],2)],"$h$ steht senkrecht auf dem Mittelpunkt der Grundfläche. Gegenüber dem rechten Winkel liegt $s$: $s^2=r^2+h^2$.")
mc(5,"E","Welche Reihenfolge gilt in jeder quadratischen Pyramide? (TH S. 5)",["$h<h_s<k$","$h_s<h<k$","$k<h_s<h$","$h=h_s<k$"],0,"In Dreieck 1 ist $h_s$ Hypotenuse, also $h<h_s$. In Dreieck 2 ist $k$ Hypotenuse, also $h_s<k$.")
mc(5,"G","Welches rechtwinklige Dreieck im Innern der Pyramide enthält die Körperhöhe $h$? (TH S. 5)",["$h$, $\\frac{a}{2}$ und $h_s$, Hypotenuse $h_s$","$h$, $\\frac{a}{2}$ und $h_s$, Hypotenuse $h$","$h$, $a$ und $h_s$, Hypotenuse $a$","$h$, $h_s$ und $k$, Hypotenuse $k$"],0,"Dreieck 1: Körperhöhe $h$, halbe Grundkante $\\frac{a}{2}$ und Seitenhöhe $h_s$ als Hypotenuse.")
num(5,"E","Kopfrechnen: Ein Kegel hat den Radius 6 cm und die Mantellinie 10 cm. Wie hoch ist er? (TH S. 9)",8,0,"cm","$h=\\sqrt{s^2-r^2}=\\sqrt{100-36}=\\sqrt{64}=8$ cm.")
# LZ6
mc(6,"G","Du schneidest die Mantelfläche eines Kegels entlang einer Mantellinie auf und legst sie flach. Was entsteht? (TH S. 8)",["Ein Dreieck, dessen Höhe die Körperhöhe $h$ ist","Ein Kreissektor, dessen Radius die Mantellinie $s$ ist","Ein Kreissektor, dessen Radius der Kegelradius $r$ ist","Ein Rechteck mit der Länge $2\\cdot\\pi\\cdot r$"],1,"Es entsteht ein Kreissektor («Kuchenstück»). Sein Radius ist $s$, sein Bogen ist so lang wie der Umfang des Grundkreises.")
mc(6,"G","Woraus besteht das Netz einer quadratischen Pyramide? (TH S. 4)",["1 Quadrat und 4 gleiche Dreiecke","2 Quadrate und 4 Rechtecke","1 Quadrat und 4 Rechtecke","4 gleiche Dreiecke"],0,"Die Grundfläche ist ein Quadrat, die Mantelfläche besteht aus 4 gleichen Seitendreiecken.")
cloze(6,"G","Ergänze zum Kegelnetz. (TH S. 8)","Der Bogen des Kreissektors ist so lang wie der {0} des Grundkreises.",[sel(["Radius","Durchmesser","Umfang"],2)],"Beim Aufrollen legt sich der Bogen genau um den Grundkreis: $b=2\\cdot\\pi\\cdot r$.")
mc(6,"E","Mit welchem Term berechnet man die Fläche eines Seitendreiecks der quadratischen Pyramide? (TH S. 4–5)",["$\\frac{a\\cdot h_s}{2}$","$\\frac{a\\cdot h}{2}$","$a\\cdot h_s$","$\\frac{a\\cdot k}{2}$"],0,"Grundseite $a$, Höhe des Dreiecks $h_s$. Die Körperhöhe $h$ liegt nicht im Seitendreieck.")
# LZ7
mc(7,"G","Warum steht in der Volumenformel der Pyramide der Faktor $\\frac{1}{3}$? (TH S. 6)",["Weil eine Pyramide drei Seitenflächen hat","Weil man eine hohle Pyramide 3-mal füllen muss, bis das Prisma mit gleicher Grundfläche und gleicher Höhe voll ist","Weil die Spitze ein Drittel der Höhe ausmacht","Weil man die Grundfläche durch 3 teilen muss, da sie ein Dreieck ist"],1,"Umschüttversuch: Das Prisma mit gleichem $G$ und $h$ fasst genau 3 Pyramidenfüllungen. Darum $V=\\frac{1}{3}\\cdot G\\cdot h$.")
tf(7,"G","Der Faktor $\\frac{1}{3}$ gilt nur für Pyramiden mit quadratischer Grundfläche. (TH S. 6)",False,"Falsch. $V=\\frac{1}{3}\\cdot G\\cdot h$ gilt für jede Pyramide, ob die Grundfläche ein Quadrat, Rechteck oder Dreieck ist.")
mc(7,"G","Würfel-Trick: Man verbindet die Mitte eines Würfels mit allen Ecken. In wie viele gleiche Pyramiden zerfällt der Würfel? (TH S. 6)",["4","6","8","12"],1,"Eine Pyramide pro Würfelfläche, also 6.")
mc(7,"E","Beim Würfel-Trick hat jede Pyramide $G=a^2$ und $h=\\frac{a}{2}$. Warum folgt daraus der Faktor $\\frac{1}{3}$? (TH S. 6)",["Weil ein Sechstel des Würfels gleich $\\frac{1}{3}\\cdot a^2\\cdot\\frac{a}{2}$ ist","Weil die Pyramidenhöhe ein Drittel der Würfelkante ist","Weil der Würfel 3 Paare gegenüberliegender Flächen hat","Weil jede Pyramide 3 Seitenflächen hat"],0,"$V=\\frac{a^3}{6}=\\frac{1}{3}\\cdot a^2\\cdot\\frac{a}{2}=\\frac{1}{3}\\cdot G\\cdot h$.")
# LZ8
mc(8,"G","Für das Volumen dieser Pyramide wird gerechnet: $V=\\frac{1}{3}\\cdot a^2\\cdot h_s$. Was ist falsch? (TH S. 7)",["Nichts, die Rechnung stimmt.","Man hätte die Körperhöhe $h$ statt der Seitenhöhe $h_s$ einsetzen müssen.","Man hätte $\\frac{1}{2}$ statt $\\frac{1}{3}$ nehmen müssen.","Man hätte $a$ statt $a^2$ einsetzen müssen."],1,"Im Volumen steht immer die senkrechte Körperhöhe $h$, nie $h_s$. Ist nur $h_s$ bekannt, rechnet man $h$ zuerst mit Pythagoras aus. Weil $h<h_s$, wäre das Resultat zu gross.",image=IMG("pyramide-fehler.svg","Quadratische Pyramide mit Körperhöhe h, Seitenhöhe hs und Grundkante a"))
mc(8,"G","Welche Formel gibt das Volumen eines Kegels? (TH S. 9)",["$V=\\frac{1}{3}\\cdot\\pi\\cdot r^2\\cdot h$","$V=\\pi\\cdot r\\cdot s$","$V=\\frac{1}{3}\\cdot\\pi\\cdot r^2\\cdot s$","$V=\\pi\\cdot r^2\\cdot h$"],0,"Ein Drittel vom Zylinder mit gleichem $r$ und $h$. $\\pi\\cdot r\\cdot s$ ist die Mantelfläche.")
mc(8,"E","Ein Kegel und ein Zylinder haben den gleichen Radius. Wann haben sie das gleiche Volumen? (TH S. 9)",["Wenn der Kegel gleich hoch ist","Wenn der Kegel doppelt so hoch ist","Wenn der Kegel 3-mal so hoch ist","Wenn der Kegel einen Drittel so hoch ist"],2,"$\\frac{1}{3}\\cdot\\pi\\cdot r^2\\cdot(3h)=\\pi\\cdot r^2\\cdot h$.")
# LZ9
mc(9,"G","Eine Pyramide hat den Würfelboden als Grundfläche, ihre Spitze liegt auf der Deckfläche. Welcher Anteil des Würfelvolumens ist das? (TH S. 6)",["$\\frac{1}{6}$","$\\frac{1}{4}$","$\\frac{1}{3}$","$\\frac{1}{2}$"],2,"Gleiche Grundfläche und gleiche Höhe wie der Würfel (ein Prisma): $\\frac{1}{3}$.")
mc(9,"E","Beim Würfel-Trick ist jede Pyramide ein Sechstel des Würfels. Wie viel Prozent sind das? (TH S. 6)",["16.67 %","25 %","33.33 %","50 %"],0,"$\\frac{1}{6}=1:6\\approx 0.1667=16.67$ %.")
num(9,"G","Kopfrechnen: Ein Würfel hat die Kante 6 cm. Eine Pyramide hat den Würfelboden als Grundfläche und die Spitze auf der Deckfläche. Wie gross ist ihr Volumen? (TH S. 6–7)",72,0,"cm³","$V=\\frac{1}{3}\\cdot 6^2\\cdot 6=\\frac{216}{3}=72$ cm³.")
# LZ10
mc(10,"G","Mit welcher Formel berechnet man den Zentriwinkel $\\alpha$ im Kegelnetz? (TH S. 8–9)",["$\\alpha=\\frac{r}{s}\\cdot 360^\\circ$","$\\alpha=\\frac{s}{r}\\cdot 360^\\circ$","$\\alpha=\\frac{h}{s}\\cdot 360^\\circ$","$\\alpha=\\frac{r}{h}\\cdot 360^\\circ$"],0,"Der Bogen $2\\cdot\\pi\\cdot r$ ist der Anteil $\\frac{r}{s}$ vom ganzen Kreis $2\\cdot\\pi\\cdot s$.")
mc(10,"E","Ein Kegel wird aus einem Halbkreis gerollt ($\\alpha=180^\\circ$). Was gilt? (TH S. 8–9)",["$r=s$","$r=\\frac{s}{2}$","$r=2\\cdot s$","$r=\\frac{s}{4}$"],1,"$\\frac{r}{s}\\cdot 360^\\circ=180^\\circ$ ergibt $\\frac{r}{s}=\\frac{1}{2}$, also $r=\\frac{s}{2}$.")
# LZ11
mc(11,"G","Wie viele Grosskreise sind zusammen so gross wie die Oberfläche einer Kugel? (TH S. 10)",["2","3","4","6"],2,"Archimedes: $O=4\\cdot\\pi\\cdot r^2$, das sind 4 Grosskreise.")
tf(11,"G","Eine Kugel hat wie der Kegel ein Netz. (TH S. 10)",False,"Falsch. Die Kugeloberfläche lässt sich nicht flach ausbreiten (Orangenschale).")
mc(11,"E","Kegel, Halbkugel und Zylinder haben den gleichen Radius $r$ und die Höhe $h=r$. Wie verhalten sich ihre Volumen? (TH S. 10)",["1 : 2 : 3","1 : 3 : 4","1 : 1 : 3","2 : 3 : 4"],0,"$\\frac{1}{3}\\pi r^3:\\frac{2}{3}\\pi r^3:\\pi r^3=1:2:3$.")
# LZ12
mc(12,"G","Wie stellt man $V=\\frac{1}{3}\\cdot G\\cdot h$ nach $h$ um? (TH S. 7)",["$h=\\frac{3\\cdot V}{G}$","$h=\\frac{V}{3\\cdot G}$","$h=3\\cdot V\\cdot G$","$h=\\frac{G}{3\\cdot V}$"],0,"Beide Seiten mal 3, dann durch $G$: $h=\\frac{3\\cdot V}{G}$.")
mc(12,"G","Von einem Kegel kennt man $s$ und $r$. Wie berechnet man $h$? (TH S. 9)",["$h=\\sqrt{s^2-r^2}$","$h=\\sqrt{s^2+r^2}$","$h=s-r$","$h=\\sqrt{r^2-s^2}$"],0,"$s$ ist die Hypotenuse: $h^2=s^2-r^2$.")
mc(12,"E","Wie berechnet man den Radius einer Kugel aus ihrer Oberfläche $O$? (TH S. 11)",["$r=\\sqrt{\\frac{O}{4\\cdot\\pi}}$","$r=\\frac{O}{4\\cdot\\pi}$","$r=\\sqrt[3]{\\frac{O}{4\\cdot\\pi}}$","$r=\\sqrt{4\\cdot\\pi\\cdot O}$"],0,"$O=4\\cdot\\pi\\cdot r^2$ ⇒ $r^2=\\frac{O}{4\\cdot\\pi}$ ⇒ Quadratwurzel.")
# LZ13
mc(13,"G","Ein Haus (Quader) hat ein Pyramidendach. Welche Fläche gehört NICHT zur Oberfläche des ganzen Körpers? (TH S. 12)",["Die Mantelfläche des Daches","Der Boden","Die Fläche, an der Dach und Quader zusammenstossen","Die Wände"],2,"Die Klebefläche zwischen zwei Teilkörpern sieht man von aussen nicht. Sie zählt nicht zur Oberfläche.")
order(13,"E","Ordne die 4 Schritte für zusammengesetzte Körper. (TH S. 12)",["Zerlegen und Skizze beschriften","Masse den Teilkörpern zuordnen, fehlende Strecken mit Pythagoras","Teilkörper berechnen und addieren oder subtrahieren","Umrechnen und Antwortsatz schreiben"],"Zerlegen – Masse zuordnen – Teilkörper berechnen – Umrechnen und Antwortsatz.")
# LZ14
mc(14,"G","Für das Volumen eines Verkehrs-Leitkegels kommt 3.2 m³ heraus. Was sagst du dazu? (TH S. 12)",["Plausibel, Leitkegel sind schwer.","Viel zu gross: Ein Leitkegel fasst nur wenige Liter.","Zu klein: Es müssten etwa 30 m³ sein.","Man kann das nicht abschätzen."],1,"3.2 m³ = 3’200 L, so viel wie ein grosser Wassertank. Ein Leitkegel fasst nur wenige Liter.")
num(14,"G","Kopfrechnen: 1 m³ Kies wiegt 1.8 t. Wie viele Tonnen wiegen 5 m³ Kies? (TH S. 12)",9,0,"t","$m=\\rho\\cdot V=1.8\\cdot 5=9$ t.")
mc(14,"E","Schätzen: Ein Silo fasst rund 80 m³ Weizen (0.78 t/m³). Wie schwer ist die volle Ladung ungefähr? (TH S. 12–13)",["etwa 6 t","etwa 60 t","etwa 100 t","etwa 600 t"],1,"$0.78\\cdot 80\\approx 62$ t, also rund 60 t. Etwas weniger als 80 t, weil Weizen leichter ist als Wasser.")
# LZ15
mc(15,"E","Bei einem Kegel wird der Radius $r$ verdoppelt, die Höhe $h$ bleibt gleich. Was passiert mit dem Volumen? (AH3, AH5)",["Es verdoppelt sich.","Es wird 4-mal so gross.","Es wird 8-mal so gross.","Es bleibt gleich, weil $h$ gleich bleibt."],1,"In $V=\\frac{1}{3}\\cdot\\pi\\cdot r^2\\cdot h$ steht $r$ im Quadrat: $(2r)^2=4r^2$.")
mc(15,"G","Bei einer Pyramide wird die Höhe halbiert, die Grundfläche bleibt gleich. Was passiert mit dem Volumen? (AH3)",["Es bleibt gleich.","Es wird halb so gross.","Es wird ein Viertel so gross.","Es wird ein Drittel so gross."],1,"$V=\\frac{1}{3}\\cdot G\\cdot h$: $h$ steht einfach (nicht im Quadrat), also halbes $h$ = halbes $V$.")
mc(15,"E","Bei einem Kegel werden Radius und Höhe verdoppelt. Wie verändert sich das Volumen? (AH3, AH5)",["2-mal so gross","4-mal so gross","6-mal so gross","8-mal so gross"],3,"$r^2$ wird 4-mal, $h$ 2-mal so gross: $4\\cdot 2=8$.")
goals={"1":"Körper erkennen, benennen und Eigenschaften beschreiben","2":"Grössen an einer Skizze zeigen und Fachbegriffe verwenden","3":"Prisma und Zylinder: Volumen und Oberfläche (Repetition)","4":"Volumeneinheiten umrechnen (cm³, dm³, m³, Liter)","5":"Pythagoras in Pyramide und Kegel (h, hs, k, s)","6":"Netz von Pyramide und Kegel, Mantel- und Oberfläche","7":"Begründen, warum Pyramide/Kegel ein Drittel von Prisma/Zylinder sind","8":"Volumen von Pyramide und Kegel","9":"Pyramiden im Würfel als Bruchteil und Prozent","10":"Kegel aus dem Kreissektor","11":"Kugel: Volumen und Oberfläche","12":"Formeln umstellen","13":"Zusammengesetzte Körper","14":"Sachaufgaben, Schätzen und Plausibilität","15":"Volumenänderung bei veränderten Längen begründen"}
t={"subject":"ma","status":"aktuell","quelle":"Spartan-117: 02 Unterrichtsmaterial\\Mathematik\\09 Klasse 9\\LU14 Pyramide und Kegel\\ (Theorieheft, Lernziele)","topic":{"id":"mathe9-pyramide-kegel","name":"Pyramide und Kegel","goals":goals,"questions":Q}}
json.dump(t,open(__import__('os').path.join(__import__('os').path.dirname(__file__),'mathe9-pyramide-kegel.json'),'w'),ensure_ascii=False,indent=1)
print(len(Q),Counter(q['type'] for q in Q),Counter(q['level'] for q in Q))
print(sorted(Counter(q['goal'] for q in Q).items()))
# Lösungsliste
for q in Q:
    a=q.get('answer');s={'mc':lambda:q['options'][a],'tf':lambda:a,'num':lambda:f"{a} {q['unit']}",'cloze':lambda:[g['options'][g['answer']] for g in q['gaps']],'match':lambda:q['pairs'],'order':lambda:q['items']}[q['type']]()
    print(q['id'],q['goal'],q['level'],'|',q['prompt'][:70],'=>',str(s)[:90])
