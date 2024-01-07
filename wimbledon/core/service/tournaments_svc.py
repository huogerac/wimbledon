import random
from ..models import Tournament, Competitor, Match


def add_tournament(description):
    tournament = Tournament(description=description)
    tournament.save()
    return tournament.to_dict_json()


def list_tournaments():
    tournaments = Tournament.objects.all()
    return [item.to_dict_json() for item in tournaments]


def create_competitor(tournament_id, name):
    new_competitor = Competitor(tournament_id=tournament_id, name=name)
    new_competitor.save()
    return new_competitor.to_dict_json()


def start_tournament(tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    competitors = tournament.competitors.all().order_by("?")

    print("competitors:", [p.id for p in competitors])

    nr_competitors = len(competitors)
    game_count = nr_competitors - 1
    games = []

    # obtem level ## TODO!!!
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
        .filter(tournament_id=1)
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
    return match.to_dict_json()
