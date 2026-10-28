# 生成スクリプト（記録用）

`index.html` の作者コメントデータを浮遊工作室（ミステリィ制作部）から取得・生成するために使った Python スクリプト。
実行には使わない記録用のアーカイブ。データ取得元: https://www.ne.jp/asahi/beat/non/mori/myst/

## 現行パイプライン（全シリーズ対応版）

1. **`fetch_all_debug.py`** — 全17シリーズページを取得し `debug_all/*.txt` に保存（2秒間隔）
2. **`extract_all_comments.py`** — 英語タイトルをアンカーに作者コメントを抽出し `author_comments_all.json` に出力
3. **`update_html_series.py`** — HTML の `/* __COMMENTS_START__ */` … `/* __COMMENTS_END__ */` ブロックを置換

## 初期版（G/W/WW のみ）

- `debug_pages.py` — G/W/WW ページ取得
- `extract_from_debug.py` — G/W/WW のコメント抽出＋HTML更新
- `update_mori_comments.py` — 初期の取得・更新スクリプト

## 実装メモ

- 日本語タイトルはHTML要素分割で複数行に割れるため、常に1行で出る英語タイトルをアンカーに使う
- `re.sub` の置換文字列は `\n` を実改行に展開してJS文字列を壊すため、必ず `lambda m: replacement` を使う
- 文字コードは HTTPヘッダ → metaタグ → utf-8/cp932/euc_jp の順でフォールバック
