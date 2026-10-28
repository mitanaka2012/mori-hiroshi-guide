#!/usr/bin/env python3
"""mori_volumes.html に新シリーズのCSS変数と S データを追加する。
COMMENTS の更新は extract_all_comments.py で行う。"""

from pathlib import Path

BASE = Path(__file__).parent
HTML_PATH = BASE / "mori_volumes.html"

# ---------- 追加する CSS 変数 ----------
NEW_CSS_LIGHT = (
    ";--sm:#8b3a3a;--sml:#fde8e8"
    ";--v:#4a2d8a;--vl:#ece8fa"
    ";--sh:#2c5a3a;--shl:#e8f5ec"
    ";--x:#2a4060;--xl:#e8eef5"
    ";--xx:#1a5050;--xxl:#e8f5f5"
    ";--mr:#7a4520;--mrl:#f5ece8"
    ";--sc:#1a2a58;--scl:#e8ecf5"
    ";--vs:#3a5820;--vsl:#eef5e8"
    ";--mizu:#1a4a68;--mizul:#e8f0f5"
    ";--z:#383840;--zl:#f0f0f2"
    ";--short:#581a4a;--shortl:#f5e8f2"
    ";--etc:#2a1a58;--etcl:#ece8f5"
    ";--cream:#5c3a10;--creaml:#f5f0e8"
)

NEW_CSS_DARK = (
    ";--sm:#d07070;--sml:#3a2020"
    ";--v:#9a78d4;--vl:#2a1a3a"
    ";--sh:#70c898;--shl:#1a2a20"
    ";--x:#7898c4;--xl:#1a2230"
    ";--xx:#60c4c4;--xxl:#1a2a2a"
    ";--mr:#c87040;--mrl:#3a2010"
    ";--sc:#6878c4;--scl:#1a1e2a"
    ";--vs:#90c450;--vsl:#202a10"
    ";--mizu:#50a0c8;--mizul:#1a2828"
    ";--z:#9898a0;--zl:#202022"
    ";--short:#c060a0;--shortl:#2a1a24"
    ";--etc:#7070c8;--etcl:#1a1a2a"
    ";--cream:#c0901a;--creaml:#2a1c08"
)


def vol_entry(num, title, date):
    return f"[{num},'{title}','{date}','','',[],'']"


# ---------- 新シリーズ S エントリ ----------
def build_series(key, name, c, cl, intro, vols):
    entries = ",\n ".join(vols)
    return f",{key}:{{name:'{name}',c:'{c}',cl:'{cl}',\n intro:'{intro}',\n vols:[\n {entries}]}}"


SM_VOLS = [
    vol_entry(1, "すべてがＦになる", "1996/4"),
    vol_entry(2, "冷たい密室と博士たち", "1996/7"),
    vol_entry(3, "笑わない数学者", "1996/9"),
    vol_entry(4, "詩的私的ジャック", "1997/1"),
    vol_entry(5, "封印再度", "1997/4"),
    vol_entry(6, "幻惑の死と使途", "1997/10"),
    vol_entry(7, "夏のレプリカ", "1998/1"),
    vol_entry(8, "今はもうない", "1998/4"),
    vol_entry(9, "数奇にして模型", "1998/7"),
    vol_entry(10, "有限と微小のパン", "1998/10"),
]
V_VOLS = [
    vol_entry(1, "黒猫の三角", "1999/5"),
    vol_entry(2, "人形式モナリザ", "1999/9"),
    vol_entry(3, "月は幽咽のデバイス", "2000/1"),
    vol_entry(4, "夢・出逢い・魔性", "2000/5"),
    vol_entry(5, "魔剣天翔", "2000/9"),
    vol_entry(6, "恋恋蓮歩の演習", "2001/5"),
    vol_entry(7, "六人の超音波科学者", "2001/9"),
    vol_entry(8, "捩れ屋敷の利鈍", "2002/1"),
    vol_entry(9, "朽ちる散る落ちる", "2002/5"),
    vol_entry(10, "赤緑黒白", "2002/9"),
]
SH_VOLS = [
    vol_entry(1, "四季 春", "2003/9"),
    vol_entry(2, "四季 夏", "2003/11"),
    vol_entry(3, "四季 秋", "2004/1"),
    vol_entry(4, "四季 冬", "2004/3"),
]
X_VOLS = [
    vol_entry(1, "イナイ×イナイ", "2007/5"),
    vol_entry(2, "キラレ×キラレ", "2007/9"),
    vol_entry(3, "タカイ×タカイ", "2008/1"),
    vol_entry(4, "ムカシ×ムカシ", "2014/6"),
    vol_entry(5, "サイタ×サイタ", "2014/11"),
    vol_entry(6, "ダマシ×ダマシ", "2017/5"),
]
XX_VOLS = [
    vol_entry(1, "馬鹿と嘘の弓", "2020/10"),
    vol_entry(2, "歌の終わりは海", "2021/10"),
    vol_entry(3, "情景の殺人者", "2023/10"),
]
MR_VOLS = [
    vol_entry(1, "女王の百年密室", "2000/6"),
    vol_entry(2, "迷宮百年の睡魔", "2003/6"),
    vol_entry(3, "赤目姫の潮解", "2013/7"),
]
SC_VOLS = [
    vol_entry(1, "ナ・バ・テア", "2004/6"),
    vol_entry(2, "ダウン・ツ・ヘヴン", "2005/6"),
    vol_entry(3, "フラッタ・リンツ・ライフ", "2006/6"),
    vol_entry(4, "クレィドゥ・ザ・スカイ", "2007/6"),
    vol_entry(5, "スカイ・クロラ", "2001/6"),
    vol_entry(6, "スカイ・イクリプス（短編集）", "2008/6"),
]
VS_VOLS = [
    vol_entry(1, "ヴォイド・シェイパ", "2011/4"),
    vol_entry(2, "ブラッド・スクーパ", "2012/4"),
    vol_entry(3, "スカル・ブレーカ", "2013/4"),
    vol_entry(4, "フォグ・ハイダ", "2014/4"),
    vol_entry(5, "マインド・クァンチャ", "2015/4"),
]
MIZU_VOLS = [
    vol_entry(1, "工学部・水柿助教授の日常", "2000/12"),
    vol_entry(2, "工学部・水柿助教授の逡巡", "2004/12"),
    vol_entry(3, "工学部・水柿助教授の解脱", "2008/4"),
]
Z_VOLS = [
    vol_entry(1, "ＺＯＫＵ", "2003/10"),
    vol_entry(2, "ＺＯＫＵＤＡＭ", "2007/7"),
    vol_entry(3, "ＺＯＫＵＲＡＮＧＥＲ", "2009/4"),
]
SHORT_VOLS = [
    vol_entry(1, "どちらかが魔女", "2008/8"),
    vol_entry(2, "僕は秋子に借りがある", "2008/8"),
    vol_entry(3, "まどろみ消去", "1997/7"),
    vol_entry(4, "地球儀のスライス", "1999/1"),
    vol_entry(5, "今夜はパラシュート博物館へ", "2001/1"),
    vol_entry(6, "虚空の逆マトリクス", "2003/1"),
    vol_entry(7, "レタス・フライ", "2006/1"),
]
ETC_VOLS = [
    vol_entry(1, "そして二人だけになった", "1999/6"),
    vol_entry(2, "墜ちていく僕たち", "2001/6"),
    vol_entry(3, "奥様はネットワーカ", "2002/7"),
    vol_entry(4, "探偵伯爵と僕", "2004/4"),
    vol_entry(5, "どきどきフェノメノン", "2005/4"),
    vol_entry(6, "カクレカラクリ", "2006/8"),
    vol_entry(7, "少し変わった子あります", "2006/8"),
    vol_entry(8, "ゾラ・一撃・さようなら", "2007/8"),
    vol_entry(9, "暗闇・キッス・それだけで", "2015/1"),
    vol_entry(10, "もえない", "2007/12"),
    vol_entry(11, "銀河不動産の超越", "2008/5"),
    vol_entry(12, "トーマの心臓", "2009/7"),
    vol_entry(13, "喜嶋先生の静かな世界", "2010/10"),
    vol_entry(14, "相田家のグッドバイ", "2012/2"),
    vol_entry(15, "実験的経験", "2012/5"),
    vol_entry(16, "神様が殺してくれる", "2013/6"),
    vol_entry(17, "イデアの影", "2015/11"),
]
CREAM_VOLS = [
    vol_entry(1, "つぶやきのクリーム", "2011/9"),
    vol_entry(2, "つぼやきのテリーヌ", "2013/12"),
    vol_entry(3, "つぼねのカトリーヌ", "2014/12"),
    vol_entry(4, "ツンドラモンスーン", "2015/12"),
    vol_entry(5, "つぼみ茸ムース", "2016/12"),
    vol_entry(6, "つぶさにミルフィーユ", "2017/12"),
    vol_entry(7, "月夜のサラサーテ", "2018/12"),
    vol_entry(8, "つんつんブラザーズ", "2019/12"),
    vol_entry(9, "ツベルクリンムーチョ", "2020/12"),
    vol_entry(10, "追懐のコヨーテ", "2021/12"),
    vol_entry(11, "積み木シンドローム", "2022/12"),
    vol_entry(12, "妻のオンパレード", "2023/12"),
    vol_entry(13, "つむじ風のスープ", "2024/12"),
    vol_entry(14, "つくねもハンバーグ", "2025/12"),
]

NEW_SERIES_BLOCK = (
    build_series("sm", "S&M シリーズ", "--sm", "--sml",
                 "犀川創平と西之園萌絵のコンビが謎を解く本格ミステリィシリーズ（全10作）。密室ものを中心に那古野市周辺が主な舞台です。",
                 SM_VOLS) +
    build_series("v", "V シリーズ", "--v", "--vl",
                 "瀬在丸紅子・小鳥遊練無ら4人組が事件を解くシリーズ（全10作）。S&Mシリーズとほぼ同時期に並行して書かれました。",
                 V_VOLS) +
    build_series("sh", "四季シリーズ", "--sh", "--shl",
                 "天才科学者・真賀田四季の生涯を描いた全4作。もともと1つの作品を分冊して発行したものです。",
                 SH_VOLS) +
    build_series("x", "X シリーズ", "--x", "--xl",
                 "個性的な探偵コンビが活躍するシリーズ（全6作）。G・Vシリーズとは異なるレトロな雰囲気を持ちます。",
                 X_VOLS) +
    build_series("xx", "XX シリーズ", "--xx", "--xxl",
                 "Xシリーズの流れを汲む、地味な探偵コンビが登場するシリーズ（既刊3作）。",
                 XX_VOLS) +
    build_series("mr", "百年シリーズ", "--mr", "--mrl",
                 "百年後の未来を舞台に、人造人間・ロイディと人間のコンビが活躍するシリーズ（全3作）。",
                 MR_VOLS) +
    build_series("sc", "スカイ・クロラ", "--sc", "--scl",
                 "永遠に生きる少年兵士たちが空を飛び続ける世界を描いた幻想的なシリーズ（全5作＋短編集）。",
                 SC_VOLS) +
    build_series("vs", "ヴォイド・シェイパ", "--vs", "--vsl",
                 "森の中で一人剣を磨く若者が旅をする、時代劇・ファンタジィ寄りのシリーズ（全5作）。",
                 VS_VOLS) +
    build_series("mizu", "水柿シリーズ", "--mizu", "--mizul",
                 "工学部の水柿助教授と妻・須摩子さんの日常を描いたアンチミステリィ（全3作）。",
                 MIZU_VOLS) +
    build_series("z", "Z シリーズ", "--z", "--zl",
                 "雑誌ジャーロに連載されたアンチな短編集シリーズ（全3巻、各5短編収録）。",
                 Z_VOLS) +
    build_series("short", "短編集", "--short", "--shortl",
                 "森博嗣の短編をまとめた作品集（全7冊）。シリーズ短編集・自選短編集・テーマ別短編集があります。",
                 SHORT_VOLS) +
    build_series("etc", "シリーズ外", "--etc", "--etcl",
                 "シリーズに属さない長編・単発作品群（全17作）。多彩なジャンルをカバーしています。",
                 ETC_VOLS) +
    build_series("cream", "クリームシリーズ", "--cream", "--creaml",
                 "森博嗣のエッセィシリーズ（全14作）。思いついた短いフレーズと解説をまとめた講談社文庫書下ろし。",
                 CREAM_VOLS)
)


def main():
    html = HTML_PATH.read_text(encoding="utf-8")
    changed = False

    # 1. ライトモードCSS変数を追加（未追加の場合のみ）
    old_light = "--ww:#a4572b;--wwl:#fbeadf}"
    if "--sm:#" not in html:
        new_light = "--ww:#a4572b;--wwl:#fbeadf" + NEW_CSS_LIGHT + "}"
        if old_light in html:
            html = html.replace(old_light, new_light, 1)
            print("✓ ライトモードCSS変数を追加")
            changed = True
        else:
            print("⚠ ライトモードCSSのアンカーが見つかりません")
    else:
        print("  ライトモードCSS変数はすでに存在します")

    # 2. ダークモードCSS変数を追加（未追加の場合のみ）
    old_dark = "--ww:#e8a074;--wwl:#472f20}}"
    if "--sm:#d07070" not in html:
        new_dark = "--ww:#e8a074;--wwl:#472f20" + NEW_CSS_DARK + "}}"
        if old_dark in html:
            html = html.replace(old_dark, new_dark, 1)
            print("✓ ダークモードCSS変数を追加")
            changed = True
        else:
            print("⚠ ダークモードCSSのアンカーが見つかりません")
    else:
        print("  ダークモードCSS変数はすでに存在します")

    # 3. S データに新シリーズを追加（未追加の場合のみ）
    # ww の最終ボリューム行の後、S の閉じ };の前に挿入
    # アンカー: `',[],'']]}` + 改行 + `};`
    if ",sm:{name:" not in html:
        # ww の最後のエントリの末尾を探す
        # "',[],'']]}の後に改行と"};"が来るパターン
        anchor_end = "',[],'']]}\\n};"
        anchor_end_alt = "',[],'']]}\\r\\n};"

        insert_after = "',[],'']]}\\n"

        pos_unix = html.find("',[],'']]}\\n};")
        pos_win  = html.find("',[],'']]}\\r\\n};")

        if pos_unix >= 0:
            insert_at = pos_unix + len("',[],'']]}\\n")
            html = html[:insert_at] + NEW_SERIES_BLOCK + "\\n" + html[insert_at:]
            print("✓ S データに新シリーズを追加")
            changed = True
        elif pos_win >= 0:
            insert_at = pos_win + len("',[],'']]}\\r\\n")
            html = html[:insert_at] + NEW_SERIES_BLOCK + "\\n" + html[insert_at:]
            print("✓ S データに新シリーズを追加 (CRLF)")
            changed = True
        else:
            print("⚠ S データの末尾パターンが見つかりません")
            # デバッグ: 末尾近辺を確認
            idx = html.rfind("']]}\\n};")
            if idx >= 0:
                print("  最後の ']]}\\n}; は", idx, "文字目:", repr(html[idx:idx+20]))
            else:
                idx = html.rfind("']}")
                print("  最後の ']}  は", idx, "文字目:", repr(html[idx:idx+20]))
    else:
        print("  S データの新シリーズはすでに存在します")

    if changed:
        HTML_PATH.write_text(html, encoding="utf-8")
        print(f"\\n✓ HTML 更新完了: {HTML_PATH}")
    else:
        print("\\n変更なし")


if __name__ == "__main__":
    main()
