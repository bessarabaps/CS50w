from django.urls import path

from . import views


app_name = 'item'

urlpatterns = [
    path("add/", views.add, name="add"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/add_Watchlist/", views.add_Watchlist, name="add_Watchlist"),
    path("<int:pk>/remove_Watchlist/", views.remove_Watchlist, name="remove_Watchlist"),
    path("<int:pk>/add_bid/", views.add_bid, name="add_bid"),
    path("<int:pk>/close_item/", views.close_item, name="close_item"),
    path("<int:pk>/add_comment/", views.add_comment, name="add_comment")
    ]