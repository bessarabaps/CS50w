from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("random", views.random_page, name="random"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("<str:name>", views.articles, name="articles")
]
