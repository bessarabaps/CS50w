
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like"),
    path("newPost", views.newPost, name="newPost"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
