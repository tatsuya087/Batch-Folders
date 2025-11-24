import sys
import os
import tkinter as tk
from tkinter import messagebox
from main_gui import BatchFoldersGUI
from folder_creator import FolderCreator
from config_manager import ConfigManager

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "create":
            if len(sys.argv) < 4:
                print("Usage: batch_folders.py create <set_name> <target_path>")
                return
            
            set_name = sys.argv[2]
            target_path = sys.argv[3]
            
            config_mgr = ConfigManager()
            creator = FolderCreator(config_mgr)
            
            success, msg = creator.create_folders(set_name, target_path)
            
            if not success:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Batch Folders Error", msg)
                root.destroy()
            
        else:
            print(f"Unknown command: {command}")
            
    else:
        app = BatchFoldersGUI()
        app.mainloop()

if __name__ == "__main__":
    main()
