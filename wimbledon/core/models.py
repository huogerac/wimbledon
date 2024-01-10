from django.db import models


class Tournament(models.Model):
    description = models.CharField(max_length=512)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "description": self.description,
            "done": self.done,
        }


class Competitor(models.Model):
    name = models.CharField(max_length=128)
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="competitors"
    )

    class Meta:
        unique_together = [["tournament", "name"]]

    def __str__(self):
        return f"{self.name}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "tournament_id": self.tournament_id,
            "name": self.name,
        }


class Match(models.Model):
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="matches"
    )
    game_number = models.IntegerField(blank=True, null=True)
    level_number = models.IntegerField(blank=True, null=True)
    competitor1 = models.ForeignKey(
        Competitor,
        models.SET_NULL,
        related_name="competitor1",
        blank=True,
        null=True,
    )
    competitor2 = models.ForeignKey(
        Competitor,
        models.SET_NULL,
        related_name="competitor2",
        blank=True,
        null=True,
    )
    winner = models.ForeignKey(
        Competitor,
        models.SET_NULL,
        related_name="winner",
        blank=True,
        null=True,
    )

    def __str__(self):
        output = f"[{self.level_number}] Game {self.game_number}: {self.competitor1.id} vs {self.competitor2.id}"
        if self.winner:
            output += f"-> {self.winner.id}"
        return output

    def to_dict_json(self):
        return {
            "id": self.id,
            "tournament_id": self.tournament_id,
            "level_number": self.level_number,
            "game_number": self.game_number,
            "competitor1": self.competitor1.to_dict_json(),
            "competitor2": self.competitor2.to_dict_json(),
            "winner": self.winner.to_dict_json() if self.winner else None,
        }
