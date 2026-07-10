import xbmcgui
import xbmcplugin


class Router:

    def run(self, argv):

        handle = int(argv[1])

        menus = [
            "🔥 Trending",
            "⭐ Popular",
            "🆕 New Releases",
            "📺 Streaming Services",
            "🎬 Collections",
            "🎭 Genres",
            "❤️ Trakt",
            "⚙ Settings"
        ]

        for menu in menus:
            item = xbmcgui.ListItem(label=menu)
            xbmcplugin.addDirectoryItem(
                handle,
                "",
                item,
                True
            )

        xbmcplugin.endOfDirectory(handle)
