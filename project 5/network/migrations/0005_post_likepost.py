# Generated by Django 4.2.5 on 2023-09-14 13:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likePost',
            field=models.ManyToManyField(blank=True, related_name='User_who_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
