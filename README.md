<h1 align="center">
<sub>
<img width="38" src="https://github.com/user-attachments/assets/465e2016-5615-48a9-94a9-676d632f9e86" />
</sub>
Batch Folders
</h1>

[日本語のREADMEはこちら](README_JP.md)

Batch Folders is a Windows application that allows you to create multiple folders in batch with a single click.

Batch Foldersは、ワンクリックで複数のフォルダーを一括で作成することができるWindowsアプリケーションです。

## Features

- Right-click anywhere to create a set of folders via the context menu.
- Supports both English and Japanese languages.
- Create, rename, and manage multiple folder sets.

## Usage

1. Download the latest `BatchFolders.exe` from the releases page.
2. **Create a Set**
   - Run `BatchFolders.exe`.
   - Click "Add Set" and give it a name.
   - Enter the folder names you want to create (one per line).
   - Click "Save & Update".

3. **Use from Context Menu**
   - Right-click on your Desktop or inside any folder.
   - Select `Batch Folders` > `[Your Set Name]`.
   - The folders will be created instantly.

https://github.com/user-attachments/assets/9bcaca61-c935-48b3-9cea-ffb334374549

## Development

### Requirements

- Python 3.x
- `customtkinter`
- `pyinstaller` (for building)

### Setup

```bash
pip install -r requirements.txt
```

### Build

```bash
python build.py
```

## License

MIT
