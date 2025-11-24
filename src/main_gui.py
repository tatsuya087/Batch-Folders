import customtkinter as ctk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config_manager import ConfigManager
from registry_manager import RegistryManager

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

TRANSLATIONS = {
    "ja": {
        "title": "Batch Folders 設定",
        "folder_sets": "フォルダーセット",
        "add_set": "セットを追加",
        "remove_set": "選択したセットを削除",
        "select_set_label": "セットを選択してください",
        "editing_label": "編集中: {}",
        "save_update": "保存してメニューを更新",
        "remove_menu": "すべて削除",
        "new_set_title": "新しいセット",
        "new_set_prompt": "新しいセット名を入力:",
        "rename_set_title": "セット名の変更",
        "rename_set_prompt": "'{}' の新しい名前を入力:",
        "confirm_delete_title": "確認",
        "confirm_delete_msg": "セット '{}' を削除しますか？",
        "success_title": "成功",
        "success_save_msg": "'{}' を保存し、メニューを更新しました。",
        "success_remove_menu": "メニューから削除しました。",
        "error_title": "エラー",
        "error_exists": "そのセット名は既に存在します。",
        "warning_title": "警告",
        "warning_save_fail": "保存しましたが、レジストリの更新に失敗しました:\n{}",
        "info_select_first": "先にセットを選択してください。",
        "input_helper": "作成したいフォルダー名を1行に1つずつ入力してください。",
        "lang_label": "言語 / Language"
    },
    "en": {
        "title": "Batch Folders Settings",
        "folder_sets": "Folder Sets",
        "add_set": "Add Set",
        "remove_set": "Remove Selected Set",
        "select_set_label": "Select a Set",
        "editing_label": "Editing: {}",
        "save_update": "Save & Update Menu",
        "remove_menu": "Remove All",
        "new_set_title": "New Set",
        "new_set_prompt": "Enter name for new set:",
        "rename_set_title": "Rename Set",
        "rename_set_prompt": "Enter new name for '{}':",
        "confirm_delete_title": "Confirm",
        "confirm_delete_msg": "Delete set '{}'?",
        "success_title": "Success",
        "success_save_msg": "Saved '{}' and updated menu.",
        "success_remove_menu": "Removed from Context Menu.",
        "error_title": "Error",
        "error_exists": "Set already exists.",
        "warning_title": "Warning",
        "warning_save_fail": "Saved but registry update failed:\n{}",
        "info_select_first": "Please select a set first.",
        "input_helper": "Enter one folder name per line.",
        "lang_label": "Language"
    }
}

class BatchFoldersGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config_manager = ConfigManager()
        self.lang = self.config_manager.get_language()
        self.t = TRANSLATIONS[self.lang]

        self.title(self.t["title"])
        
        self.geometry(self.config_manager.get_window_geometry())
        self.minsize(632, 470)

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            self.app_path = sys.executable
            window_icon_path = os.path.join(base_path, "icon.ico")
            registry_icon_path = sys.executable
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            py_path = sys.executable.replace("pythonw.exe", "python.exe")
            script_path = os.path.abspath(__file__).replace("main_gui.py", "batch_folders.py")
            self.app_path = f'"{py_path}" "{script_path}"'
            window_icon_path = os.path.join(base_path, "icon.ico")
            registry_icon_path = window_icon_path

        try:
            self.iconbitmap(window_icon_path)
        except Exception as e:
            print(f"Failed to set window icon: {e}")

        self.font_name = "IBM Plex Sans JP SemiBold"
        font_file = "IBMPlexSansJP-SemiBold.ttf"
        font_path = os.path.join(base_path, font_file)
        self.load_custom_font(font_path)

        self.main_font = ctk.CTkFont(family=self.font_name, size=14)
        self.text_font = ctk.CTkFont(family=self.font_name, size=12)
        self.header_font = ctk.CTkFont(family=self.font_name, size=18, weight="bold")

        self.registry_manager = RegistryManager(self.app_path, icon_path=registry_icon_path)

        self._init_ui()
        
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        if event.widget == self:
            if hasattr(self, "_resize_timer"):
                self.after_cancel(self._resize_timer)
            self._resize_timer = self.after(500, self.save_window_geometry)

    def save_window_geometry(self):
        self.config_manager.set_window_geometry(self.geometry())

    def load_custom_font(self, font_path):
        try:
            import ctypes
            if os.path.exists(font_path):
                ctypes.windll.gdi32.AddFontResourceExW(font_path, 0x10, 0)
        except Exception as e:
            print(f"Failed to load font: {e}")

    def _init_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_rowconfigure(1, weight=1) 
        left_frame.grid_columnconfigure(0, weight=1) 

        self.sets_label = ctk.CTkLabel(left_frame, text=self.t["folder_sets"], font=self.header_font)
        self.sets_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew") 
        
        self.sets_scroll_frame = ctk.CTkScrollableFrame(left_frame, label_text="")
        self.sets_scroll_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")
        
        btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.add_btn = ctk.CTkButton(btn_frame, text=self.t["add_set"], command=self.add_set, font=self.text_font)
        self.add_btn.pack(fill="x", pady=(0, 5))

        self.remove_btn = ctk.CTkButton(btn_frame, text=self.t["remove_set"], command=self.remove_set, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), font=self.text_font, state="disabled")
        self.remove_btn.pack(fill="x")

        settings_frame = ctk.CTkFrame(left_frame)
        settings_frame.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="ew")
        
        ctk.CTkLabel(settings_frame, text=self.t["lang_label"], font=self.text_font).pack(anchor="w", padx=10, pady=(5,0))
        self.lang_var = ctk.StringVar(value=self.lang)
        self.lang_combo = ctk.CTkComboBox(settings_frame, values=["ja", "en"], command=self.change_language, variable=self.lang_var, font=self.text_font, state="readonly")
        self.lang_combo.pack(fill="x", padx=10, pady=5)

        self.remove_reg_btn = ctk.CTkButton(settings_frame, text=self.t["remove_menu"], command=self.remove_registry, fg_color="#FF5555", hover_color="#CC0000", font=self.text_font)
        self.remove_reg_btn.pack(fill="x", padx=10, pady=(5, 10))

        right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        right_frame.grid_rowconfigure(2, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        self.set_label = ctk.CTkLabel(right_frame, text=self.t["select_set_label"], font=self.header_font)
        self.set_label.grid(row=0, column=0, sticky="ew", pady=(0, 5)) 

        self.helper_label = ctk.CTkLabel(right_frame, text=self.t["input_helper"], font=self.text_font, text_color="gray", justify="left")
        self.helper_label.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        self.helper_label.bind('<Configure>', lambda e: self.helper_label.configure(wraplength=e.width))

        self.folders_textbox = ctk.CTkTextbox(right_frame, font=self.text_font)
        self.folders_textbox.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        
        # Configure internal text widget to ensure font is applied during IME composition
        # Use tuple format (Family, Size) which is robust for Tkinter
        font_tuple = (self.font_name, 12)
        self.folders_textbox._textbox.configure(font=font_tuple)
        
        # Re-apply on focus in to ensure it persists
        self.folders_textbox._textbox.bind("<FocusIn>", lambda e: self.folders_textbox._textbox.configure(font=font_tuple))
        
        self.save_btn = ctk.CTkButton(right_frame, text=self.t["save_update"], command=self.save_and_update, font=self.main_font, height=40)
        self.save_btn.grid(row=3, column=0, sticky="ew")

        self.selected_set_name = None
        self.set_buttons = []
        self.refresh_sets_list()

    def change_language(self, choice):
        self.config_manager.set_language(choice)
        self.lang = choice
        self.t = TRANSLATIONS[self.lang]
        self.update_ui_text()

    def update_ui_text(self):
        self.title(self.t["title"])
        self.sets_label.configure(text=self.t["folder_sets"])
        self.add_btn.configure(text=self.t["add_set"])
        self.remove_btn.configure(text=self.t["remove_set"])
        self.save_btn.configure(text=self.t["save_update"])
        self.remove_reg_btn.configure(text=self.t["remove_menu"])
        self.helper_label.configure(text=self.t["input_helper"])
        
        if self.selected_set_name:
            self.set_label.configure(text=self.t["editing_label"].format(self.selected_set_name))
        else:
            self.set_label.configure(text=self.t["select_set_label"])

    def refresh_sets_list(self):
        for btn in self.set_buttons:
            btn.destroy()
        self.set_buttons = []

        sets = self.config_manager.get_sets()
        for name in sets:
            btn = ctk.CTkButton(self.sets_scroll_frame, text=name, command=lambda n=name: self.select_set(n), fg_color="transparent", text_color=("gray10", "#DCE4EE"), anchor="w", font=self.text_font)
            btn.pack(fill="x", padx=5, pady=2)
            
            btn.bind("<Double-Button-1>", lambda event, n=name: self.rename_set_dialog(n))
            
            self.set_buttons.append(btn)

    def select_set(self, set_name):
        self.selected_set_name = set_name
        self.set_label.configure(text=self.t["editing_label"].format(set_name))
        
        for btn in self.set_buttons:
            if btn.cget("text") == set_name:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")

        folders = self.config_manager.get_set_folders(set_name)
        self.folders_textbox.delete("1.0", "end")
        self.folders_textbox.insert("1.0", "\n".join(folders))
        
        self.remove_btn.configure(state="normal")

    def _center_dialog(self, dialog_width=300, dialog_height=200):
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog_width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog_height // 2)
        return f"+{x}+{y}"

    def add_set(self):
        dialog = ctk.CTkInputDialog(text=self.t["new_set_prompt"], title=self.t["new_set_title"])
        dialog.geometry(self._center_dialog(300, 150))
        name = dialog.get_input()
        if name:
            if name in self.config_manager.get_sets():
                messagebox.showerror(self.t["error_title"], self.t["error_exists"], parent=self)
                return
            self.config_manager.add_set(name, [])
            self.refresh_sets_list()
            self.select_set(name)

    def rename_set_dialog(self, old_name):
        dialog = ctk.CTkInputDialog(text=self.t["rename_set_prompt"].format(old_name), title=self.t["rename_set_title"])
        dialog.geometry(self._center_dialog(300, 150))
        new_name = dialog.get_input()
        if new_name and new_name != old_name:
            if new_name in self.config_manager.get_sets():
                messagebox.showerror(self.t["error_title"], self.t["error_exists"], parent=self)
                return
            
            self.config_manager.rename_set(old_name, new_name)
            self.refresh_sets_list()
            
            if self.selected_set_name == old_name:
                self.select_set(new_name)
            
            sets = self.config_manager.get_sets()
            self.registry_manager.register_context_menu(sets)

    def remove_set(self):
        if self.selected_set_name:
            if messagebox.askyesno(self.t["confirm_delete_title"], self.t["confirm_delete_msg"].format(self.selected_set_name), parent=self):
                self.config_manager.remove_set(self.selected_set_name)
                self.refresh_sets_list()
                self.folders_textbox.delete("1.0", "end")
                self.selected_set_name = None
                self.set_label.configure(text=self.t["select_set_label"])
                self.remove_btn.configure(state="disabled")
                
                sets = self.config_manager.get_sets()
                self.registry_manager.register_context_menu(sets)

    def save_and_update(self):
        if self.selected_set_name:
            content = self.folders_textbox.get("1.0", "end").strip()
            folders = [line.strip() for line in content.split("\n") if line.strip()]
            self.config_manager.add_set(self.selected_set_name, folders)
            
            sets = self.config_manager.get_sets()
            success, msg = self.registry_manager.register_context_menu(sets)
            
            if success:
                messagebox.showinfo(self.t["success_title"], self.t["success_save_msg"].format(self.selected_set_name), parent=self)
            else:
                messagebox.showwarning(self.t["warning_title"], self.t["warning_save_fail"].format(msg), parent=self)
        else:
            messagebox.showinfo("Info", self.t["info_select_first"], parent=self)

    def remove_registry(self):
        success, msg = self.registry_manager.unregister_context_menu()
        if success:
            messagebox.showinfo(self.t["success_title"], self.t["success_remove_menu"], parent=self)
        else:
            messagebox.showerror(self.t["error_title"], msg, parent=self)

if __name__ == "__main__":
    app = BatchFoldersGUI()
    app.mainloop()
