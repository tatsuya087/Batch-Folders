<h1 align="center">
<sub>
<img width="38" src="https://github.com/user-attachments/assets/465e2016-5615-48a9-94a9-676d632f9e86" />
</sub>
Batch Folders
</h1>

<p align="center">
[日本語のREADMEはこちら](README_JP.md)
</p>

<p align="center">
Batch Folders is a Windows application that allows you to create multiple folders in batch with a single click.</p>

<hr>

## Features

- Instantly create multiple folders with a right-click.
- Supports English and Japanese UI.
- Create, rename, and manage multiple folder sets.

## Usage

1. Download the latest `BatchFolders.exe` from the releases page.
2. **Create a Set**
   - Run `BatchFolders.exe`.
   - Click "Add Set" and give it a name.
   - Enter the folder names you want to create (one per line).
   - Click "Save & Update".

3. **Use from Context Menu**
   - Right-click on your Desktop or in File Explorer.
   - Select `Batch Folders` > `[Your Set Name]`.
   - Folders will be created.

https://github.com/user-attachments/assets/9bcaca61-c935-48b3-9cea-ffb334374549

## Building

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
