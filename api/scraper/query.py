from bs4 import BeautifulSoup
from bs4.element import ResultSet
import os
import requests
from requests.compat import quote_plus
from requests.models import Response
from typing import List

from . import constants as const
from .media import image
from .stypes import Movie


def genericSearch(searchTerm: str) -> List[Movie]:
    tail: str = (
        f"search-series?searchword={quote_plus(searchTerm)}&searchphrase=all&limit=0"
    )
    permalink: str = f"{const.BASEURL}{tail}"
    mime: Response = requests.get(permalink)
    soup: BeautifulSoup = BeautifulSoup(mime.content, const.PARSER)
    articles: ResultSet = soup.find_all("article")

    return [
        {
            "title": article.get_text().strip(),
            "permalink": article.find("a").get("href").split("/")[-1],
        }
        for article in articles
    ]


def filteredSearch(filter: str) -> List[Movie]:
    tail: str = (
        f"tv-series-started-in-{filter}"
        if filter.isnumeric()
        else f"tv-series-{filter}-genre"
    )

    permalink: str = f"{const.BASEURL}{tail}"
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
    }

    return [
        {
            "title": components["title"](article),
            "permalink": components["permalink"](article),
            "imageSrc": components["image"](article),
        }
        for article in articles
    ]
