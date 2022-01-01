from django.http import JsonResponse, HttpResponse


from .scraper.constants import MEDIA
from .scraper.detail import detail
from .scraper.index import index
from .scraper.media import trailers
from .scraper.query import genericSearch, filteredSearch


def indexView(_, cursor: int) -> JsonResponse:
    result = index(cursor)
    return JsonResponse({"data": result})


def searchView(_, searchTerm) -> JsonResponse:
    result = genericSearch(searchTerm)
    return JsonResponse({"data": result})


def filterView(_, filter, cursor: int) -> JsonResponse:
    result = filteredSearch(filter, cursor)
    return JsonResponse({"data": result})


def trailersView(_) -> JsonResponse:
    result = trailers()
    return JsonResponse({"data": result})


def imageView(_, image) -> HttpResponse:
    extension: str = image.split(".")[-1]

    with open(f"./{MEDIA}/{image}", "rb") as file:
        return HttpResponse(file, content_type=f"image/{extension}")


def detailView(_, movie) -> JsonResponse:
    result = detail(movie)
    return JsonResponse({"data": result})
