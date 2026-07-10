import sys
from urllib.parse import parse_qsl

import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.lib.json_loader import JsonLoader


class Router:

    def __init__(self):

        self.handle = int(sys.argv[1])

        self.params = dict(
            parse_qsl(sys.argv[2][1:])
        )

        addon = xbmcaddon.Addon()

        self.path = addon.getAddonInfo("path")


    def run(self, argv):

        action = self.params.get("action")

        if action == "section":
            self.open_section()

        else:
            self.home()


    def home(self):

        data = JsonLoader(
            self.path
        ).load()

        for section in data["sections"]:

            url = (
                sys.argv[0]
                + "?action=section&id="
                + section["id"]
            )

            item = xbmcgui.ListItem(
                label=section["title"]
            )

            art = (
                self.path
                + "/resources/media/"
                + section["image"]
            )

            item.setArt(
                {
                    "thumb": art,
                    "icon": art,
                    "poster": art,
                    "fanart": art
                }
            )

            xbmcplugin.addDirectoryItem(
                self.handle,
                url,
                item,
                True
            )

        xbmcplugin.endOfDirectory(
            self.handle
        )


    def open_section(self):

        section_id = self.params.get("id")

        data = JsonLoader(
            self.path
        ).load()

        for section in data["sections"]:

            if section["id"] == section_id:

                for entry in section["items"]:

                    item = xbmcgui.ListItem(
                        label=entry["title"]
                    )

                    item.setInfo(
                        "video",
                        {
                            "title": entry["title"],
                            "plot": entry.get("plot", "")
                        }
                    )

                    url = entry["action"]

                    xbmcplugin.addDirectoryItem(
                        self.handle,
                        url,
                        item,
                        True
                    )

        xbmcplugin.endOfDirectory(
            self.handle
        )