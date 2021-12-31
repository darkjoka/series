from bs4 import BeautifulSoup
from bs4.element import ResultSet
import os
import pickle
import requests
from requests.compat import quote_plus
from requests.models import Response
from typing import List

from . import constants as const
from .media import image
from .stypes import Movie
from .detail import detail


def genericSearch(searchTerm: str, cursor: int) -> List[Movie]:
    tail: str = (
        f"search-series?searchword={quote_plus(searchTerm)}&searchphrase=all&limit=5"
    )
    navExtension = f"&?start={cursor}" if cursor else ""
    permalink: str = f"{const.BASEURL}{tail}{navExtension}"
    mime: Response = requests.get(permalink)
    soup: BeautifulSoup = BeautifulSoup(mime.content, const.PARSER)
    articles: ResultSet = soup.find_all("article")

    data = [
        {
            "title": article.get_text().strip(),
            "permalink": article.find("a").get("href").split("/")[-1],
        }
        for article in articles
    ]

    result = queryInfoSeek(const.QUERY_CACHE, data)
    result["length"]


def filteredSearch(filter: str, cursor: int) -> List[Movie]:
    tail: str = (
        f"tv-series-started-in-{filter}"
        if filter.isnumeric()
        else f"tv-series-{filter}-genre"
    )
    navExtension = f"?start={cursor}" if cursor else ""

    permalink: str = f"{const.BASEURL}{tail}{navExtension}"
    mime: Response = requests.get(permalink)
    soup: BeautifulSoup = BeautifulSoup(mime.content, const.PARSER)
    articles: ResultSet = soup.find_all("article")

    components = {
        "title": lambda x: x.find(class_="uk-article-titletag").get_text().strip(),
        "permalink": lambda x: x.find(class_="uk-article-titletag")
        .find("a")
        .get("href")
        .strip()
        .split("/")[-1],
        "image": lambda x: image(
            x.find("img").get("src").strip(), set(os.listdir(const.MEDIA))
        ),
        "length": soup.find(class_="uk-badge-notification").get_text().strip(),
    }

    data = [
        {
            "title": components["title"](article),
            "permalink": components["permalink"](article),
            "imageSrc": components["image"](article),
        }
        for article in articles
    ]

    return {
        "length": components["length"],
        data: queryInfoSeek(const.QUERY_CACHE, data),
    }


def queryInfoSeek(store, data):
    result = []
    cached_data = {}

    if not os.path.isfile(store):
        with open(store, "wb") as file:
            pickle.dump(dict(), file)

    with open(store, "rb") as file:
        cached_data = pickle.load(file)
        for info in data[:6]:

            if info["title"] in cached_data:
                result.append(cached_data[info["title"]])
            else:
                detailData = detail(info["permalink"])
                requiredData = {key: info[key] for key in info.keys()}
                requiredData["heroImage"] = detailData["heroImage"]
                description = " ".join(detailData["description"].split("\n"))
                requiredData["description"] = description[:150]
                requiredData["rating"] = detailData["rating"]

                result.append(requiredData)
                cached_data[info["title"]] = requiredData

    with open(store, "wb") as file:
        pickle.dump(cached_data, file)

    return result
