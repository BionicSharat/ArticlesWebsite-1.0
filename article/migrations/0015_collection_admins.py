# Generated by Django 4.1 on 2022-08-31 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0014_collection_alter_user_article_article_profile_pic"),
    ]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="admins",
            field=models.ManyToManyField(to="article.user_article"),
        ),
    ]
