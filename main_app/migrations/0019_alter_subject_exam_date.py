# Generated by Django 5.0.1 on 2024-02-09 01:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0018_alter_assignment_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='exam_date',
            field=models.DateField(default=datetime.date(2024, 2, 10), verbose_name='Date'),
        ),
    ]
