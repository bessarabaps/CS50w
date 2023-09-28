from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    default_auto_field = 'django.db.models.AutoField'
