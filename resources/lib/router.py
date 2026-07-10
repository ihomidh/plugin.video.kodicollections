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


        else:

            self.home()



    def load_collections(self):


        path = xbmcvfs.translatePath(
            "special://home/addons/plugin.video.kodicollections/resources/data/collections.json"
        )


        try:

            file = xbmcvfs.File(
                path
            )

            content = file.read()

            file.close()


            data = json.loads(
                content
            )


            if isinstance(
                data,
                dict
            ):

                return data.get(
                    "sections",
                    []
                )


            if isinstance(
                data,
                list
            ):

                return data


            return []


        except Exception as error:


            xbmcgui.Dialog().notification(
                "Kodi Collections",
                str(error),
                xbmcgui.NOTIFICATION_ERROR,
                5000
            )


            return []




    def home(self):


        sections = self.load_collections()


        for section in sections:


            title = section.get(
                "title",
                "No Title"
            )


            url = (
                self.base_url
                + "?action=section&id="
                + section.get(
                    "id",
                    ""
                )
            )


            item = xbmcgui.ListItem(
                label=title
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


                    title = entry.get(
                        "title",
                        "No Title"
                    )


                    url = entry.get(
                        "action",
                        ""
                    )


                    item = xbmcgui.ListItem(
                        label=title
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