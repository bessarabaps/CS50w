# Generated by Django 4.2.4 on 2023-08-19 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0008_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='bid_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]