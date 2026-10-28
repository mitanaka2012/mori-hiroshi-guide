#!/usr/bin/env python3
"""debug_*.txt から英語タイトルをアンカーにして作者コメントを抽出し、
mori_volumes.html の COMMENTS ブロックを更新するスクリプト。"""

import json, re
from pathlib import Path

BASE = Path(__file__).parent

# 英語タイトル（完全一致で使用。サイト上の表記のまま）
EN_TITLES = {
    "g": [
        "Path connected φ broke",
        "Another playmate θ",
        "Please stay until τ",
        "Swearing on solemn ε",
        "λ has no teeth",
        "Dreamily in spite of η",
        "Disinfectant α  for the eyes",   # ← 原文の二重スペースに注意
        "Jig β knows Heaven",
        "Kiwi γ in Clockwork",
        "The Tragedy of χ",
        "The Tragedy of ψ",
        "SAIKAWA Sohei's Last Case",
    ],
    "w": [
        "Does She Walk Alone?",
        "What Color is the Magic?",
        "The Wind Across Qinghai Lake?",
        "Deborah, Are You Sleeping?",
        "Are We Under the Biofeedback?",
        "Did the Moon Shed a Pale Light?",
        "Did Pegasus Answer the Vanity?",
        "Is It Blood, Death or Null?",
        "Where is the Sky Arrow?",
        "Did She Cry Humanly?",
    ],
    "ww": [
        "Still Does Demian Have Only One Brain?",
        "When Will God be Questioned?",
        "How Did Catherine Cooper Have a Child ?",   # ← 原文スペース注意
        "Who Created the Ghost",
        "Are You Endangered Species?",
        "Where Am I on the Real Side?",
        "Whose Dream Did You See?",
        "Why Didn't Elise Speak?",
    ],
}

# 除外パターン（書誌情報行のみ。コメント本文は除外しない）
SKIP_RE = re.compile(
    r"^\d{4}[/年]"          # 発行年で始まる行
    r"|^解説："              # 解説クレジット
    r"|浮遊工作室"
    r"|Go Back"
    r"|^W?W series"
    r"|Ｇシリーズ$|Ｗシリーズ$|ＷＷシリーズ$"   # ヘッダー行
    r"|カバーデザイン|装丁|装画|カバーイラスト"   # カバー関連
)


def extract_comment_block(text, en_title, next_en_title):
    """英語タイトル以降～次の英語タイトルまでのブロックからコメントを抽出"""
    start = text.find(en_title)
    if start < 0:
        return ""
    end = text.find(next_en_title, start + len(en_title)) if next_en_title else len(text)
    chunk = text[start + len(en_title):end]

    lines = chunk.split("\n")
    comment_lines = []
    for line in lines:
        stripped = line.strip().lstrip("　 \t")  # 全角スペースも除去
        if not stripped:
            continue
        if SKIP_RE.search(stripped):
            continue
        # 短すぎる行（10文字未満）は書誌断片として除外
        if len(stripped) < 10:
            continue
        comment_lines.append(stripped)

    return "\n".join(comment_lines)


all_comments = {}

for series, debug_file in [("g", "debug_g.txt"), ("w", "debug_w.txt"), ("ww", "debug_ww.txt")]:
    path = BASE / debug_file
    if not path.exists():
        print(f"⚠  {debug_file} が見つかりません。debug_pages.py を先に実行してください。")
        all_comments[series] = [""] * len(EN_TITLES[series])
        continue

    text = path.read_text(encoding="utf-8")
    titles = EN_TITLES[series]
    comments = []

    for i, en_title in enumerate(titles):
        next_title = titles[i + 1] if i + 1 < len(titles) else None
        comment = extract_comment_block(text, en_title, next_title)
        comments.append(comment)
        preview = (comment[:50] + "…") if len(comment) > 50 else (comment or "(空)")
        print(f"  {series} vol{i+1}: {preview}")

    all_comments[series] = comments

# JSON バックアップ
json_path = BASE / "author_comments.json"
json_path.write_text(json.dumps(all_comments, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nJSON 保存: {json_path}")

# HTML の COMMENTS ブロックを置き換え
html_path = BASE / "mori_volumes.html"
html = html_path.read_text(encoding="utf-8")

new_block = "const COMMENTS={\n"
for series, comments in all_comments.items():
    escaped = [json.dumps(c, ensure_ascii=False) for c in comments]
    new_block += f" {series}:[{','.join(escaped)}],\n"
new_block += "};"

pattern = r"/\* __COMMENTS_START__ \*/(.*?)/\* __COMMENTS_END__ \*/"
replacement = f"/* __COMMENTS_START__ */\n{new_block}\n/* __COMMENTS_END__ */"
new_html = re.sub(pattern, lambda m: replacement, html, flags=re.DOTALL)

if new_html == html:
    print("⚠  マーカーが見つかりません。")
else:
    html_path.write_text(new_html, encoding="utf-8")
    print(f"✓  HTML 更新完了: {html_path}")
