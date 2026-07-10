import json
import urllib.request


URL = "https://graphql.anilist.co"


def request(sort):

    query = """
    query {
      Page(page: 1, perPage: 25) {
        media(
          type: ANIME,
          sort: [%s]
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
    """ % sort


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
        "TRENDING_DESC"
    )



def popular():

    return request(
        "POPULARITY_DESC"
    )



def top():

    return request(
        "SCORE_DESC"
    )