#!/usr/bin/env python3
"""ページのテキストをダンプして文字を確認するデバッグスクリプト"""
import re, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://www.ne.jp/asahi/beat/non/mori/myst/"
UA = "Mozilla/5.0 (personal archive script)"

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

for series, rel in [("G","indexjpeg/G1.html"),("W","indexjpeg/W1.html"),("WW","indexjpeg/WW1.html")]:
    url = urllib.parse.urljoin(BASE, rel)
    print(f"=== {series} ({url}) ===")
    text = fetch_text(url)
    sc = Scan()
    sc.feed(text)
    body = re.sub(r"\n{3,}", "\n\n", "".join(sc.out)).strip()
    out_file = Path(__file__).parent / f"debug_{series.lower()}.txt"
    out_file.write_text(body, encoding="utf-8")
    print(f"  保存: {out_file}  ({len(body)} 文字)")
    # タイトルっぽい行を先頭から表示
    lines = [l.strip() for l in body.split("\n") if l.strip()]
    print(f"  先頭20行:")
    for l in lines[:20]:
        print(f"    [{l[:80]}]")
    print()
