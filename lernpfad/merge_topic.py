#!/usr/bin/env python3
"""Fügt eine Themendatei in questions.json und config.json ein (oder ersetzt ein Thema mit gleicher ID).
  python3 merge_topic.py inhalte/rzg-universum.json
Vorher wird die Datei mit check.py geprüft; danach wird alles nochmals geprüft. Sicherung: *.bak
"""
import json, os, subprocess, sys, shutil
D = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1]
if subprocess.run([sys.executable, os.path.join(D, "check.py"), src]).returncode: sys.exit("Abbruch: Themendatei fehlerhaft.")
f = json.load(open(src, encoding="utf-8"))
qp, cp = os.path.join(D, "questions.json"), os.path.join(D, "config.json")
for p in (qp, cp): shutil.copy(p, p + ".bak")
data = json.load(open(qp, encoding="utf-8")); cfg = json.load(open(cp, encoding="utf-8"))
subj = next((s for s in data["subjects"] if s["id"] == f["subject"]), None)
if not subj: sys.exit(f"Fach {f['subject']} gibt es nicht in questions.json.")
t = f["topic"]; old = [i for i, x in enumerate(subj["topics"]) if x["id"] == t["id"]]
if old: subj["topics"][old[0]] = t; print("Thema ersetzt:", t["id"])
else: subj["topics"].append(t); print("Thema neu:", t["id"])
cfg.setdefault("topics", {})[t["id"]] = f["status"]
json.dump(data, open(qp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(cfg, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if subprocess.run([sys.executable, os.path.join(D, "check.py")]).returncode:
    for p in (qp, cp): shutil.copy(p + ".bak", p)
    sys.exit("Fehler nach dem Einfügen: Sicherung wiederhergestellt.")
print("Fertig. Danach: Cache-Namen in sw.js erhöhen und Bilder in die Cache-Liste aufnehmen.")
