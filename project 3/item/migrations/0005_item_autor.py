# Generated by Django 4.1.7 on 2023-06-27 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0004_rename_discription_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='autor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]