#!/usr/bin/env python3
"""Prüft questions.json gegen schema.json und fachliche Regeln. Aufruf: python3 check.py"""
import json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
err = []
data = json.load(open(os.path.join(D, "questions.json"), encoding="utf-8"))
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

val(data, schema, "$")
ids = set(); stat = {}
for s in data.get("subjects", []):
    if not os.path.exists(os.path.join(D, s["icon"])): err.append(f"{s['id']}: Icon fehlt")
    for t in s["topics"]:
        for q in t["questions"]:
            p = q.get("id", "?")
            if p in ids: err.append(f"{p}: ID doppelt")
            ids.add(p)
            if str(q["goal"]) not in t["goals"]: err.append(f"{p}: Lernziel {q['goal']} nicht im Thema")
            if q["level"] == "E" and q["goal"] not in (14, 18) or q["level"] == "G" and q["goal"] in (14, 18):
                err.append(f"{p}: Niveau passt nicht zum Lernziel {q['goal']}")
            ty, a = q["type"], q["answer"]
            if ty == "mc":
                o = q.get("options", [])
                if len(o) < 3: err.append(f"{p}: MC braucht ≥3 Optionen")
                if len(set(o)) != len(o): err.append(f"{p}: Optionen doppelt")
                if not (isinstance(a, int) and not isinstance(a, bool) and 0 <= a < len(o)): err.append(f"{p}: MC-Antwort ungültig")
            elif ty == "tf":
                if not isinstance(a, bool): err.append(f"{p}: R/F-Antwort muss true/false sein")
                if "options" in q: err.append(f"{p}: R/F ohne Optionen")
            elif ty == "num":
                if not isinstance(a, (int, float)) or isinstance(a, bool): err.append(f"{p}: Zahl erwartet")
                if "tolerance" not in q or "unit" not in q: err.append(f"{p}: Toleranz/Einheit fehlt")
            if "image" in q and not os.path.exists(os.path.join(D, q["image"])): err.append(f"{p}: Bild fehlt")
            txt = json.dumps(q, ensure_ascii=False)
            if "ß" in txt: err.append(f"{p}: ß verwendet")
            if "'" in txt: err.append(f"{p}: gerades Apostroph")
            stat.setdefault(q["level"], 0); stat[q["level"]] += 1
print(f"Fragen: {len(ids)}  G: {stat.get('G',0)}  E: {stat.get('E',0)}")
# Antwort-Verteilung MC
if err:
    print("FEHLER:"); [print(" -", e) for e in err]; sys.exit(1)
print("OK: Schema, IDs, Lernziele, Niveaus und Antwortschlüssel geprüft.")
