import sys
from urllib.parse import parse_qsl

import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.lib.json_loader import JsonLoader


class Router:

    def __init__(self):
        self.handle = int(sys.argv[1])
        self.params = dict(parse_qsl(sys.argv[2][1:]))

        addon = xbmcaddon.Addon()
        self.addon_path = addon.getAddonInfo("path")

    def run(self, argv):

        action = self.params.get("action")

        if action == "open":
            self.show_collection()
        else:
            self.show_home()

    def show_home(self):

        loader = JsonLoader(self.addon_path)

        data = loader.load()

        menus = data.get("menus", [])

        for menu in menus:

            url = (
                f"{sys.argv[0]}?"
                f"action=open&id={menu['id']}"
            )

            item = xbmcgui.ListItem(label=menu["title"])

            xbmcplugin.addDirectoryItem(
                self.handle,
                url,
                item,
                True
            )

        xbmcplugin.endOfDirectory(self.handle)

    def show_collection(self):

        collection = self.params.get("id")

        item = xbmcgui.ListItem(
            label=f"Selected: {collection}"
        )

        xbmcplugin.addDirectoryItem(
            self.handle,
            "",
            item,
            False
        )

        xbmcplugin.endOfDirectory(self.handle)
