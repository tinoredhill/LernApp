#!/usr/bin/env python3
"""Prüft die Lerninhalte.
  python3 check.py                     prüft questions.json (+ config.json)
  python3 check.py inhalte/thema.json  prüft eine einzelne Themendatei vor dem Einfügen
Prüft Schema, eindeutige IDs, Lernziele/Niveaus, Antwortschlüssel aller Fragetypen,
Bilder (Datei, Alt-Text, Bildnachweis), Rechtschreibregeln (ss statt ß, ’ statt ').
"""
import json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
err, warn = [], []
schema = json.load(open(os.path.join(D, "schema.json"), encoding="utf-8"))
T = {"object": dict, "array": list, "string": str, "integer": int, "number": (int, float), "boolean": bool}

def val(x, s, p):
    t = s.get("type")
    if t and (not isinstance(x, T[t]) or (t in ("integer", "number") and isinstance(x, bool))):
        err.append(f"{p}: Typ {t} erwartet"); return
    if "enum" in s and x not in s["enum"]: err.append(f"{p}: {x!r} nicht in {s['enum']}")
    if "pattern" in s and not re.search(s["pattern"], x): err.append(f"{p}: Muster verletzt")
    if "minimum" in s and x < s["minimum"]: err.append(f"{p}: < {s['minimum']}")
    if isinstance(x, dict):
        for k in s.get("required", []):
            if k not in x: err.append(f"{p}: Feld «{k}» fehlt")
        pr = s.get("properties", {})
        for k, v in x.items():
            if k in pr: val(v, pr[k], f"{p}.{k}")
            elif s.get("additionalProperties") is False: err.append(f"{p}: unbekanntes Feld «{k}»")
            elif isinstance(s.get("additionalProperties"), dict): val(v, s["additionalProperties"], f"{p}.{k}")
    if isinstance(x, list):
        if len(x) < s.get("minItems", 0): err.append(f"{p}: zu wenige Einträge")
        for i, v in enumerate(x): val(v, s.get("items", {}), f"{p}[{i}]")

TOPIC_SCHEMA = schema["properties"]["subjects"]["items"]["properties"]["topics"]["items"]
isint = lambda a: isinstance(a, int) and not isinstance(a, bool)

def check_q(q, t, ids):
    p = q.get("id", "?")
    if p in ids: err.append(f"{p}: ID doppelt")
    ids.add(p)
    if str(q["goal"]) not in t["goals"]: err.append(f"{p}: Lernziel {q['goal']} nicht im Thema")
    eo = t.get("eOnly", [])
    if eo and ((q["level"] == "E") != (q["goal"] in eo)): err.append(f"{p}: Niveau passt nicht zu eOnly {eo}")
    ty, a = q["type"], q.get("answer")
    if ty == "mc":
        o = q.get("options", [])
        if len(o) < 3: err.append(f"{p}: MC braucht ≥3 Optionen")
        if len(set(o)) != len(o): err.append(f"{p}: Optionen doppelt")
        if not (isint(a) and 0 <= a < len(o)): err.append(f"{p}: MC-Antwort ungültig")
    elif ty == "tf":
        if not isinstance(a, bool): err.append(f"{p}: R/F-Antwort muss true/false sein")
    elif ty == "num":
        if not isinstance(a, (int, float)) or isinstance(a, bool): err.append(f"{p}: Zahl erwartet")
        if "tolerance" not in q or "unit" not in q: err.append(f"{p}: Toleranz/Einheit fehlt")
    elif ty == "order":
        it = q.get("items", [])
        if len(it) < 3 or len(set(it)) != len(it): err.append(f"{p}: Reihenfolge braucht ≥3 verschiedene Einträge")
    elif ty == "match":
        pr = q.get("pairs", [])
        if len(pr) < 3 or any(len(x) != 2 for x in pr): err.append(f"{p}: Zuordnen braucht ≥3 Paare [links, rechts]")
        elif len({x[0] for x in pr}) != len(pr) or len({x[1] for x in pr}) != len(pr): err.append(f"{p}: Paare nicht eindeutig")
    elif ty == "cloze":
        g = q.get("gaps", []); txt = q.get("text", "")
        marks = sorted(int(m) for m in re.findall(r"\{(\d+)\}", txt))
        if marks != list(range(len(g))): err.append(f"{p}: Lücken {{0}}…{{n}} passen nicht zu gaps")
        for i, x in enumerate(g):
            if "options" in x:
                if not (isint(x.get("answer")) and 0 <= x["answer"] < len(x["options"])): err.append(f"{p}: Lücke {i} Antwort ungültig")
            elif not (isinstance(x.get("answer"), str) and x["answer"].strip()): err.append(f"{p}: Lücke {i} braucht Text-Antwort")
    if ty not in ("mc", "tf", "num") and "answer" in q: warn.append(f"{p}: «answer» wird bei {ty} nicht verwendet")
    im = q.get("image")
    if im is not None:
        src = im if isinstance(im, str) else im.get("src", "")
        if not os.path.exists(os.path.join(D, src)): err.append(f"{p}: Bild fehlt ({src})")
        if isinstance(im, dict) and (not im.get("alt") or not im.get("credit")): err.append(f"{p}: Bild braucht alt und credit")
        if isinstance(im, str) and not src.endswith(".svg"): warn.append(f"{p}: Bild ohne alt/credit")
    txt = json.dumps(q, ensure_ascii=False)
    if "ß" in txt: err.append(f"{p}: ß verwendet")
    if "'" in txt: err.append(f"{p}: gerades Apostroph")
    if re.search(r"\d,\d", txt): warn.append(f"{p}: Dezimalkomma? (Format 2’903.36)")
    if re.search(r"\d{5,}", re.sub(r'"answer": *\d+', "", txt)): warn.append(f"{p}: grosse Zahl ohne ’-Trennung im Text")

def check_topic(t, ids, label):
    val(t, TOPIC_SCHEMA, label)
    if err: return
    for q in t["questions"]: check_q(q, t, ids)
    lv = {}
    for q in t["questions"]: lv.setdefault(q["level"], 0); lv[q["level"]] += 1
    print(f"  {t['id']}: {len(t['questions'])} Fragen (G {lv.get('G',0)}, E {lv.get('E',0)}), {len(t['goals'])} Lernziele")
    for g in t["goals"]:
        n = [q for q in t["questions"] if str(q["goal"]) == g]
        if t["questions"] and not n: warn.append(f"{t['id']}: Lernziel {g} ohne Fragen")

args = sys.argv[1:]
if args:  # einzelne Themendatei
    f = json.load(open(args[0], encoding="utf-8"))
    for k in ("subject", "status", "topic"):
        if k not in f: err.append(f"Themendatei: Feld «{k}» fehlt")
    if f.get("status") not in ("aktuell", "repetition", "spaeter"): err.append("status ungültig")
    if not err: check_topic(f["topic"], set(), "topic")
else:
    data = json.load(open(os.path.join(D, "questions.json"), encoding="utf-8"))
    val(data, schema, "$")
    ids = set()
    for s in data.get("subjects", []):
        if not os.path.exists(os.path.join(D, s["icon"])): err.append(f"{s['id']}: Icon fehlt")
        for t in s["topics"]: check_topic(t, ids, t["id"])
    cp = os.path.join(D, "config.json")
    if os.path.exists(cp):
        cfg = json.load(open(cp, encoding="utf-8")).get("topics", {})
        tids = {t["id"] for s in data["subjects"] for t in s["topics"]}
        for k, v in cfg.items():
            if v not in ("aktuell", "repetition", "spaeter") or k not in tids: err.append(f"config: {k}={v}")
        print(f"  config.json: {len(cfg)} Status-Einträge")
for w in warn: print("Hinweis:", w)
if err:
    print("FEHLER:"); [print(" -", e) for e in err]; sys.exit(1)
print("OK: Schema, IDs, Lernziele, Niveaus, Antwortschlüssel und Bilder geprüft.")
