from django.db.models import Count, Max
from django.db.utils import IntegrityError

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

    except IntegrityError:
        raise ValueError(f"'{name}' already exists for this tounament.")


def list_competitors(tournament_id, order_by="name"):
    competitors = Competitor.objects.filter(tournament_id=tournament_id).order_by(
        order_by
    )
    return [c.to_dict_json() for c in competitors]


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
    elif nr_competitors > 16 and nr_competitors <= 32:
        game_level = 5

    while competitors:
        next_game, competitors = competitors[:2], competitors[2:]
        if len(next_game) == 1:
            new_match = Match(
                tournament=tournament,
                game_number=0,
                level_number=game_level,
                competitor1=next_game[0],
                competitor2=next_game[0],
                winner=next_game[0],
                auto_win=True,
            )
            new_match.save()
            continue

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

        if len(level_matches) == 1:
            new_match = Match(
                tournament_id=tournament_id,
                game_number=0,
                level_number=level_number,
                competitor1=level_matches[0].winner,
                competitor2=level_matches[0].winner,
                winner=level_matches[0].winner,
                auto_win=True,
            )
            new_match.save()
            level_matches = []
            continue

        if level_number == 1 and len(level_matches) == 0:
            if g1.auto_win or g2.auto_win:
                continue
            g1_loser = g1.competitor2 if g1.winner == g1.competitor1 else g1.competitor1
            g2_loser = g2.competitor2 if g2.winner == g2.competitor1 else g2.competitor1
            new_match = Match(
                tournament_id=tournament_id,
                game_number=last_game_number + 100,
                level_number=level_number,
                game_extra=True,
                competitor1=g1_loser,
                competitor2=g2_loser,
            )
            new_match.save()

        last_game_number -= 1


def list_competitors_top4(tournament_id):
    # TODO: Não retorna os 4 ganhadores dependendo o nro de competidores
    top_matches = (
        Match.objects.select_related("competitor1")
        .select_related("competitor2")
        .select_related("winner")
        .filter(tournament_id=tournament_id, level_number=1)
        .filter(winner__isnull=False)
        .order_by("level_number", "game_number")
    )
    if not top_matches:
        return []

    if len(top_matches) == 1:
        g1 = top_matches[0]
        g1_vice = g1.competitor2 if g1.winner == g1.competitor1 else g1.competitor1
        list_top4 = [g1.winner, g1_vice]
    else:
        g1, g2 = top_matches
        g1_vice = g1.competitor2 if g1.winner == g1.competitor1 else g1.competitor1
        g2_vice = g2.competitor2 if g2.winner == g2.competitor1 else g2.competitor1
        list_top4 = [g1.winner, g1_vice, g2.winner, g2_vice]
    return [m.to_dict_json() for m in list_top4]
