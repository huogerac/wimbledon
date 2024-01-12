import pytest

from wimbledon.core.models import Tournament, Competitor
from wimbledon.core.service import tournaments_svc


# TODO: Mockar o service
@pytest.mark.django_db
def test_deve_criar_novo_competidor(tournament_mock):
    novo_competidor = tournaments_svc.create_competitor(
        tournament_mock.id, "Rafael Nadal"
    )

    competidor_db = Competitor.objects.all().first()

    assert competidor_db.id == novo_competidor.get("id")
    assert competidor_db.name == novo_competidor.get("name")


@pytest.mark.django_db
def test_deve_nao_permite_nomes_duplicados_no_mesmo_torneio(tournament_mock):
    # Dado um campetidor cadastrado
    tournaments_svc.create_competitor(tournament_mock.id, "Rafael Nadal")

    # Quando tentamos cadastrá-lo novamente
    with pytest.raises(ValueError) as error:
        tournaments_svc.create_competitor(tournament_mock.id, "Rafael Nadal")

    # Então
    assert str(error.value) == "'Rafael Nadal' already exists for this tounament."


@pytest.mark.django_db
def test_deve_permitir_duplicar_competidor_para_diferentes_torneios():
    # Dado dois torneios
    tournament1 = Tournament.objects.create(description="Wimbledon 2024")
    tournament2 = Tournament.objects.create(description="Wimbledon 2025")

    # Quando tentamos cadastrar duas vezes
    tournaments_svc.create_competitor(tournament1.id, "Rafael Nadal")
    tournaments_svc.create_competitor(tournament2.id, "Rafael Nadal")
    competidores_list = Competitor.objects.filter(name="Rafael Nadal")

    # Então
    assert len(competidores_list) == 2
