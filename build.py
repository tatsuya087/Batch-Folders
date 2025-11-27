import PyInstaller.__main__
import os

print("Building Batch Folders EXE...")

src_path = os.path.join(os.getcwd(), "src")
font_path = os.path.join(src_path, "GenYoGothic2JP-B.otf")
icon_path = os.path.join(src_path, "icon.ico")

PyInstaller.__main__.run([
    os.path.join(src_path, 'batch_folders.py'),
    '--onefile',
    '--windowed',
    '--name=Batch Folders 1.00',
    '--clean',
    f'--add-data={font_path};.',
    f'--add-data={icon_path};.',
    '--collect-all=customtkinter',
    f'--paths={src_path}',
    f'--icon={icon_path}',
])

print("Build complete. Check 'dist' folder.")
