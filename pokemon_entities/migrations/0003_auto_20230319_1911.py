# Generated by Django 3.1.14 on 2023-03-19 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0002_auto_20230319_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='disappeared_at',
            field=models.DateTimeField(null=True),
        ),
    ]