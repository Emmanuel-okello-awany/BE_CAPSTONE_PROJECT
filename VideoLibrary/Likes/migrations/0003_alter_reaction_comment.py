# Generated by Django 5.1.7 on 2025-04-04 01:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Comments", "0001_initial"),
        ("Likes", "0002_reaction_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reaction",
            name="comment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Comments.comment"
            ),
        ),
    ]
