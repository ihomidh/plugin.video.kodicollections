import json
import os
import xbmcvfs


class JsonLoader:
    def __init__(self, addon_path):
        self.addon_path = addon_path

    def load(self, filename="collections.json"):
        path = os.path.join(
            self.addon_path,
            "resources",
            "data",
            filename
        )

        if not xbmcvfs.exists(path):
            return {}

        file = xbmcvfs.File(path)
        data = file.read()
        file.close()

        return json.loads(data)
