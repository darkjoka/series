from django.http import JsonResponse, HttpResponse


from scraper.constants import MEDIA
from scraper.index import index
from scraper.media import trailers
from scraper.query import genericSearch, filteredSearch


def indexView(_) -> JsonResponse:
    result = index()
    return JsonResponse({"data": result})


def searchView(_, searchTerm) -> JsonResponse:
    result = genericSearch(searchTerm)
    return JsonResponse({"data": result})


def filterView(_, filter) -> JsonResponse:
    result = filteredSearch(filter)
    return JsonResponse({"data": result})


def trailersView(_) -> JsonResponse:
    result = trailers()
    return JsonResponse({"data": result})


def imageView(_, image) -> HttpResponse:
    extension: str = image.split(".")[-1]

    with open(f"./{MEDIA}/{image}", "rb") as file:
        return HttpResponse(file, content_type=f"image/{extension}")
