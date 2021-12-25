from bs4 import BeautifulSoup
from bs4.element import ResultSet
import os
import requests
from requests.models import Response

from . import constants as const
from .media import image


def index(cursor: int):
    navExtension = f"?start={cursor}" if cursor else ""
    mime: Response = requests.get(f"{const.BASEURL}{const.SUBURL}{navExtension}")
    soup: BeautifulSoup = BeautifulSoup(mime.content, const.PARSER)
    articles: ResultSet = soup.find_all(class_="uk-article")

    component = {
        "imageSrc": lambda x: image(
            x.find("img").get("src"), set(os.listdir(const.MEDIA))
        ),
        "lastEpisode": lambda x: x.find("time").get("datetime"),
        "permalink": lambda x: x.get("data-permalink").split("/")[-1],
        "rating": lambda x: x.find(class_="current-rating").get_text().strip(),
        "teaser": lambda x: x.find(class_="teasershort").get_text().strip(),
        "title": lambda x: x.find(class_="uk-article-title1").get_text().strip(),
    }

    return [
        {
            "imageSrc": component["imageSrc"](article),
            "lastEpisode": component["lastEpisode"](article),
            "permalink": component["permalink"](article),
            "rating": component["rating"](article),
            "teaser": component["teaser"](article),
            "title": component["title"](article),
        }
        for article in articles
    ]
