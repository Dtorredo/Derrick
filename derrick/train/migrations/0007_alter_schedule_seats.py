# Generated by Django 3.2.12 on 2024-11-21 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0006_schedule_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='seats',
            field=models.JSONField(default=dict, null=True),
        ),
    ]
