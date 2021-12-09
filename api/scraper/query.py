from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests
from requests.compat import quote_plus
from requests.models import Response
from typing import List

from . import constants as const
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
            "permalink": article.find("a").get("href"),
        }
        for article in articles
    ]


def filteredSearch(filter: str) -> List[Movie]:
    tail: str = (
        f"tv-series-started-in-{filter}"
        if type.isnumeric()
        else f"tv-series-{filter}-genre"
    )

    permalink: str = f"{const.BASEURL}{tail}"
    mime: Response = requests.get(permalink)
    soup: BeautifulSoup = BeautifulSoup(mime.content, const.PARSER)
    articles: ResultSet = soup.find_all("article")

    components = {
        "title": lambda x: x.find(class_="uk-article-titletag").get_text().strip(),
        "permalink": lambda x: x.find(class_="uk-article-titletage")
        .find("a")
        .get("href")
        .strip(),
        "image": lambda x: x.find("img").get("src").strip(),
    }

    return [
        {
            "title": components["title"](article),
            "permalink": components["permalink"](article),
            "imageSrc": components["image"](article),
        }
        for article in articles
    ]
