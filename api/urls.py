from django.urls import path

from . import views

urlpatterns = [
    path("", views.indexView, name="index"),
    path("detail/<str:movie>", views.detailView, name="detail"),
    path("filter/<str:filter>", views.filterView, name="filter"),
    path("image/<str:image>", views.imageView, name="image"),
    path("search/<str:searchTerm>", views.searchView, name="search"),
    path("trailers/", views.trailersView, name="trailers"),
]
