#!/usr/bin/env python3
import urllib.request, re, os

DIR = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

URL = "https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,300;0,400;0,500;1,300;1,400&display=swap"
req = urllib.request.Request(URL, headers={"User-Agent": UA})
css = urllib.request.urlopen(req).read().decode("utf-8")

blocks = re.findall(r'@font-face\s*\{([^}]+)\}', css, re.DOTALL)
downloaded = []

for block in blocks:
    style  = re.search(r'font-style:\s*(\w+)', block)
    weight = re.search(r'font-weight:\s*(\d+)', block)
    src    = re.search(r'url\((https://[^)]+\.woff2)\)', block)
    if not all([style, weight, src]):
        continue
    sty = style.group(1)
    wgt = weight.group(1)
    url = src.group(1)
    fname = f"newsreader-{wgt}-{sty}.woff2"
    if fname in downloaded:
        continue
    req2 = urllib.request.Request(url, headers={"User-Agent": UA})
    data = urllib.request.urlopen(req2).read()
    with open(os.path.join(DIR, fname), 'wb') as f:
        f.write(data)
    downloaded.append(fname)
    print(f"✅  {fname}  ({len(data)//1024} KB)")

print(f"\n✅ Fertig — {len(downloaded)} Newsreader-Dateien")
