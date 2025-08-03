import settings
import actions

import os
import json
import shutil
import time

from pathlib import Path


class CreatePlugin:
    def __init__(self):
        self.folder_name = settings.PLUGIN_ID + ".sdPlugin"
        self.folder_path = self.get_folder_path()

        self.actions = []

    def get_folder_path(self):
        path = Path("./Plugin-Files") / self.folder_name
        return path

    def create_main_folder(self):
        if os.path.exists(self.folder_path):
            shutil.rmtree(self.folder_path)

        os.makedirs(self.folder_path)

    def create_manifest(self):
        mani_dict = {
            "Actions": self.actions,
            "SDKVersion": 2,
            "Author": settings.AUTHOR,
            "Name": settings.NAME,
            "Icon": "images/spotify.png",
            "CodePath": "plugin/main.bat",
            "Description": settings.DESCRIPTION,
            "Category": settings.CATEGORY,
            "CategoryIcon": "images/spotify.png",
            "Version": settings.VERSION,
            "URL": settings.URL,
            "OS": [
                {
                    "Platform": "windows",
                    "MinimumVersion": "7"
                }
            ],
            "Software": {
                "MinimumVersion": "2.9.172.0"
            }
        }

        with open(self.folder_path / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(mani_dict, f, ensure_ascii=False, indent=2)

    def create_action(self, action_name=None, action_dict_update=None):
        action_dict = {}
        if action_dict_update is not None:
            action_dict.update(action_dict_update)
        if action_name is not None:
            action_dict["UUID"] = settings.PLUGIN_ID + "." + action_name
        self.actions.append(action_dict)

    @staticmethod
    def add_action(action):
        plugin.create_action(action_dict_update={
            "Icon": action.IMAGE,
            "Name": action.NAME,
            "States": [{
                "Image": action.IMAGE,
            }],
            "Controllers": action.CONTROLLERS,
            "Tooltip": action.TOOLTIP,
            "UUID": action().UUID,
        })

    def copy_static(self):
        shutil.copytree('./static', self.folder_path, dirs_exist_ok=True)

    def copy_plugin_to_direct(self, path):
        if os.path.exists(Path(path) / self.folder_name):
            shutil.rmtree(Path(path) / self.folder_name)

        shutil.copytree(self.folder_path, Path(path) / self.folder_name)

    @staticmethod
    def restart_ajazz():
        process_name = "Stream Dock AJAZZ.exe"
        os.system(f"taskkill /f /im \"{process_name}\"")
        time.sleep(1)
        os.startfile(r"C:\Program Files (x86)\Stream Dock AJAZZ Global\Stream Dock AJAZZ.exe")

    def generate(self):
        self.create_main_folder()
        self.create_manifest()
        self.copy_static()


if __name__ == '__main__':
    plugin = CreatePlugin()

    for class_action in actions.BaseAction.__subclasses__():
        plugin.add_action(class_action)

    plugin.generate()

    plugin.copy_plugin_to_direct(r"C:\Users\Zebaro\AppData\Roaming\HotSpot\StreamDock\plugins")
    plugin.restart_ajazz()
