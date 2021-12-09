from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests
from requests.models import Response
from typing import List, Set


from api.scraper.types import Movie
import api.scraper.constants as const


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
