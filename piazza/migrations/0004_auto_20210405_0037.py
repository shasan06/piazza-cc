# Generated by Django 3.0.2 on 2021-04-05 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piazza', '0003_auto_20210402_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interaction',
            name='comments',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
