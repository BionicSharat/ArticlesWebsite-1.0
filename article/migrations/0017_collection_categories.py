# Generated by Django 4.1 on 2022-08-31 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0016_collection_articles_collection_participants_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="categories",
            field=models.ManyToManyField(to="article.categories"),
        ),
    ]
