from bs4 import BeautifulSoup
import os
import requests
from requests.models import Response

from . import constants as const
from .media import image


def detail(movie: str):
    pagelink: str = f"{const.BASEURL}{const.SUBURL}/{movie}"
    mime: Response = requests.get(pagelink)
    soup: BeautifulSoup = BeautifulSoup(mime.content, const.PARSER)

    def getDescription():
        descriptors = soup.select(".extravote ~ p")
        result = ""
        for descriptor in descriptors:
            if descriptor.find("span"):
                break
            result += descriptor.get_text().strip() + "\n"
        return result.strip()

    component = {
        "description": getDescription(),
        "episodePermalink": lambda x: x.find(class_="cell4").find("a").get("href"),
        "episodes": lambda x: x.find_all(class_="footer"),
        "episodeSize": lambda x: x.find(class_="cell3").get_text().strip(),
        "episodeTitle": lambda x: x.find(class_="cell2").get_text().strip(),
        "genres": soup.find(class_="footer")
        .find(class_="cell1")
        .get_text()
        .split(" | "),
        "heroImage": image(
            soup.find(class_="imageseries1").find("img").get("src"),
            set(os.listdir(const.MEDIA)),
        ),
        "season": lambda x: x.get_text().strip(),
        "title": soup.find("h1", attrs={"class": "uk-badge1"}).get_text().strip(),
        "rating": soup.find("span", attrs={"class": "extravote-info"})
        .get_text()
        .strip()
        .split(" ")[1],
    }

    seasonEpisodes = [
        {
            "season": component["season"](seasonHead),
            "episodes": [
                {
                    "episodePermalink": component["episodePermalink"](episode),
                    "episodeSize": component["episodeSize"](episode),
                    "episodeTitle": component["episodeTitle"](episode),
                }
                for episode in component["episodes"](episodeHead)
            ],
        }
        for seasonHead, episodeHead in zip(
            soup.find_all(class_="uk-accordion-title"),
            soup.find_all(class_="uk-accordion-content"),
        )
    ]

    return {
        "description": component["description"],
        "genres": component["genres"],
        "heroImage": component["heroImage"],
        "rating": component["rating"],
        "seasonEpisodes": seasonEpisodes,
        "title": component["title"],
    }
