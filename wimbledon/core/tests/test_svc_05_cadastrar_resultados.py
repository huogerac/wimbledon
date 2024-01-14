import pytest

from django.db import connection

from wimbledon.core.models import Tournament, Match
from wimbledon.core.service import tournaments_svc


# TODO: Mockar o service
@pytest.mark.django_db
def test_deve_salvar_resultado_e_gerar_final(tournament_mock):
    """
       ?                p1
     /   \   ---->     /   \ 
    p1   p2           p1   p2
    """
    # Dado 2 competidores e torneio iniciado
    torneio = tournament_mock
    p1 = tournaments_svc.create_competitor(torneio.id, "p1")
    p2 = tournaments_svc.create_competitor(torneio.id, "p2")
    matches = tournaments_svc.start_tournament(torneio.id, seed="id")
    final = matches[0]

    # Quando iniciamos o torneio
    final = tournaments_svc.save_match_result(torneio.id, final.get("id"), p1.get("id"))

    # Então
    assert final.get("game_number") == 1
    assert final.get("competitor1").get("name") == "p1"
    assert final.get("competitor2").get("name") == "p2"
    assert final.get("winner").get("name") == "p1"


@pytest.mark.django_db
def test_deve_salvar_resultado_e_gerar_final_e_semi_final(tournament_mock):
    """
    Tem que gerar           game3      game2           game1            game101
                                                         p1              p2
                                                       /    \           /  \ 
       ?        ?     #1      p1       p3     #2     p1       p3       p2  p4
     /   \    /   \  ---->  /   \    /   \   ---->  /   \    /   \ 
    p1   p2  p3   p4       p1   p2  p3   p4        p1   p2  p3   p4
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
    game3, game2, game1, game101 = Match.objects.all()

    # Parte 2
    tournaments_svc.save_match_result(torneio.id, game1.id, p1.get("id"))
    tournaments_svc.save_match_result(torneio.id, game101.id, p2.get("id"))
    game3, game2, game1, game101 = Match.objects.all()

    # Então
    # Parte 1
    assert game3.winner.id == p1.get("id")
    assert game2.winner.id == p3.get("id")
    # Parte 2
    assert game1.winner.id == p1.get("id")
    assert game101.winner.id == p2.get("id")  # 3o. lugar


@pytest.mark.django_db
def test_deve_salvar_resultado_fase2_com_6_jogadores(tournament_mock):
    """
            g           ?
          /  \          |
       p1      p3       p5 
     /   \    /  \     /  \ 
    p1   p2  p3   p4  p5   p6
    """
