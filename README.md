# みんなの早押しクイズ 自動操作

## 使用方法

### はじめに

1. Vysor をインストール
    - https://www.vysor.io/
2. Vysor で Android 版のみんなの早押しクイズを開き、クイズリストページを開く
3. `python ./main.py position` を実行し、 `constants.py` の中の各ボタンの座標を確認しながらアップデートする

### 問題の追加

```
python ./main.py add_quiz [CSVまでのパス]
```

## requirements

### install
```
pip install -r requirements.txt
```

### freeze
```
pip freeze > requirements.txt
```
