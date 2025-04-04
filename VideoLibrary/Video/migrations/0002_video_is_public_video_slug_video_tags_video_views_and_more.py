# Generated by Django 5.1.7 on 2025-03-25 21:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Video", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="is_public",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="video",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name="video",
            name="tags",
            field=models.CharField(
                blank=True, help_text="Comma-separated tags", max_length=255
            ),
        ),
        migrations.AddField(
            model_name="video",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="video",
            name="category",
            field=models.CharField(
                choices=[
                    ("Music", "Music"),
                    ("Sports", "Sports"),
                    ("Education", "Education"),
                    ("Movies", "Movies"),
                    ("Gaming", "Gaming"),
                    ("Technology", "Technology"),
                ],
                default="Education",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                default="thumbnails/default-thumbnail.jpg",
                null=True,
                upload_to="thumbnails/",
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="title",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="video",
            name="uploaded_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="videos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
