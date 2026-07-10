import json
import urllib.request
import urllib.parse


API_KEY = "5b91cf02dcacac6e4301fac5021b128b"



def find_tv(title, year=None):


    query = urllib.parse.quote(
        title
    )


    url = (
        "https://api.themoviedb.org/3/search/tv"
        "?api_key="
        + API_KEY
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



    return results[0]["id"]