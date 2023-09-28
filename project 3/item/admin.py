from django.contrib import admin

# Register your models here.
from .models import Category, Item, Comment

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Comment)