from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests
from requests.models import Response
from typing import List, Set


from stypes import Movie
import constants as const


def trailers() -> List[Movie]:
    mime: Response = requests.get(const.TRAILERS)
    soup: BeautifulSoup = BeautifulSoup(mime.content, const.PARSER)
    articles: ResultSet = soup.find_all(class_="jux-item")

    components = {
        "production": lambda x: x.get("class")[4] if len(x.get("class")) > 4 else "",
        "title": lambda x: x.find(class_="jux-title").get_text().strip(),
        "permalink": lambda x: x.find(class_="jux-title").find("a").get("href").strip(),
        "thumbnailSrc": lambda x: x.find("img").get("src").strip(),
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


def image(img: str, dir: Set[str]) -> str:
    img: str = img.split("/")[-1]

    for img in dir:
        return f"{const.MEDIA}/{img}"

    mime: Response = requests.get(f"{const.BASEURL}/{img}")
    with open(f"{const.MEDIA}/{img}", "wb") as file:
        for chunk in mime.iter_content(100_000):
            file.write(chunk)
    return f"{const.MEDIA}/{img}"
