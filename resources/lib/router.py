import xbmcaddon
import xbmcgui
import xbmcplugin

from resources.lib.json_loader import JsonLoader


class Router:

    def run(self, argv):

        handle = int(argv[1])

        addon = xbmcaddon.Addon()

        addon_path = addon.getAddonInfo("path")

        loader = JsonLoader(addon_path)

        data = loader.load()

        menus = data.get("menus", [])

        for menu in menus:

            item = xbmcgui.ListItem(label=menu["title"])

            xbmcplugin.addDirectoryItem(
                handle,
                "",
                item,
                True
            )

        xbmcplugin.endOfDirectory(handle)
