# Batch Folders

[日本語のREADMEはこちら](README_JP.md)

Batch Folders is a Windows application that allows you to create multiple folders at once with a single click.

Batch Foldersは、ワンクリックで複数のフォルダ一気に作成できるWindowsアプリケーションです。

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
