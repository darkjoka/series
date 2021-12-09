from os import name
from django.urls import path

from . import views

urlpatterns = [
    path("/", views.indexView, name="index"),
    path("search/?<str:searchTerm>", views.searchView, name="search"),
    path("trailers/", views.trailersView, name="trailers"),
]
