# Generated by Django 5.0.1 on 2024-02-07 08:12

import main_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_profile_avatar_url_delete_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='exam_date',
            field=models.DateField(default=main_app.models.one_day_after, verbose_name='Date'),
        ),
    ]
