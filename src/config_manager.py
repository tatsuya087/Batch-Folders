import json
import os
import sys

CONFIG_FILE = "Batch Folders Config.json"

class ConfigManager:
    def __init__(self, config_path=None):
        if config_path:
            self.config_file = config_path
        else:
            user_home = os.path.expanduser('~')
            self.config_file = os.path.join(user_home, CONFIG_FILE)
        
        self.config = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_file):
            return {"sets": {}}
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {"sets": {}}

    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_sets(self):
        return self.config.get("sets", {})

    def get_set_folders(self, set_name):
        return self.config.get("sets", {}).get(set_name, [])

    def add_set(self, set_name, folders):
        if "sets" not in self.config:
            self.config["sets"] = {}
        self.config["sets"][set_name] = folders
        self.save_config()

    def remove_set(self, set_name):
        if "sets" in self.config and set_name in self.config["sets"]:
            del self.config["sets"][set_name]
            self.save_config()

    def rename_set(self, old_name, new_name):
        if "sets" in self.config and old_name in self.config["sets"]:
            self.config["sets"][new_name] = self.config["sets"].pop(old_name)
            self.save_config()

    def get_language(self):
        return self.config.get("language", "en")

    def set_language(self, lang_code):
        self.config["language"] = lang_code
        self.save_config()

    def get_window_geometry(self):
        return self.config.get("window_geometry", "720x620")

    def set_window_geometry(self, geometry):
        self.config["window_geometry"] = geometry
        self.save_config()
