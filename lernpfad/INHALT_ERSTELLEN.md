# Lernpfad: Inhalte erstellen (Ablauf für ein neues Thema)

Auslöser: Tino sagt «Wir brauchen für den Test X einen Lernpfad». Daraus entsteht **eine Themendatei**
`inhalte/<fach>-<thema>.json`, die mit `merge_topic.py` in die App kommt. Kein Spreadsheet, keine Handarbeit in `questions.json`.

## 1. Eingaben (nur lesen)
| Quelle | Wozu |
|---|---|
| Skript (`.tex` bevorzugt, sonst PDF; Scans als Bild lesen) | Fachinhalt, Fachbegriffe, Zahlen, Bilder |
| Lernziele (aus dem Skript oder LZ-Blatt) | **eine Etappe = ein Lernziel**, Nummern übernehmen |
| Test (falls vorhanden) | nur zum **Ausschliessen**: keine Testaufgaben übernehmen oder nachbauen |
| Bildnachweise des Skripts | nur freie Bilder (gemeinfrei, CC) oder eigene exakte Grafiken (TikZ/SVG/matplotlib) |

## 2. Ausgabe: Themendatei (festes Format)
```json
{
 "subject": "rzg",                 // Fach-ID aus questions.json (nt, ma, rzg …)
 "status": "aktuell",              // aktuell | repetition | spaeter
 "quelle": "Pfad zum Skript",
 "topic": {
  "id": "rzg-universum", "name": "Vom Universum zur Erde",
  "goals": {"1": "Kurztext Lernziel 1", "2": "…"},
  "eOnly": [14, 18],               // optional: Lernziele, die nur Sek (E) sind
  "questions": [ … ]
 }
}
```
Frage-Felder (alle: `id`, `goal`, `level` G|E, `type`, `prompt`, `explanation`; optional `image`):

| type | zusätzliche Felder | Bewertung |
|---|---|---|
| `mc` | `options` (≥3), `answer` = Index | genau eine richtige Option |
| `tf` | `answer` true/false | |
| `num` | `answer` Zahl, `tolerance`, `unit` | akzeptiert 2’903.36, 2903,36, 2 903.36 |
| `order` | `items` in **richtiger** Reihenfolge (≥3) | App mischt; Antippen ordnet |
| `match` | `pairs` [[links, rechts], …] (≥3, eindeutig) | Auswahlliste pro Zeile |
| `cloze` | `text` mit `{0}`, `{1}` …; `gaps`: `{"options":[…],"answer":i}` oder `{"answer":"Text","alt":["…"]}` | Texteingabe ohne Gross/Klein, Leerzeichen; «.» = «:» bei Uhrzeiten |
| `image` | `{"src":"img/<fach>/datei.jpg","alt":"…","credit":"Urheber, Lizenz"}` | Pflicht: alt + credit |

## 3. Regeln
- **Etappen** = Lernziele. Pro Etappe **6 G-Fragen** (Real) + **2 E-Fragen** (Sek) ≈ 8. Real sieht nur G, Sek G+E.
- **Mix pro Thema**: ca. 35 % mc, 20 % num, 15 % tf, je 10 % cloze/match/order. Pro Etappe mind. 3 Typen.
- G = Wissen/Verstehen direkt aus dem Theorieteil. E = Anwenden/Rechnen/Vergleichen (Vertiefung).
- Deutsch de-CH, **ss statt ß**, typografischer Apostroph **’**, Zahlen **2’903.36** (Dezimalpunkt), Einheit separat.
- Keine Suggestivfragen; Distraktoren plausibel, aber eindeutig falsch laut Skript. «NICHT»-Fragen sparsam.
- Keine Aufgaben aus dem Test; Skript-Aufgaben nur mit neuen Zahlen/neuer Form.
- **Jede Lösung zweimal prüfen**: 1× beim Schreiben gegen das Skript, 1× mit der Lösungsliste (Schritt 4b). Rechnungen zweimal rechnen.
- Erklärung: 1–2 Sätze, nennt die richtige Antwort und den Grund.
- Keine Schülerdaten, keine Namen von Lernenden.
- Bilder: max. ~1 pro 2 Etappen, verkleinert (≤ 900 px, JPEG q≈78), nach `img/<fach>/`; nie Lehrmittel-Scans.
- Unklares oder Fehlendes: Frage weglassen statt erfinden.

## 4. Arbeitsschritte
1. Lernziele und Theorietext aus dem `.tex` extrahieren (Befehle entfernen, Aufgaben/Lösungen markieren).
2. Fragen in einem kleinen Python-Builder schreiben (Vorlage: `inhalte/_build_rzg-universum.py`) → erzeugt die Themendatei.
3. `python3 check.py inhalte/<datei>.json` – Schema, IDs, Lücken, Paare, Bilder, ß/'/Dezimalkomma.
4. a) `python3 merge_topic.py inhalte/<datei>.json` (sichert und prüft alles nochmals).
   b) Zweite Prüfung: Lösungsliste ausgeben (siehe Builder) und gegen das Skript lesen;
      Headless-Durchlauf: jede Frage richtig beantworten → keine Frage darf «falsch» melden.
5. `sw.js`: Cache-Namen erhöhen, neue Bilder in die Cache-Liste.
6. Screenshots, Muster an Tino; erst nach seinem Ok veröffentlichen.

## 5. Aufwand (Erfahrung RZG «Vom Universum zur Erde», 13 LZ, 104 Fragen)
- Lesen der Quelle: ~6 Kapitel `.tex` ≈ 60 KB Text. Als `.tex` deutlich billiger als PDF-Bilder.
- Schreiben: ein Durchgang im Builder, ~8 Fragen pro LZ. Prüfen: check.py + 1 Headless-Lauf (~90 s).
- Kostentreiber: Quellen als Bilder lesen (Scans), Neuschreiben statt Korrigieren, viele Screenshot-Runden.
