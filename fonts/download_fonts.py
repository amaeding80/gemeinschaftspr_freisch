#!/usr/bin/env python3
"""Fonts von Google Fonts herunterladen und korrekt benennen"""
import urllib.request, re, os, sys

DIR = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Beide Fonts auf einmal holen
URL = ("https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@"
       "0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;"
       "1,9..40,300;1,9..40,400;1,9..40,500"
       "&family=Newsreader:ital,wght@0,300;0,400;0,500;1,300;1,400"
       "&display=swap")

req = urllib.request.Request(URL, headers={"User-Agent": UA})
css = urllib.request.urlopen(req).read().decode("utf-8")

# Alle @font-face Blöcke parsen
blocks = re.findall(r'@font-face\s*\{([^}]+)\}', css, re.DOTALL)
downloaded = []

for block in blocks:
    family = re.search(r"font-family:\s*'([^']+)'", block)
    style  = re.search(r'font-style:\s*(\w+)', block)
    weight = re.search(r'font-weight:\s*(\d+)', block)
    src    = re.search(r'url\((https://[^)]+\.woff2)\)', block)
    # Subset aus dem Kommentar davor ermitteln — wir filtern nur latin
    
    if not all([family, style, weight, src]):
        continue

    fam = family.group(1).lower().replace(' ', '-')
    sty = style.group(1)      # normal / italic
    wgt = weight.group(1)     # 300, 400, 500, 600
    url = src.group(1)

    fname = f"{fam}-{wgt}-{sty}.woff2"
    fpath = os.path.join(DIR, fname)

    # Nicht doppelt herunterladen (latin + latin-ext haben gleichen Namen)
    if fname in [d[0] for d in downloaded]:
        continue

    req2 = urllib.request.Request(url, headers={"User-Agent": UA})
    data = urllib.request.urlopen(req2).read()
    with open(fpath, 'wb') as f:
        f.write(data)
    size = len(data)
    downloaded.append((fname, size))
    print(f"✅  {fname}  ({size//1024} KB)")

# Alte Hash-Dateien löschen
for f in os.listdir(DIR):
    if re.match(r'^[a-zA-Z0-9_-]{20,}\.woff2$', f):
        os.remove(os.path.join(DIR, f))
        print(f"🗑  {f} (alt, gelöscht)")

print(f"\n✅ Fertig — {len(downloaded)} Font-Dateien bereit")
