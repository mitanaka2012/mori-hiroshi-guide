#!/usr/bin/env python3
"""
浮遊工作室（ミステリィ制作部）から G/W/WW シリーズの作者コメントを取得し、
mori_volumes.html の COMMENTS データを更新するスクリプト。

使い方（Python 3.8以上、標準ライブラリのみ）:
    python update_mori_comments.py
"""

import json, re, sys, time, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://www.ne.jp/asahi/beat/non/mori/myst/"
UA = "Mozilla/5.0 (personal archive script)"

SERIES_PAGES = {
    "g":  "indexjpeg/G1.html",
    "w":  "indexjpeg/W1.html",
    "ww": "indexjpeg/WW1.html",
}

SERIES_TITLES = {
    "g": [
        "φは壊れたね", "θは遊んでくれたよ", "τになるまで待って",
        "εに誓って", "λに歯がない", "ηなのに夢のよう",
        "目薬αで殺菌します", "ジグβは神ですか", "キウイγは時計仕掛け",
        "χの悲劇", "ψの悲劇", "ω城の惨劇",
    ],
    "w": [
        "彼女は一人で歩くのか？", "魔法の色を知っているか？", "風は青海を渡るのか？",
        "デボラ、眠っているのか？", "私たちは生きているのか？", "青白く輝く月を見たか？",
        "ペガサスの解は虚栄か？", "血か、死か、無か？", "天空の矢はどこへ？",
        "人間のように泣いたのか？",
    ],
    "ww": [
        "それでもデミアンは一人なのか？", "神はいつ問われるのか？",
        "キャサリンはどのように子供を産んだのか？",
        "幽霊を創出したのは誰か？", "君たちは絶滅危惧種なのか？",
        "リアルの私はどこにいる？", "君が見たのは誰の夢？",
        "何故エリーズは語らなかったのか？",
    ],
}

SKIP_RE = re.compile(
    r"講談社|文庫|タイガ|新潮社|単行本|初出|定価|ISBN|978-|amazon|楽天|"
    r"浮遊工作室|ミステリィ制作部|Copyright|Wシリーズ|Gシリーズ|WWシリーズ|"
    r"^\d{4}年|^\d{2}/\d{2}|^[A-Z\s]+series|^W\s|^WW\s|^G\s"
)


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("br", "p", "div", "tr", "li", "h1", "h2", "h3", "table", "hr"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if tag in ("p", "div", "tr", "li", "h1", "h2", "h3", "table"):
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw, hc = r.read(), r.headers.get_content_charset()

    cands = list(filter(None, [hc]))
    m = re.search(rb"charset=[\"']?([A-Za-z0-9_\-]+)", raw[:3000])
    if m:
        cands.append(m.group(1).decode())
    cands += ["utf-8", "cp932", "euc_jp"]
    for c in cands:
        try:
            text = raw.decode(c)
            break
        except (UnicodeDecodeError, LookupError):
            pass
    else:
        text = raw.decode("utf-8", errors="replace")

    sc = Scan()
    sc.feed(text)
    return re.sub(r"\n{3,}", "\n\n", "".join(sc.out)).strip()


def extract_comment(chunk):
    lines = [l.strip() for l in chunk.split("\n") if l.strip()]
    result = []
    for line in lines:
        if len(line) < 20:
            continue
        if SKIP_RE.search(line):
            continue
        result.append(line)
        if len(result) >= 3:
            break
    return "\n".join(result)


def fetch_series_comments(series_key):
    url = urllib.parse.urljoin(BASE, SERIES_PAGES[series_key])
    print(f"  取得中: {url}", flush=True)

    try:
        text = fetch_text(url)
    except Exception as e:
        print(f"  エラー: {e}", flush=True)
        return [""] * len(SERIES_TITLES[series_key])

    titles = SERIES_TITLES[series_key]
    positions = []
    for title in titles:
        pos = text.find(title)
        if pos >= 0:
            positions.append((pos, title))
        else:
            print(f"  ⚠  見つかりません: {title}", flush=True)

    positions.sort()
    title_to_comment = {}

    for i, (pos, title) in enumerate(positions):
        start = pos + len(title)
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        chunk = text[start:end]
        comment = extract_comment(chunk)
        title_to_comment[title] = comment
        preview = (comment[:40] + "…") if len(comment) > 40 else (comment or "(空)")
        print(f"  vol{i+1} 『{title[:12]}』→ {preview}", flush=True)

    return [title_to_comment.get(t, "") for t in titles]


def main():
    candidates = [
        Path(__file__).parent / "mori_volumes.html",
        Path.home() / "Downloads" / "mori_volumes.html",
    ]
    html_path = next((p for p in candidates if p.exists()), None)
    if not html_path:
        sys.exit(
            "エラー: mori_volumes.html が見つかりません。\n"
            "このスクリプトと同じフォルダか Downloads フォルダに置いてください。"
        )

    print(f"対象ファイル: {html_path}\n")
    all_comments = {}

    for series in ("g", "w", "ww"):
        print(f"=== {series.upper()} シリーズ ===")
        all_comments[series] = fetch_series_comments(series)
        time.sleep(2.0)

    json_path = html_path.parent / "author_comments.json"
    json_path.write_text(
        json.dumps(all_comments, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nJSON 保存: {json_path}")

    html = html_path.read_text(encoding="utf-8")

    new_comments = "const COMMENTS={\n"
    for series, comments in all_comments.items():
        escaped = [json.dumps(c, ensure_ascii=False) for c in comments]
        new_comments += f" {series}:[{','.join(escaped)}],\n"
    new_comments += "};"

    pattern = r"/\* __COMMENTS_START__ \*/(.*?)/\* __COMMENTS_END__ \*/"
    replacement = (
        f"/* __COMMENTS_START__ */\n{new_comments}\n/* __COMMENTS_END__ */"
    )

    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

    if new_html == html:
        print(
            "\n⚠  HTML にマーカーが見つかりませんでした。"
            "novel/mori_volumes.html（このリポジトリのもの）を対象にしているか確認してください。"
        )
    else:
        html_path.write_text(new_html, encoding="utf-8")
        print(f"✓  HTML 更新完了: {html_path}")

    print("\n完了。ブラウザで mori_volumes.html を開いて確認してください。")


if __name__ == "__main__":
    main()
