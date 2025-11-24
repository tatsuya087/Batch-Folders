import unittest
import os
import shutil
import json
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from config_manager import ConfigManager
from folder_creator import FolderCreator

class TestBatchFolders(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_env"
        os.makedirs(self.test_dir, exist_ok=True)
        self.config_path = os.path.join(self.test_dir, "test_config.json")
        self.config_mgr = ConfigManager(self.config_path)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_config_ops(self):
        self.config_mgr.add_set("Set1", ["A", "B"])
        sets = self.config_mgr.get_sets()
        self.assertIn("Set1", sets)
        self.assertEqual(self.config_mgr.get_set_folders("Set1"), ["A", "B"])

        self.config_mgr.remove_set("Set1")
        self.assertNotIn("Set1", self.config_mgr.get_sets())

    def test_folder_creation(self):
        self.config_mgr.add_set("Set1", ["FolderA", "FolderB"])
        creator = FolderCreator(self.config_mgr)
        
        target_path = os.path.join(self.test_dir, "Target")
        os.makedirs(target_path, exist_ok=True)

        success, msg = creator.create_folders("Set1", target_path)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(target_path, "FolderA")))
        self.assertTrue(os.path.exists(os.path.join(target_path, "FolderB")))

if __name__ == '__main__':
    unittest.main()
