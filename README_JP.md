<h1 align="center">
<sub>
<img width="38" src="https://github.com/user-attachments/assets/465e2016-5615-48a9-94a9-676d632f9e86" />
</sub>
Batch Folders
</h1>

Batch Foldersは、ワンクリックで複数のフォルダーを一括で作成することができるWindowsアプリケーションです。

## 特徴

- コンテキストメニューからどこでも右クリックしてフォルダセットを作成できます。
- 英語と日本語の多言語に対応しています。
- 複数のフォルダセットを作成、名前変更、管理することができます。

## 使い方

1. リリースページから最新の `BatchFolders.exe` をダウンロードします。
2. **セットの作成**
   - `BatchFolders.exe` を実行します。
   - 「セット追加」をクリックし、名前を付けます。
   - 作成したいフォルダ名を入力します（1行に1つ）。
   - 「保存して更新」をクリックします。

3. **コンテキストメニューからの使用**
   - デスクトップまたはフォルダ内で右クリックします。
   - `Batch Folders` > `[セット名]` を選択します。
   - フォルダが即座に作成されます。

https://github.com/user-attachments/assets/9bcaca61-c935-48b3-9cea-ffb334374549

## 開発

### 必要要件

- Python 3.x
- `customtkinter`
- `pyinstaller` (ビルド用)

### セットアップ

```bash
pip install -r requirements.txt
```

### ビルド

```bash
python build.py
```

## ライセンス

MIT
