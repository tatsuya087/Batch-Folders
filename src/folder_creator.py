import os

class FolderCreator:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def create_folders(self, set_name, target_path):
        folders = self.config_manager.get_set_folders(set_name)
        if not folders:
            return False, f"Set '{set_name}' not found or empty."

        created_count = 0
        errors = []

        for folder_name in folders:
            clean_name = folder_name.strip()
            if not clean_name:
                continue
            
            full_path = os.path.join(target_path, clean_name)
            
            try:
                os.makedirs(full_path, exist_ok=True)
                created_count += 1
            except Exception as e:
                errors.append(f"Failed to create '{clean_name}': {e}")

        if errors:
            return False, "\n".join(errors)
        
        return True, f"Successfully created {created_count} folders in '{target_path}'."
