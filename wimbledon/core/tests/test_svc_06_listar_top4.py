import pytest

from django.db import connection

from wimbledon.core.models import Tournament, Match
from wimbledon.core.service import tournaments_svc


# TODO: Mockar o service
@pytest.mark.django_db
def test_deve_listar_top4_com_4_competidores(tournament_mock):
    """
    Tem que gerar                 g1
                                  p1
       g3       g2              /    \ 
       p1       p3    #1      p1      p3      #2     p2
     /   \    /   \  ---->  /   \    /   \   ---->  /   \ 
    p1   p2  p3   p4       p1   p2  p3   p4        p2   p4
    """
    # Dado os competidores e torneio iniciado
    torneio = tournament_mock
    p1 = tournaments_svc.create_competitor(torneio.id, "p1")
    p2 = tournaments_svc.create_competitor(torneio.id, "p2")
    p3 = tournaments_svc.create_competitor(torneio.id, "p3")
    p4 = tournaments_svc.create_competitor(torneio.id, "p4")
    tournaments_svc.start_tournament(torneio.id, seed="id")
    game3, game2 = Match.objects.all()

    # Quando salvamos
    # Parte 1
    tournaments_svc.save_match_result(torneio.id, game3.id, p1.get("id"))
    tournaments_svc.save_match_result(torneio.id, game2.id, p3.get("id"))
    game_1_e_2_lugar, game_3_e_4_lugar = Match.objects.all().order_by(
        "level_number", "game_number"
    )[:2]

    tournaments_svc.save_match_result(torneio.id, game_1_e_2_lugar.id, p1.get("id"))
    tournaments_svc.save_match_result(torneio.id, game_3_e_4_lugar.id, p2.get("id"))

    top1, top2, top3, top4 = tournaments_svc.list_competitors_top4(torneio.id)

    assert top1.get("id") == p1.get("id")
    assert top2.get("id") == p3.get("id")
    assert top3.get("id") == p2.get("id")
    assert top4.get("id") == p4.get("id")
