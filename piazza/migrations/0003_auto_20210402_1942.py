# Generated by Django 3.0.2 on 2021-04-02 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piazza', '0002_auto_20210401_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interaction',
            name='comments',
            field=models.CharField(blank=True, max_length=600),
        ),
        migrations.DeleteModel(
            name='response',
        ),
    ]