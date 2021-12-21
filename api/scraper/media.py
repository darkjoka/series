import os
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests
from requests.models import Response
from typing import List, Set


from .stypes import Movie
from . import constants as const


def trailers() -> List[Movie]:
    mime: Response = requests.get(const.TRAILERS)
    soup: BeautifulSoup = BeautifulSoup(mime.content, const.PARSER)
    articles: ResultSet = soup.find_all(class_="jux-item")

    components = {
        "production": lambda x: x.get("class")[4] if len(x.get("class")) > 4 else "",
        "title": lambda x: x.find(class_="jux-title").get_text().strip(),
        "permalink": lambda x: x.find(class_="jux-title").find("a").get("href").strip(),
        "thumbnailSrc": lambda x: image(
            x.find("img").get("src").strip(), set(os.listdir(const.MEDIA))
        ),
        "videoSrc": lambda x: x.find("iframe").get("src").strip(),
    }

    return [
        {
            "title": components["title"](article),
            "permalink": components["permalink"](article),
            "thumbnailSrc": components["thumbnailSrc"](article),
            "videoSrc": components["videoSrc"](article),
            "production": components["production"](article),
        }
        for article in articles
    ]


def image(imageSrc: str, dir: Set[str]) -> str:
    image: str = imageSrc.split("/")[-1]

    if image in dir:
        return image

    mime: Response = requests.get(f"{const.BASEURL}/{imageSrc}")
    with open(f"{const.MEDIA}/{image}", "wb") as file:
        for chunk in mime.iter_content(100_000):
            file.write(chunk)
    return image
