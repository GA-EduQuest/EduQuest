# Generated by Django 5.0.1 on 2024-02-08 02:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_merge_20240207_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='complete_date',
            field=models.DateField(blank=True, null=True, verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='due_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='exam_date',
            field=models.DateField(default=datetime.date(2024, 2, 9), verbose_name='Date'),
        ),
    ]
