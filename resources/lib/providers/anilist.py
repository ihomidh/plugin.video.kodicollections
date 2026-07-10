import json
import urllib.request


ANILIST_URL = "https://graphql.anilist.co"


def request_anilist(query):

    data = json.dumps({
        "query": query
    }).encode("utf-8")

    req = urllib.request.Request(
        ANILIST_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        }
    )

    response = urllib.request.urlopen(req)

    return json.loads(
        response.read().decode("utf-8")
    )


def get_trending():

    query = """
    {
      Page(page:1, perPage:25) {
        media(
          type:ANIME,
          sort:TRENDING_DESC
        ) {
          id
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
    """

    result = request_anilist(query)

    return parse(result)



def get_popular():

    query = """
    {
      Page(page:1, perPage:25) {
        media(
          type:ANIME,
          sort:POPULARITY_DESC
        ) {
          id
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
    """

    result = request_anilist(query)

    return parse(result)



def get_top():

    query = """
    {
      Page(page:1, perPage:25) {
        media(
          type:ANIME,
          sort:SCORE_DESC
        ) {
          id
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
    """

    result = request_anilist(query)

    return parse(result)



def parse(result):

    shows = []

    items = result["data"]["Page"]["media"]

    for anime in items:

        title = (
            anime["title"]["english"]
            or anime["title"]["romaji"]
        )

        shows.append(
            {
                "title": title,
                "poster": anime["coverImage"]["large"],

                # هنا الربط مع TMDb Helper للتشغيل + Trakt
                "action":
                "plugin://plugin.video.themoviedb.helper/?info=search&tmdb_type=tv&query="
                + title
            }
        )

    return shows