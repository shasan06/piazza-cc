# Generated by Django 3.0.2 on 2021-04-05 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piazza', '0004_auto_20210405_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.CharField(blank=True, max_length=240),
        ),
    ]
