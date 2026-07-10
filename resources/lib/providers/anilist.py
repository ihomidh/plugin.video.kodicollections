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
            extraLarge
            large
          }

          bannerImage

          description(
            asHtml:false
          )

          averageScore

          episodes

          seasonYear

          genres
        }
      }
    }
    """ % extra



    payload = json.dumps(
        {
            "query": query
        }
    ).encode("utf-8")



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
        "KodiCollections"
    )



    response = urllib.request.urlopen(req)


    data = json.loads(
        response.read().decode(
            "utf-8"
        )
    )



    results = []



    for anime in data["data"]["Page"]["media"]:


        title = (
            anime["title"]["english"]
            or
            anime["title"]["romaji"]
        )


        poster = (
            anime["coverImage"]["extraLarge"]
            or
            anime["coverImage"]["large"]
        )


        results.append(
            {

                "title":
                title,


                "original_title":
                anime["title"]["romaji"],


                "poster":
                poster,


                "fanart":
                anime.get(
                    "bannerImage"
                ),


                "plot":
                anime.get(
                    "description"
                ),


                "score":
                anime.get(
                    "averageScore"
                ),


                "episodes":
                anime.get(
                    "episodes"
                ),


                "year":
                anime.get(
                    "seasonYear"
                ),


                "genres":
                anime.get(
                    "genres",
                    []
                )

            }
        )


    return results






def trending():

    return request(
        "sort:[TRENDING_DESC]"
    )



def popular():

    return request(
        "sort:[POPULARITY_DESC]"
    )



def top():

    return request(
        "sort:[SCORE_DESC]"
    )



def movies():

    return request(
        """
        format:MOVIE,
        sort:[POPULARITY_DESC]
        """
    )



def season():

    return request(
        """
        sort:[TRENDING_DESC]
        """
    )



def action():

    return request(
        """
        genre:"Action",
        sort:[POPULARITY_DESC]
        """
    )



def comedy():

    return request(
        """
        genre:"Comedy",
        sort:[POPULARITY_DESC]
        """
    )



def isekai():

    return request(
        """
        tag:"Isekai",
        sort:[POPULARITY_DESC]
        """
    )




def search(text):


    text = text.replace(
        '"',
        ''
    )


    return request(
        '''
        search:"%s",
        sort:[POPULARITY_DESC]
        '''
        %
        text
    )