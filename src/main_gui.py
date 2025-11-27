import customtkinter as ctk
from tkinter import messagebox
import sys
import os
import copy

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
        "save_update": "保存して更新",
        "remove_menu": "すべての設定をリセット",
        "new_set_title": "新しいセット",
        "new_set_prompt": "新しいセット名を入力:",
        "rename_set_title": "セット名の変更",
        "rename_set_prompt": "'{}' の新しい名前を入力:",
        "confirm_delete_title": "確認",
        "confirm_delete_msg": "セット '{}' を削除しますか？",
        "confirm_reset_title": "確認",
        "confirm_reset_msg": "すべての設定をリセットしますか？\nこの操作は取り消せません。",
        "success_title": "成功",
        "success_save_msg": "'{}' を保存し、メニューを更新しました。",
        "success_remove_menu": "メニューから削除しました。",
        "error_title": "エラー",
        "error_exists": "そのセット名は既に存在します。",
        "warning_title": "警告",
        "warning_save_fail": "保存しましたが、レジストリの更新に失敗しました:\n{}",
        "info_select_first": "先にセットを選択してください。",
        "input_helper": "フォルダー名を入力してEnterキーを押すと追加されます。",
        "lang_label": "言語 / Language",
        "input_placeholder": "フォルダー名を入力...",
        "btn_ok": "OK",
        "btn_cancel": "キャンセル"
    },
    "en": {
        "title": "Batch Folders Settings",
        "folder_sets": "Folder Sets",
        "add_set": "Add Set",
        "remove_set": "Remove Selected Set",
        "select_set_label": "Select a Set",
        "editing_label": "Editing: {}",
        "save_update": "Save & Update",
        "remove_menu": "Reset All Settings",
        "new_set_title": "New Set",
        "new_set_prompt": "Enter name for new set:",
        "rename_set_title": "Rename Set",
        "rename_set_prompt": "Enter new name for '{}':",
        "confirm_delete_title": "Confirm",
        "confirm_delete_msg": "Delete set '{}'?",
        "confirm_reset_title": "Confirm",
        "confirm_reset_msg": "Are you sure you want to reset all settings?\nThis cannot be undone.",
        "success_title": "Success",
        "success_save_msg": "Saved '{}' and updated menu.",
        "success_remove_menu": "Removed from Context Menu.",
        "error_title": "Error",
        "error_exists": "Set already exists.",
        "warning_title": "Warning",
        "warning_save_fail": "Saved but registry update failed:\n{}",
        "info_select_first": "Please select a set first.",
        "input_helper": "Type folder name and press Enter to add.",
        "lang_label": "Language",
        "input_placeholder": "Enter folder name...",
        "btn_ok": "OK",
        "btn_cancel": "Cancel"
    }
}

class CustomDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, message, font, icon_path=None, type="info", ok_text="OK", cancel_text="Cancel"):
        super().__init__(parent)
        self.title(title)
        self.font = font
        self.result = False
        
        if icon_path and os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
                # Re-apply icon after a short delay to ensure it sticks
                self.after(200, lambda: self.iconbitmap(icon_path))
            except:
                pass
        
        self.transient(parent)
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        label = ctk.CTkLabel(self, text=message, font=self.font, wraplength=350)
        label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        
        if type == "confirm":
            ok_btn = ctk.CTkButton(self, text=ok_text, command=self.on_ok, font=self.font, width=100)
            ok_btn.grid(row=1, column=0, padx=10, pady=10)
            cancel_btn = ctk.CTkButton(self, text=cancel_text, command=self.on_cancel, font=self.font, fg_color="transparent", border_width=1, width=100)
            cancel_btn.grid(row=1, column=1, padx=10, pady=10)
        else:
            ok_btn = ctk.CTkButton(self, text=ok_text, command=self.on_ok, font=self.font, width=100)
            ok_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.update_idletasks()
        req_width = self.winfo_reqwidth()
        req_height = self.winfo_reqheight()
        
        # Enforce minimum size and 16:9 ratio
        min_width = 360
        min_height = 203 # approx 360 / (16/9)
        
        target_width = max(req_width, min_width)
        target_height = max(req_height, min_height)
        
        # Adjust for 16:9 ratio (width = 1.77 * height)
        ratio = 16/9
        if target_width / target_height < ratio:
            target_width = int(target_height * ratio)
        elif target_width / target_height > ratio:
            target_height = int(target_width / ratio)
            
        width = target_width
        height = target_height
        
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.wait_window()

    def on_ok(self):
        self.result = True
        self.destroy()

    def on_cancel(self):
        self.result = False
        self.destroy()

class CustomInputDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, prompt, font, icon_path=None, ok_text="OK", cancel_text="Cancel"):
        super().__init__(parent)
        self.title(title)
        self.font = font
        self.input_text = None
        
        if icon_path and os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
                # Re-apply icon after a short delay to ensure it sticks
                self.after(200, lambda: self.iconbitmap(icon_path))
            except:
                pass
        
        self.transient(parent)
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        label = ctk.CTkLabel(self, text=prompt, font=self.font)
        label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
        
        self.entry = ctk.CTkEntry(self, font=self.font, width=250)
        self.entry.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda e: self.on_ok())
        
        ok_btn = ctk.CTkButton(self, text=ok_text, command=self.on_ok, font=self.font, width=100)
        ok_btn.grid(row=2, column=0, padx=10, pady=20)
        cancel_btn = ctk.CTkButton(self, text=cancel_text, command=self.on_cancel, font=self.font, fg_color="transparent", border_width=1, width=100)
        cancel_btn.grid(row=2, column=1, padx=10, pady=20)

        self.update_idletasks()
        req_width = self.winfo_reqwidth()
        req_height = self.winfo_reqheight()
        
        # Enforce minimum size and 16:9 ratio
        min_width = 360
        min_height = 203
        
        target_width = max(req_width, min_width)
        target_height = max(req_height, min_height)
        
        # Adjust for 16:9 ratio
        ratio = 16/9
        if target_width / target_height < ratio:
            target_width = int(target_height * ratio)
        elif target_width / target_height > ratio:
            target_height = int(target_width / ratio)
            
        width = target_width
        height = target_height

        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.wait_window()

    def on_ok(self):
        self.input_text = self.entry.get()
        self.destroy()

    def on_cancel(self):
        self.input_text = None
        self.destroy()

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
            
        self.icon_path = window_icon_path # Store for dialogs

        try:
            self.iconbitmap(window_icon_path)
        except Exception as e:
            print(f"Failed to set window icon: {e}")

        self.font_name = "GenYoGothic JP B"
        font_file = "GenYoGothic2JP-B.otf"
        font_path = os.path.join(base_path, font_file)
        self.load_custom_font(font_path)

        self.main_font = ctk.CTkFont(family=self.font_name, size=14)
        self.text_font = ctk.CTkFont(family=self.font_name, size=12)
        self.header_font = ctk.CTkFont(family=self.font_name, size=18, weight="bold")
        
        # Font tuple for tkinter widgets (Entry)
        self.font_tuple = (self.font_name, 12)

        self.registry_manager = RegistryManager(self.app_path, icon_path=registry_icon_path)

        self.selected_set_name = None
        self.current_folders = [] 
        self.original_folders = [] # To track changes
        self.folder_widgets = [] 
        self.set_buttons = []

        self._init_ui()
        
        # Global click binding to remove focus
        self.bind("<Button-1>", self.on_global_click)
        
        self._finish_init()

    def on_global_click(self, event):
        try:
            if event.widget.winfo_class() == "Entry":
                return
        except:
            pass
        self.focus()

    def _finish_init(self):
        self.bind("<Configure>", self.on_resize)
        self.refresh_sets_list()
        self.update_right_panel_state() 

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

        # --- Left Frame ---
        left_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_rowconfigure(2, weight=1) 
        left_frame.grid_columnconfigure(0, weight=1) 

        self.sets_label = ctk.CTkLabel(left_frame, text=self.t["folder_sets"], font=self.header_font)
        self.sets_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew") 
        
        self.add_btn = ctk.CTkButton(left_frame, text=self.t["add_set"], command=self.add_set, font=self.text_font)
        self.add_btn.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.sets_scroll_frame = ctk.CTkScrollableFrame(left_frame, label_text="")
        self.sets_scroll_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")
        
        btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.remove_btn = ctk.CTkButton(btn_frame, text=self.t["remove_set"], command=self.remove_set, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), font=self.text_font, state="disabled")
        self.remove_btn.pack(fill="x")

        settings_frame = ctk.CTkFrame(left_frame)
        settings_frame.grid(row=4, column=0, padx=10, pady=(0, 20), sticky="ew")
        
        ctk.CTkLabel(settings_frame, text=self.t["lang_label"], font=self.text_font).pack(anchor="w", padx=10, pady=(5,0))
        self.lang_var = ctk.StringVar(value=self.lang)
        self.lang_combo = ctk.CTkComboBox(settings_frame, values=["日本語", "English"], command=self.change_language, variable=self.lang_var, font=self.text_font, dropdown_font=self.text_font, state="readonly")
        self.lang_combo.pack(fill="x", padx=10, pady=5)
        
        if self.lang == "ja":
            self.lang_combo.set("日本語")
        else:
            self.lang_combo.set("English")

        self.remove_reg_btn = ctk.CTkButton(settings_frame, text=self.t["remove_menu"], command=self.remove_registry, fg_color="#FF5555", hover_color="#CC0000", font=self.text_font)
        self.remove_reg_btn.pack(fill="x", padx=10, pady=(5, 10))

        # --- Right Frame ---
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.right_frame.grid_rowconfigure(2, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.set_label = ctk.CTkLabel(self.right_frame, text=self.t["select_set_label"], font=self.header_font)
        self.set_label.grid(row=0, column=0, sticky="ew", pady=(0, 5)) 

        self.helper_label = ctk.CTkLabel(self.right_frame, text=self.t["input_helper"], font=self.text_font, text_color="gray", justify="left")
        self.helper_label.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        self.helper_label.bind('<Configure>', lambda e: self.helper_label.configure(wraplength=e.width))

        self.folders_scroll_frame = ctk.CTkScrollableFrame(self.right_frame, label_text="")
        self.folders_scroll_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        
        self.save_btn = ctk.CTkButton(self.right_frame, text=self.t["save_update"], command=self.save_and_update, font=self.main_font, height=40)
        self.save_btn.grid(row=3, column=0, sticky="ew")

        self.right_frame.bind("<Button-1>", lambda e: self.focus())
        self.folders_scroll_frame.bind("<Button-1>", lambda e: self.focus())
        try:
            self.folders_scroll_frame._parent_canvas.bind("<Button-1>", lambda e: self.focus())
        except:
            pass

    def change_language(self, choice):
        lang_code = "ja" if choice == "日本語" else "en"
        self.config_manager.set_language(lang_code)
        self.lang = lang_code
        self.t = TRANSLATIONS[self.lang]
        self.update_ui_text()
        
        self.update_idletasks()
        self.helper_label.configure(wraplength=self.helper_label.winfo_width())

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
        
        if self.selected_set_name:
            self.refresh_folder_list_ui()

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

        self.current_folders = self.config_manager.get_set_folders(set_name)
        self.original_folders = copy.deepcopy(self.current_folders) # Store original state
        self.refresh_folder_list_ui()
        
        self.remove_btn.configure(state="normal")
        self.update_right_panel_state()
        self.check_changes() # Initial check

    def update_right_panel_state(self):
        if self.selected_set_name:
            self.folders_scroll_frame.configure(fg_color=("gray85", "gray17")) 
            self.helper_label.configure(text_color="gray")
        else:
            self.folders_scroll_frame.configure(fg_color=("gray90", "gray13")) 
            self.save_btn.configure(state="disabled", fg_color="gray")
            self.helper_label.configure(text_color="gray")
            
            for widget in self.folders_scroll_frame.winfo_children():
                widget.destroy()

    def check_changes(self):
        if not self.selected_set_name:
            return
            
        # Get current state including pending input
        current_state = list(self.current_folders)
        
        # Check if last entry has text
        if self.folder_widgets:
            last_frame = self.folder_widgets[-1]
            for child in last_frame.winfo_children():
                if isinstance(child, ctk.CTkEntry):
                    text = child.get().strip()
                    if text and text != self.t["input_placeholder"]:
                        current_state.append(text)
                    break
        
        if current_state != self.original_folders:
            self.save_btn.configure(state="normal", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        else:
            self.save_btn.configure(state="disabled", fg_color="gray")

    def refresh_folder_list_ui(self):
        for widget in self.folders_scroll_frame.winfo_children():
            widget.destroy()
        
        self.folder_widgets = []

        for i, folder_name in enumerate(self.current_folders):
            self._create_folder_block(i, folder_name)

        self._create_folder_entry(len(self.current_folders))

    def _create_folder_block(self, index, text):
        frame = ctk.CTkFrame(self.folders_scroll_frame, fg_color="transparent")
        frame.pack(fill="x", pady=2)

        btn = ctk.CTkButton(frame, text=text, anchor="w", font=self.text_font,
                            fg_color=("gray80", "gray20"), 
                            text_color=("black", "white"),
                            hover_color=("gray70", "gray30"),
                            command=lambda i=index: self._switch_to_edit_mode(i))
        btn.pack(fill="x", padx=5)
        self.folder_widgets.append(frame)

    def _create_folder_entry(self, index, initial_text=""):
        frame = ctk.CTkFrame(self.folders_scroll_frame, fg_color="transparent")
        frame.pack(fill="x", pady=2)
        
        entry = ctk.CTkEntry(frame, font=self.text_font)
        entry.pack(fill="x", padx=5)
        
        placeholder = self.t["input_placeholder"]
        default_text_color = ("gray10", "#DCE4EE")
        placeholder_color = "gray"

        def on_focus_in(event):
            try:
                entry._entry.configure(font=self.font_tuple)
            except:
                pass
            
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.configure(text_color=default_text_color)

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(text_color=placeholder_color)
                # Do NOT reset font here for placeholder, as it might cause size jump
                # Only reset if it was previously changed for IME input
                # But since we only change it on FocusIn, and placeholder is static text,
                # we can leave it as is or ensure it uses the standard text_font
                pass
            
            # Trigger change check on focus out (to handle empty edits)
            self.after(100, self.check_changes)
        
        def on_key_release(event):
            self.check_changes()

        entry._entry.bind("<FocusIn>", on_focus_in, add="+")
        entry._entry.bind("<FocusOut>", on_focus_out, add="+")
        entry.bind("<KeyRelease>", on_key_release)
        
        if initial_text:
            entry.insert(0, initial_text)
            entry.configure(text_color=default_text_color)
            entry.focus_set()
        else:
            entry.insert(0, placeholder)
            entry.configure(text_color=placeholder_color)

        entry.bind("<Return>", lambda event, i=index, e=entry: self._on_entry_return(i, e))
        entry.bind("<FocusOut>", lambda event, i=index, e=entry: self._on_entry_focus_out(i, e))
            
        self.folder_widgets.append(frame)

    def _switch_to_edit_mode(self, index):
        self._rebuild_ui_and_focus(index)

    def _rebuild_ui_and_focus(self, focus_index):
        for widget in self.folders_scroll_frame.winfo_children():
            widget.destroy()
        self.folder_widgets = []

        for i, folder_name in enumerate(self.current_folders):
            if i == focus_index:
                self._create_folder_entry(i, folder_name)
            else:
                self._create_folder_block(i, folder_name)
        
        self._create_folder_entry(len(self.current_folders))

    def _on_entry_return(self, index, entry_widget):
        new_text = entry_widget.get().strip()
        if new_text == self.t["input_placeholder"]:
            new_text = ""
        
        if index < len(self.current_folders):
            if new_text:
                self.current_folders[index] = new_text
            else:
                self.current_folders.pop(index)
        else:
            if new_text:
                self.current_folders.append(new_text)
        
        self.refresh_folder_list_ui()
        self.check_changes()
        
        if self.folder_widgets:
            last_frame = self.folder_widgets[-1]
            for child in last_frame.winfo_children():
                if isinstance(child, ctk.CTkEntry):
                    child.focus_set()
                    break

    def _on_entry_focus_out(self, index, entry_widget):
        if index >= len(self.current_folders):
            return

        new_text = entry_widget.get().strip()
        if new_text == self.t["input_placeholder"]:
            new_text = ""
        
        if new_text:
            self.current_folders[index] = new_text
            
            frame = self.folder_widgets[index]
            for child in frame.winfo_children():
                child.destroy()
                
            btn = ctk.CTkButton(frame, text=new_text, anchor="w", font=self.text_font,
                                fg_color=("gray80", "gray20"), 
                                text_color=("black", "white"),
                                hover_color=("gray70", "gray30"),
                                command=lambda i=index: self._switch_to_edit_mode(i))
            btn.pack(fill="x", padx=5)
        else:
            self.current_folders.pop(index)
            self.refresh_folder_list_ui()
        
        self.check_changes()

    def show_info(self, title, message):
        CustomDialog(self, title, message, self.text_font, icon_path=self.icon_path, type="info", ok_text=self.t["btn_ok"])

    def show_error(self, title, message):
        CustomDialog(self, title, message, self.text_font, icon_path=self.icon_path, type="error", ok_text=self.t["btn_ok"])

    def show_confirm(self, title, message):
        dialog = CustomDialog(self, title, message, self.text_font, icon_path=self.icon_path, type="confirm", ok_text=self.t["btn_ok"], cancel_text=self.t["btn_cancel"])
        return dialog.result

    def show_input(self, title, prompt):
        dialog = CustomInputDialog(self, title, prompt, self.text_font, icon_path=self.icon_path, ok_text=self.t["btn_ok"], cancel_text=self.t["btn_cancel"])
        return dialog.input_text

    def add_set(self):
        name = self.show_input(self.t["new_set_title"], self.t["new_set_prompt"])
        if name:
            if name in self.config_manager.get_sets():
                self.show_error(self.t["error_title"], self.t["error_exists"])
                return
            self.config_manager.add_set(name, [])
            self.refresh_sets_list()
            self.select_set(name)

    def rename_set_dialog(self, old_name):
        new_name = self.show_input(self.t["rename_set_title"], self.t["rename_set_prompt"].format(old_name))
        if new_name and new_name != old_name:
            if new_name in self.config_manager.get_sets():
                self.show_error(self.t["error_title"], self.t["error_exists"])
                return
            
            self.config_manager.rename_set(old_name, new_name)
            self.refresh_sets_list()
            
            if self.selected_set_name == old_name:
                self.select_set(new_name)
            
            sets = self.config_manager.get_sets()
            self.registry_manager.register_context_menu(sets)

    def remove_set(self):
        if self.selected_set_name:
            if self.show_confirm(self.t["confirm_delete_title"], self.t["confirm_delete_msg"].format(self.selected_set_name)):
                self.config_manager.remove_set(self.selected_set_name)
                self.refresh_sets_list()
                
                self.selected_set_name = None
                self.current_folders = []
                self.set_label.configure(text=self.t["select_set_label"])
                self.remove_btn.configure(state="disabled")
                self.update_right_panel_state()
                
                sets = self.config_manager.get_sets()
                self.registry_manager.register_context_menu(sets)

    def save_and_update(self):
        if self.selected_set_name:
            if self.folder_widgets:
                last_frame = self.folder_widgets[-1]
                for child in last_frame.winfo_children():
                    if isinstance(child, ctk.CTkEntry):
                        text = child.get().strip()
                        if text and text != self.t["input_placeholder"]:
                            self.current_folders.append(text)
                            child.delete(0, "end") 
                        break
            
            self.config_manager.add_set(self.selected_set_name, self.current_folders)
            self.original_folders = copy.deepcopy(self.current_folders) # Update original state
            self.refresh_folder_list_ui() 
            self.check_changes() # Re-check to disable button
            
            sets = self.config_manager.get_sets()
            success, msg = self.registry_manager.register_context_menu(sets)
            
            if success:
                self.show_info(self.t["success_title"], self.t["success_save_msg"].format(self.selected_set_name))
            else:
                self.show_error(self.t["warning_title"], self.t["warning_save_fail"].format(msg))
        else:
            self.show_info("Info", self.t["info_select_first"])

    def remove_registry(self):
        if self.show_confirm(self.t["confirm_reset_title"], self.t["confirm_reset_msg"]):
            success, msg = self.registry_manager.unregister_context_menu()
            if success:
                try:
                    if os.path.exists(self.config_manager.config_file):
                        os.remove(self.config_manager.config_file)
                    
                    self.config_manager.config = {"sets": {}}
                    
                    self.refresh_sets_list()
                    self.selected_set_name = None
                    self.current_folders = []
                    self.set_label.configure(text=self.t["select_set_label"])
                    self.remove_btn.configure(state="disabled")
                    self.update_right_panel_state()
                    
                    self.show_info(self.t["success_title"], self.t["success_remove_menu"])
                except Exception as e:
                    self.show_error(self.t["error_title"], f"Settings reset failed: {e}")
            else:
                self.show_error(self.t["error_title"], msg)

if __name__ == "__main__":
    app = BatchFoldersGUI()
    app.mainloop()
