# Generated by Django 4.1 on 2022-10-10 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_review"),
    ]

    operations = [
        migrations.AlterField(
            model_name="suits",
            name="sizes",
            field=models.CharField(blank=True, default="44-60", max_length=20),
        ),
    ]
