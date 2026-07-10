import json
import urllib.request


URL = "https://graphql.anilist.co"



def request(extra):


    query = """
    query {
      Page(page: 1, perPage: 25) {
        media(
          type: ANIME,
          %s
        ) {

          title {
            romaji
            english
          }

          coverImage {
            large
          }

        }
      }
    }
    """ % extra



    payload = json.dumps(
        {
            "query": query
        }
    ).encode(
        "utf-8"
    )



    req = urllib.request.Request(
        URL,
        data=payload
    )


    req.add_header(
        "Content-Type",
        "application/json"
    )


    req.add_header(
        "User-Agent",
        "KodiCollections/1.0"
    )



    response = urllib.request.urlopen(
        req
    )


    data = json.loads(
        response.read().decode(
            "utf-8"
        )
    )



    results = []



    for anime in data["data"]["Page"]["media"]:


        title = (
            anime["title"]["english"]
            or anime["title"]["romaji"]
        )


        results.append(
            {
                "title": title,
                "poster": anime["coverImage"]["large"]
            }
        )



    return results





def trending():

    return request(
        "sort: [TRENDING_DESC]"
    )



def popular():

    return request(
        "sort: [POPULARITY_DESC]"
    )



def top():

    return request(
        "sort: [SCORE_DESC]"
    )



def movies():

    return request(
        """
        format: MOVIE,
        sort: [POPULARITY_DESC]
        """
    )



def season():

    return request(
        """
        season: SUMMER,
        seasonYear: 2026,
        sort: [POPULARITY_DESC]
        """
    )



def action():

    return request(
        """
        genre: "Action",
        sort: [POPULARITY_DESC]
        """
    )



def comedy():

    return request(
        """
        genre: "Comedy",
        sort: [POPULARITY_DESC]
        """
    )



def isekai():

    return request(
        """
        tag: "Isekai",
        sort: [POPULARITY_DESC]
        """
    )