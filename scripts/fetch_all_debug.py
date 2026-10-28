#!/usr/bin/env python3
"""浮遊工作室の全シリーズページをテキスト化してdebug_all/に保存する。"""
import re, time, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://www.ne.jp/asahi/beat/non/mori/myst/"
UA   = "Mozilla/5.0 (personal archive script)"

SERIES = [
    ("sm",      "indexjpeg/S_M1.html",    "S&Mシリーズ"),
    ("v",       "indexjpeg/V1.html",       "Vシリーズ"),
    ("sh",      "indexjpeg/Sh1.html",      "四季"),
    ("g",       "indexjpeg/G1.html",       "Gシリーズ"),
    ("x",       "indexjpeg/X1.html",       "Xシリーズ"),
    ("xx",      "indexjpeg/XX1.html",      "XXシリーズ"),
    ("mr",      "indexjpeg/M_R1.html",     "M&R"),
    ("w",       "indexjpeg/W1.html",       "Wシリーズ"),
    ("ww",      "indexjpeg/WW1.html",      "WWシリーズ"),
    ("short",   "indexjpeg/short.html",    "短編"),
    ("sc",      "indexjpeg/SC1.html",      "スカイ・クロラ"),
    ("vs",      "indexjpeg/VS1.html",      "ヴォイド・シェイパ"),
    ("mizu",    "indexjpeg/mizu.html",     "水柿"),
    ("z",       "indexjpeg/Z1.html",       "Zシリーズ"),
    ("etc",     "indexjpeg/etc1.html",     "その他"),
    ("essay",   "indexjpeg/essay1.html",   "エッセイ"),
    ("shinsho", "indexjpeg/Shinsho.html",  "新書"),
]

class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script","style"): self.skip += 1
        if tag in ("br","p","div","tr","li","h1","h2","h3","table","hr"): self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script","style") and self.skip: self.skip -= 1
        if tag in ("p","div","tr","li","h1","h2","h3","table"): self.out.append("\n")
    def handle_data(self, data):
        if not self.skip: self.out.append(data)

def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw, hc = r.read(), r.headers.get_content_charset()
    cands = list(filter(None, [hc]))
    m = re.search(rb"charset=[\"']?([A-Za-z0-9_\-]+)", raw[:3000])
    if m: cands.append(m.group(1).decode())
    cands += ["utf-8","cp932","euc_jp"]
    for c in cands:
        try: return raw.decode(c)
        except (UnicodeDecodeError, LookupError): pass
    return raw.decode("utf-8", errors="replace")

out_dir = Path(__file__).parent / "debug_all"
out_dir.mkdir(exist_ok=True)

for key, rel, label in SERIES:
    out_path = out_dir / f"debug_{key}.txt"
    if out_path.exists():
        print(f"  skip (cached): {key} → {out_path.name}")
        continue
    url = urllib.parse.urljoin(BASE, rel)
    print(f"  fetch: {label} ({url}) ...", end=" ", flush=True)
    try:
        text = fetch_text(url)
        sc = Scan()
        sc.feed(text)
        body = re.sub(r"\n{3,}", "\n\n", "".join(sc.out)).strip()
        out_path.write_text(body, encoding="utf-8")
        print(f"ok ({len(body)} chars)")
    except Exception as e:
        print(f"ERROR: {e}")
    time.sleep(2)

print(f"\n完了: {out_dir}")
