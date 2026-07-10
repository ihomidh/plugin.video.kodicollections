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


        f = xbmcvfs.File(path)

        data = json.loads(
            f.read()
        )

        f.close()


        return data.get(
            "sections",
            []
        )








    def home(self):

        for section in self.load_collections():


            item = xbmcgui.ListItem(
                label=section["title"]
            )


            url = (
                self.base_url
                + "?action=section&id="
                + section["id"]
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


        for section in self.load_collections():


            if section["id"] == section_id:


                for entry in section["items"]:


                    item = xbmcgui.ListItem(
                        label=entry["title"]
                    )


                    if entry.get("provider") == "anilist":


                        url = (
                            self.base_url
                            + "?action=anilist&type="
                            + entry["type"]
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

        from resources.lib.providers import anilist


        xbmcplugin.setContent(
            self.handle,
            "tvshows"
        )


        anime_type = self.params.get(
            "type"
        )



        if anime_type == "search":


            text = xbmcgui.Dialog().input(
                "Search Anime"
            )


            if not text:


                xbmcplugin.endOfDirectory(
                    self.handle
                )

                return


            results = anilist.search(
                text
            )




        elif anime_type == "popular":

            results = anilist.popular()


        elif anime_type == "top":

            results = anilist.top()


        elif anime_type == "movies":

            results = anilist.movies()


        elif anime_type == "season":

            results = anilist.season()


        elif anime_type == "action":

            results = anilist.action()


        elif anime_type == "comedy":

            results = anilist.comedy()


        elif anime_type == "isekai":

            results = anilist.isekai()


        else:

            results = anilist.trending()








        for anime in results:


            title = anime["title"]


            item = xbmcgui.ListItem(
                label=title
            )



            item.setArt(
                {

                    "poster":
                    anime.get(
                        "poster",
                        ""
                    ),

                    "thumb":
                    anime.get(
                        "poster",
                        ""
                    ),

                    "fanart":
                    anime.get(
                        "fanart",
                        ""
                    )

                }
            )





            rating = 0


            if anime.get(
                "score"
            ):


                rating = (
                    anime["score"]
                    /
                    10
                )





            item.setInfo(
                "video",
                {

                    "title":
                    title,

                    "plot":
                    anime.get(
                        "plot",
                        ""
                    ),

                    "year":
                    anime.get(
                        "year",
                        0
                    ),

                    "rating":
                    rating,

                    "genre":
                    ", ".join(
                        anime.get(
                            "genres",
                            []
                        )
                    )

                }
            )






            search = urllib.parse.quote(
                anime.get(
                    "original_title",
                    title
                )
            )



            url = (
                "plugin://plugin.video.themoviedb.helper/"
                "?info=search"
                "&tmdb_type=tv"
                "&query="
                + search
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