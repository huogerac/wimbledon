from django.db.models import Count, Max
from django.db.utils import IntegrityError
from django.db import DatabaseError, transaction

from ..models import Tournament, Competitor, Match


def add_tournament(description):
    tournament = Tournament(description=description)
    tournament.save()
    return tournament.to_dict_json()


def list_tournaments():
    tournaments = Tournament.objects.all()
    return [item.to_dict_json() for item in tournaments]


def create_competitor(tournament_id, name):
    try:
        new_competitor = Competitor(tournament_id=tournament_id, name=name)
        new_competitor.save()
        return new_competitor.to_dict_json()

    except IntegrityError as error:
        raise ValueError(f"'{name}' already exists for this tounament.")


def start_tournament(tournament_id, seed="?"):
    tournament = Tournament.objects.get(id=tournament_id)
    competitors = tournament.competitors.all().order_by(seed)

    nr_competitors = len(competitors)
    game_count = nr_competitors - 1

    # obter level usando matemática ## TODO!!!
    game_level = 1
    if nr_competitors > 2 and nr_competitors <= 4:
        game_level = 2
    elif nr_competitors > 4 and nr_competitors <= 8:
        game_level = 3
    elif nr_competitors > 8 and nr_competitors <= 16:
        game_level = 4

    while competitors:
        next_game, competitors = competitors[:2], competitors[2:]
        p1, p2 = next_game
        new_match = Match(
            tournament=tournament,
            game_number=game_count,
            level_number=game_level,
            competitor1=p1,
            competitor2=p2,
        )
        game_count -= 1
        new_match.save()

    return list_matches(tournament_id)


def list_matches(tournament_id):
    matches = (
        Match.objects.select_related("competitor1")
        .select_related("competitor2")
        .select_related("winner")
        .filter(tournament_id=tournament_id)
        .order_by("level_number", "game_number")
    )
    return [m.to_dict_json() for m in matches]


def save_match_result(tournament_id, match_id, winner_competitor_id):
    # tournament = Tournament.objects.get(id=tournament_id)
    # TODO: - validate the match_id vs tournament
    # TODO: - validate the match existing state, winner set etc..
    match = Match.objects.get(id=match_id)
    competitor = Competitor.objects.get(id=winner_competitor_id)
    match.winner = competitor
    match.save()

    prepare_next_level_matches(tournament_id)
    return match.to_dict_json()


def prepare_next_level_matches(tournament_id):
    matches_playing_by_level = (
        Match.objects.values("level_number")
        .filter(tournament_id=tournament_id)
        .annotate(
            games_total=Count("level_number"),
            games_winners=Count("winner"),
            last_game_number=Max("game_number"),
        )
        .order_by("level_number")
    )

    level_number = matches_playing_by_level[0].get("level_number")
    games_total = matches_playing_by_level[0].get("games_total")
    games_winners = matches_playing_by_level[0].get("games_winners")
    last_game_number = matches_playing_by_level[0].get("games_winners")

    all_games_with_winners = games_winners == games_total
    final = level_number == 1
    if not all_games_with_winners or final:
        return

    # current level finished, let's create the next one
    level_matches = (
        Match.objects.select_related("competitor1")
        .select_related("competitor2")
        .select_related("winner")
        .filter(tournament_id=tournament_id, level_number=level_number)
        .order_by("level_number", "game_number")
    )

    last_game_number -= 1
    level_number -= 1

    while len(level_matches) > 0:
        next_final, level_matches = level_matches[:2], level_matches[2:]
        g1, g2 = next_final
        new_match = Match(
            tournament_id=tournament_id,
            game_number=last_game_number,
            level_number=level_number,
            competitor1=g1.winner,
            competitor2=g2.winner,
        )
        new_match.save()
        last_game_number -= 1
