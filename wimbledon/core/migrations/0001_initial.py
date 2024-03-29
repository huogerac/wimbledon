# Generated by Django 4.1.7 on 2024-01-12 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Competitor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="Tournament",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(max_length=512)),
                ("done", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("game_number", models.IntegerField(blank=True, null=True)),
                ("level_number", models.IntegerField(blank=True, null=True)),
                ("game_extra", models.BooleanField(default=False)),
                ("auto_win", models.BooleanField(default=False)),
                (
                    "competitor1",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="competitor1",
                        to="core.competitor",
                    ),
                ),
                (
                    "competitor2",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="competitor2",
                        to="core.competitor",
                    ),
                ),
                (
                    "tournament",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="matches",
                        to="core.tournament",
                    ),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="winner",
                        to="core.competitor",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="competitor",
            name="tournament",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="competitors",
                to="core.tournament",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="competitor",
            unique_together={("tournament", "name")},
        ),
    ]
