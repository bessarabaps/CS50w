from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    autor = models.ForeignKey(User, related_name='autor', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    bodyPost = models.CharField(max_length=150)
    likePost = models.ManyToManyField(User, blank=True, related_name="User_who_like")

    def __str__(self):
        return f"Post №{self.id}, {self.date.strftime('%d.%m.%Y %H:%M')} by {self.autor}"

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='user_who_is_following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='user_who_is_being_followed', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower} is following {self.followed}"
