from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests
from requests.models import Response
from typing import List

from api.scraper.types import Movie


def genericSearch(searchTerm: str)->List[Movie]:
    # TODO: construct permalink
    permalink: str
    mime: Response  = requests.get(permalink)
    soup: BeautifulSoup = BeautifulSoup(mime.content, "html.parser")
    articles: ResultSet = soup.find_all('article')

    return [{"title": article.get_text().strip() ,"permalink": article.find('a').get('href')} for article in articles]


def filteredSearch(filterString: str)->List[Movie]:
    # TODO: construct permalink
    permalink: str
    mime: Response = requests.get(permalink)
    soup: BeautifulSoup = BeautifulSoup(mime.content, 'html.parser')
    articles: ResultSet = soup.find_all('article')
    
    components = {
        'title': lambda x: x.find(class_="uk-article-titletag").get_text().strip(),
        'permalink': lambda x: x.find(class_="uk-article-titletage").find('a').get('href').strip(),
        'image': lambda x: x.find('img').get('src').strip()
    }

    return [{"title": components['title'](article), "permalink": components['permalink'](article), 'imageSrc': components['image'](article)} for article in articles]