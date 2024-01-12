import pytest

from django.db import connection

from wimbledon.core.models import Tournament, Match
from wimbledon.core.service import tournaments_svc


# TODO: Mockar o service
@pytest.mark.django_db
def test_deve_gerar_final_com_2_competidores(tournament_mock):
    """
     final
     /  \
    p1  p2
    """
    # Dado 2 competidores
    p1 = tournaments_svc.create_competitor(tournament_mock.id, "p1")
    p2 = tournaments_svc.create_competitor(tournament_mock.id, "p2")

    # Quando iniciamos o torneio
    matches = tournaments_svc.start_tournament(tournament_mock.id, seed="id")
    final = matches[0]

    assert len(matches) == 1
    assert final.get("game_number") == 1
    assert final.get("level_number") == 1
    assert final.get("competitor1").get("name") == "p1"
    assert final.get("competitor2").get("name") == "p2"
    assert final.get("winner") == None


@pytest.mark.django_db
def test_deve_gerar_2_jogos_iniciais_com_4_competidores(tournament_mock):
    """
      g2     g3
     / \    / \
    p1 p2  p3 p4
    """
    """Com 4 competidores, devemos gerar 2 jogos de semi final"""
    p1 = tournaments_svc.create_competitor(tournament_mock.id, "p1")
    p2 = tournaments_svc.create_competitor(tournament_mock.id, "p2")
    p3 = tournaments_svc.create_competitor(tournament_mock.id, "p3")
    p4 = tournaments_svc.create_competitor(tournament_mock.id, "p4")

    # Quando iniciamos o torneio
    matches = tournaments_svc.start_tournament(tournament_mock.id, seed="id")
    g2, g3 = matches

    assert len(matches) == 2
    assert g2.get("level_number") == 2
    assert g3.get("level_number") == 2

    assert g2.get("game_number") == 2
    assert g3.get("game_number") == 3


@pytest.mark.django_db
def test_deve_gerar_3_jogos_iniciais_com_6_competidores(tournament_mock):
    """
      g5     g4    g3
     / \    / \    / \
    p1 p2  p3 p4  p5 p6
    """
    # Dado 6 competidores
    p1 = tournaments_svc.create_competitor(tournament_mock.id, "p1")
    p2 = tournaments_svc.create_competitor(tournament_mock.id, "p2")
    p3 = tournaments_svc.create_competitor(tournament_mock.id, "p3")
    p4 = tournaments_svc.create_competitor(tournament_mock.id, "p4")
    p5 = tournaments_svc.create_competitor(tournament_mock.id, "p5")
    p6 = tournaments_svc.create_competitor(tournament_mock.id, "p6")

    # Quando iniciamos o torneio
    tournaments_svc.start_tournament(tournament_mock.id, seed="id")
    matches = Match.objects.all()
    g5, g4, g3 = matches

    # Então
    assert g5.game_number == 5
    assert g5.competitor1.name == "p1"
    assert g5.competitor2.name == "p2"

    assert g4.game_number == 4
    assert g4.competitor1.name == "p3"
    assert g4.competitor2.name == "p4"

    assert g3.game_number == 3
    assert g3.competitor1.name == "p5"
    assert g3.competitor2.name == "p6"


@pytest.mark.django_db
def test_deve_gerar_3_e_enviar_jogador_sem_par_para_proxima_fase(tournament_mock):
    """
      g5     g4    g3      --> envia para prox. fase
     / \    / \    / \    /
    p1 p2  p3 p4  p5 p6  p7
    """
    # Dado 6 competidores
    p1 = tournaments_svc.create_competitor(tournament_mock.id, "p1")
    p2 = tournaments_svc.create_competitor(tournament_mock.id, "p2")
    p3 = tournaments_svc.create_competitor(tournament_mock.id, "p3")
    p4 = tournaments_svc.create_competitor(tournament_mock.id, "p4")
    p5 = tournaments_svc.create_competitor(tournament_mock.id, "p5")
    p6 = tournaments_svc.create_competitor(tournament_mock.id, "p6")
    p7 = tournaments_svc.create_competitor(tournament_mock.id, "p7")

    # Quando iniciamos o torneio
    tournaments_svc.start_tournament(tournament_mock.id, seed="id")
    matches = Match.objects.all()
    g6, g5, g4, g0 = matches

    # Então
    assert g6.game_number == 6
    assert g6.competitor1.name == "p1"
    assert g6.competitor2.name == "p2"

    assert g5.game_number == 5
    assert g5.competitor1.name == "p3"
    assert g5.competitor2.name == "p4"

    assert g4.game_number == 4
    assert g4.competitor1.name == "p5"
    assert g4.competitor2.name == "p6"

    assert g0.game_number == 0
    assert g0.competitor1.name == "p7"
    assert g0.competitor2.name == "p7"
    assert g0.auto_win == True
    assert g0.winner.name == "p7"
