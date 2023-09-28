# from django.contrib.auth.models import User
from django.db import models

from auctions.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Item(models.Model):
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    price = models.FloatField()
    autor = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(User, blank=True, related_name="User_watchlist")
    bid_by = models.ForeignKey(User, related_name='bids', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comment', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='item_comment', on_delete=models.CASCADE)
    message = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.user} comment on {self.item}"
