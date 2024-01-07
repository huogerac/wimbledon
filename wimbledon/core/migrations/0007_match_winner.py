# Generated by Django 4.1.7 on 2024-01-07 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_alter_competitor_tournament_alter_match_tournament"),
    ]

    operations = [
        migrations.AddField(
            model_name="match",
            name="winner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="winner",
                to="core.competitor",
            ),
        ),
    ]