# Generated by Django 3.2.12 on 2024-12-10 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0010_alter_booking_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
