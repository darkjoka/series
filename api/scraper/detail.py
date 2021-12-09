from bs4 import BeautifulSoup
import requests
from requests.models import Response

import api.scraper.constants as const


def detail(pagelink: str):
    mime: Response = requests.get(pagelink)
    soup: BeautifulSoup = BeautifulSoup(mime.content, const.PARSER)

    component = {
        "description": soup.find("meta", attrs={"property": "og:description"}).get(
            "content"
        ),
        "episodePermalink": lambda x: x.find(class_="cell4").find("a").get("href"),
        "episodes": lambda x: x.find_all(class_="footer"),
        "episodeSize": lambda x: x.find(class_="cell3").get_text().strip(),
        "episodeTitle": lambda x: x.find(class_="cell2").get_text().strip(),
        "genres": soup.find(class_="footer")
        .find(class_="cell1")
        .get_text()
        .split(" | "),
        "heroImage": soup.find(class_="imageseries1").find("img").get("src"),
        "season": lambda x: x.get_text().strip(),
        "title": soup.find("h1", attrs={"class": "uk-badge1"}).get_text().strip(),
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
        "seasonEpisodes": seasonEpisodes,
        "title": component["title"],
    }
