import sys
import json
import urllib.parse

import xbmcgui
import xbmcplugin
import xbmcvfs


class Router:


    def __init__(self):

        self.handle = int(sys.argv[1])

        self.base_url = sys.argv[0]

        self.params = dict(
            urllib.parse.parse_qsl(
                sys.argv[2][1:]
            )
        )



    def run(self, argv):


        action = self.params.get(
            "action"
        )


        if action == "section":

            self.open_section()


        elif action == "anilist":

            self.open_anilist()


        else:

            self.home()





    def load_collections(self):


        path = xbmcvfs.translatePath(
            "special://home/addons/plugin.video.kodicollections/resources/data/collections.json"
        )


        try:

            file = xbmcvfs.File(path)

            content = file.read()

            file.close()


            data = json.loads(content)


            if isinstance(data, dict):

                return data.get(
                    "sections",
                    []
                )


            if isinstance(data, list):

                return data


            return []



        except Exception as e:


            xbmcgui.Dialog().notification(
                "Kodi Collections",
                "JSON Error",
                xbmcgui.NOTIFICATION_ERROR,
                5000
            )


            return []







    def home(self):


        sections = self.load_collections()


        for section in sections:


            item = xbmcgui.ListItem(
                label=section.get(
                    "title",
                    "No Title"
                )
            )


            url = (
                self.base_url
                + "?action=section&id="
                + section.get(
                    "id",
                    ""
                )
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


        section_id = self.params.get(
            "id"
        )


        sections = self.load_collections()


        for section in sections:


            if section.get("id") == section_id:


                for entry in section.get(
                    "items",
                    []
                ):


                    item = xbmcgui.ListItem(
                        label=entry.get(
                            "title",
                            "No Title"
                        )
                    )



                    if entry.get("provider") == "anilist":


                        url = (
                            self.base_url
                            + "?action=anilist&type="
                            + entry.get(
                                "type",
                                "trending"
                            )
                        )


                    else:


                        url = entry.get(
                            "action",
                            ""
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






    def open_anilist(self):


        try:

            from resources.lib.providers import anilist


            anime_type = self.params.get(
                "type",
                "trending"
            )


            if anime_type == "popular":

                results = anilist.popular()


            elif anime_type == "top":

                results = anilist.top()


            else:

                results = anilist.trending()





            for anime in results:


                title = anime["title"]


                item = xbmcgui.ListItem(
                    label=title
                )


                item.setArt(
                    {
                        "poster": anime["poster"],
                        "thumb": anime["poster"]
                    }
                )


                url = (
                    "plugin://plugin.video.themoviedb.helper/"
                    "?info=search"
                    "&tmdb_type=tv"
                    "&query="
                    + urllib.parse.quote(
                        title
                    )
                )


                xbmcplugin.addDirectoryItem(
                    self.handle,
                    url,
                    item,
                    True
                )




        except Exception as e:


            xbmcgui.Dialog().notification(
                "AniList",
                "Connection Error",
                xbmcgui.NOTIFICATION_ERROR,
                5000
            )



        xbmcplugin.endOfDirectory(
            self.handle
        )