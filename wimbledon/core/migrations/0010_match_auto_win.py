# Generated by Django 4.1.7 on 2024-01-12 01:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_match_game_extra"),
    ]

    operations = [
        migrations.AddField(
            model_name="match",
            name="auto_win",
            field=models.BooleanField(default=False),
        ),
    ]