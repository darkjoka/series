from django.http import JsonResponse

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
