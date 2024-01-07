from ..models import Tournament


def add_tournament(new_tournament):
    tournament = Tournament(description=new_tournament)
    tournament.save()
    return tournament.to_dict_json()


def list_tournaments():
    tournaments = Tournament.objects.all()
    return [item.to_dict_json() for item in tournaments]
