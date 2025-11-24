import winreg
import sys
import os

class RegistryManager:
    def __init__(self, app_path, icon_path=None):
        self.app_path = app_path
        self.icon_path = icon_path if icon_path else app_path.replace('"', '')
        self.key_path = r"Software\Classes\Directory\Background\shell\BatchFolders"

    def register_context_menu(self, sets):
        """
        Registers the application to the context menu.
        Creates a cascading menu with items for each set.
        """
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.key_path)
            winreg.SetValueEx(key, "MUIVerb", 0, winreg.REG_SZ, "Batch Folders")
            winreg.SetValueEx(key, "SubCommands", 0, winreg.REG_SZ, "")
            
            icon_to_use = self.icon_path
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_to_use) 
            winreg.CloseKey(key)

            shell_key_path = self.key_path + r"\shell"
            
            try:
                self._delete_key_recursive(winreg.HKEY_CURRENT_USER, shell_key_path)
            except:
                pass

            shell_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, shell_key_path)
            winreg.CloseKey(shell_key)

            for set_name in sets:
                self._add_set_command(set_name)
            
            return True, "Context menu registered successfully."
        except Exception as e:
            return False, f"Error registering context menu: {e}"

    def _add_set_command(self, set_name):
        safe_name = "".join(c for c in set_name if c.isalnum() or c in (' ', '_', '-'))
        
        set_key_path = self.key_path + r"\shell\\" + safe_name
        
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, set_key_path)
            winreg.SetValueEx(key, "MUIVerb", 0, winreg.REG_SZ, set_name)
            winreg.CloseKey(key)

            command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, set_key_path + r"\command")
            
            if self.app_path.strip().startswith('"'):
                cmd_prefix = self.app_path
            else:
                cmd_prefix = f'"{self.app_path}"'

            cmd_str = f'{cmd_prefix} create "{set_name}" "%V"'
            winreg.SetValue(command_key, "", winreg.REG_SZ, cmd_str)
            winreg.CloseKey(command_key)
        except Exception as e:
            print(f"Failed to add set {set_name}: {e}")

    def unregister_context_menu(self):
        """Removes the registry keys."""
        try:
            self._delete_key_recursive(winreg.HKEY_CURRENT_USER, self.key_path)
            return True, "Context menu removed."
        except FileNotFoundError:
            return True, "Context menu was not present."
        except Exception as e:
            return False, f"Error removing context menu: {e}"

    def _delete_key_recursive(self, root, subkey):
        try:
            open_key = winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS)
            info = winreg.QueryInfoKey(open_key)
            
            for _ in range(info[0]):
                child = winreg.EnumKey(open_key, 0)
                self._delete_key_recursive(open_key, child)
            
            winreg.CloseKey(open_key)
            winreg.DeleteKey(root, subkey)
        except Exception as e:
            pass
