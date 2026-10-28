#!/usr/bin/env python3
"""debug_all/debug_*.txt から全シリーズの作者コメントを抽出し、
mori_volumes.html の COMMENTS ブロックを更新するスクリプト。"""

import json, re
from pathlib import Path

BASE = Path(__file__).parent
DEBUG_DIR = BASE / "debug_all"

# 英語タイトル（完全一致検索のアンカー）
EN_TITLES = {
    "sm": [
        "The Perfect Insider",
        "Doctors in Isolated Room",
        "Mathematical Goodbye",
        "Jack the Poetical Private",
        "Who Inside",
        "Illusion Acts Like Magic",
        "Replaceable Summer",
        "Switch Back",
        "Numerical Models",
        "The Perfect Outsider",
    ],
    "v": [
        "Delta in the Darkness",
        "Shape of Things Human",
        "The Sound Walks When the Moon Talks",
        "You May Die in My Show",
        "Cockpit on Knife Edge",
        "A Sea of Deceits",
        "Six Supersonic Scientists",
        "The Riddle in Torsional Nest",
        "Rot off and Drop away",
        "Red Green Black and White",
    ],
    "sh": [
        "Green Spring",   # "The Four Seasons\nGreen Spring" の後半
        "Red Summer",
        "White Autumn",
        "Black Winter",
    ],
    "g": [
        "Path connected φ broke",
        "Another playmate θ",
        "Please stay until τ",
        "Swearing on solemn ε",
        "λ has no teeth",
        "Dreamily in spite of η",
        "Disinfectant α  for the eyes",   # 原文の二重スペース
        "Jig β knows Heaven",
        "Kiwi γ in Clockwork",
        "The Tragedy of χ",
        "The Tragedy of ψ",
        "SAIKAWA Sohei's Last Case",
    ],
    "x": [
        "Peekaboo",
        "Cutthroat",
        "Crucifixion",
        "Reminiscence",
        "Explosive",
        "Swindler",
    ],
    "xx": [
        "Fool Lie Bow",
        "Song End Sea",
        "Scene Killer",
    ],
    "mr": [
        "God Save the Queen",
        "Labyrinth in Arm of Morpheus",
        "Lady Scarlet Eyes and Her Deliquescence",
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
        "How Did Catherine Cooper Have a Child ?",   # 原文スペース注意
        "Who Created the Ghost",
        "Are You Endangered Species?",
        "Where Am I on the Real Side?",
        "Whose Dream Did You See?",
        "Why Didn't Elise Speak?",
    ],
    "sc": [
        "None But Air",
        "Down to Heaven",
        "Flutter into Life",
        "Cradle the Sky",
        "The Sky Crawlers",
        "Sky Eclipse",
    ],
    "vs": [
        "The Void Shaper",
        "The Blood Scooper",
        "The Skull Breaker",
        "The Fog Hider",
        "The Mind Quencher",
    ],
    "mizu": [
        "The ordinary of Dr.Mizukaki",
        "The Hesitation of Dr.Mizukaki",
        "The Nirvana of Dr. Mizukaki",
    ],
    "z": [
        "ＺＯＫＵ",
        "ＺＯＫＵＤＡＭ",
        "ＺＯＫＵＲＡＮＧＥＲ",
    ],
    "short": [
        "Which is the Witch?",
        "I'm in Debt to Akiko",
        "Missing under the Mistletoe",
        "A Slice of Terrestrial Globe",
        "The Last Dive to Parachute Museum",
        "Inverse of Void Matrix",
        "Lettuce Fry",
    ],
    "etc": [
        "Until Death Do Us Part",
        "Falling Ropewalkers",
        "Wife at Network",
        "His name is Earl",
        "A phenomenon among students",
        "An Automaton in Long Sleep",
        "Eccentric persons are in stock",
        "Zola with a blow and goodbye",
        "Only the Darkness or Her Kiss",
        "Incombustibles",
        "Transcendence of Ginga Estate Agency",
        "Lost heart for Thoma",
        "The Silent World of Dr. Kishima",
        "Running in the Blood",
        "Experimental experience",
        "Dieu aime Lion",
        "The shadow of Ideas",
    ],
    "cream": [
        "The cream of the notes",
        "The cream of the notes 2",
        "The cream of the notes 3",
        "The cream of the notes 4",
        "The cream of the notes 5",
        "The cream of the notes 6",
        "The cream of the notes 7",
        "The cream of the notes 8",
        "The cream of the notes 9",
        "The cream of the notes 10",
        "The cream of the notes 11",
        "The cream of the notes 12",
        "The cream of the notes 13",
        "The cream of the notes 14",
    ],
}

# どのデバッグファイルを使うか（シリーズキー→ファイル名）
DEBUG_FILES = {
    "sm":    "debug_sm.txt",
    "v":     "debug_v.txt",
    "sh":    "debug_sh.txt",
    "g":     "debug_g.txt",
    "x":     "debug_x.txt",
    "xx":    "debug_xx.txt",
    "mr":    "debug_mr.txt",
    "w":     "debug_w.txt",
    "ww":    "debug_ww.txt",
    "sc":    "debug_sc.txt",
    "vs":    "debug_vs.txt",
    "mizu":  "debug_mizu.txt",
    "z":     "debug_z.txt",
    "short": "debug_short.txt",
    "etc":   "debug_etc.txt",
    "cream": "debug_essay.txt",
}

# 除外パターン（書誌情報・ナビゲーション行のみ）
SKIP_RE = re.compile(
    r"^\d{4}[/年]"               # 発行年で始まる行
    r"|^解説："                    # 解説クレジット
    r"|^インタビュー："             # インタビュークレジット
    r"|浮遊工作室"
    r"|Go Back"
    r"|^[A-Z].*series\s*$"        # "S&M series" 等のヘッダー
    r"|シリーズ$"                   # "Ｇシリーズ" 等
    r"|カバーデザイン|装丁|装画|カバーイラスト"
    r"|^ＰＯＰアニメ"               # Shikiシリーズ固有
    r"|^ノベルス版は"               # ノベルス版の表紙情報
    r"|^ノベルス版では"
    r"|^新装版"                    # Sky Crawlers新装版情報
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

for series, debug_file in DEBUG_FILES.items():
    path = DEBUG_DIR / debug_file
    if not path.exists():
        print(f"⚠  {debug_file} が見つかりません。")
        all_comments[series] = [""] * len(EN_TITLES[series])
        continue

    text = path.read_text(encoding="utf-8")
    titles = EN_TITLES[series]
    comments = []

    for i, en_title in enumerate(titles):
        next_title = titles[i + 1] if i + 1 < len(titles) else None
        comment = extract_comment_block(text, en_title, next_title)
        comments.append(comment)
        preview = (comment[:60] + "…") if len(comment) > 60 else (comment or "(空)")
        print(f"  {series} vol{i+1}: {preview}")

    all_comments[series] = comments
    print()

# JSON バックアップ
json_path = BASE / "author_comments_all.json"
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
