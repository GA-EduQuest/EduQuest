# Generated by Django 5.0.1 on 2024-02-08 04:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_alter_assignment_complete_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
