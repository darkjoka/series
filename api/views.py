from django.http import JsonResponse

from scraper.index import index


def indexView(request):
    result = index()
    return JsonResponse({"data": result})
