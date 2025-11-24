# Batch Folders

[日本語のREADMEはこちら](README_JP.md)

Batch Folders is a Windows application that allows you to create a predefined set of folders with a single click from the context menu.

## Features

- **Context Menu Integration**: Right-click anywhere to create a set of folders.
- **Localization**: Supports English and Japanese.
- **Customizable**: Create, rename, and manage multiple folder sets.

## Installation

1. Download the latest `BatchFolders.exe` from the releases page.
2. Run `BatchFolders.exe`.
3. Create your folder sets and click "Save & Update Menu".

## Usage

1. **Create a Set**:
   - Open the app.
   - Click "Add Set" and give it a name.
   - Enter the folder names you want to create (one per line).
   - Click "Save & Update Menu".

2. **Use from Context Menu**:
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
