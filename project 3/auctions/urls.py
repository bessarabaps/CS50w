from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("items/", include('item.urls')),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:category>", views.category_items, name="category_items"),

]

urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
