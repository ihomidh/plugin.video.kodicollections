import json
import urllib.request
import urllib.parse

import xbmcaddon



addon = xbmcaddon.Addon()



def get_api_key():

    return addon.getSetting(
        "tmdb_api"
    )






def find_tv(title, year=None):


    api_key = get_api_key()



    if not api_key:

        return None





    query = urllib.parse.quote(
        title
    )



    url = (
        "https://api.themoviedb.org/3/search/tv"
        "?api_key="
        + api_key
        + "&query="
        + query
    )



    if year:

        url += (
            "&first_air_date_year="
            + str(year)
        )




    req = urllib.request.Request(
        url
    )



    req.add_header(
        "User-Agent",
        "KodiCollections"
    )




    response = urllib.request.urlopen(
        req
    )



    data = json.loads(
        response.read().decode(
            "utf-8"
        )
    )




    results = data.get(
        "results",
        []
    )




    if not results:

        return None




    return results[0].get(
        "id"
    )