import pytest

from wimbledon.core.models import Tournament
from wimbledon.core.service import tournaments_svc


# TODO: Mockar o service
@pytest.mark.django_db
def test_deve_criar_novo_torneio():
    new_tour = tournaments_svc.add_tournament("ABC")

    tour = Tournament.objects.all().first()

    assert tour.id == new_tour.get("id")
    assert tour.description == new_tour.get("description")


@pytest.mark.django_db
def test_deve_retornar_lista_vazia():
    tour_list = tournaments_svc.list_tournaments()
    assert tour_list == []


@pytest.mark.django_db
def test_deve_listar_10_torneios(list_10_tournaments):
    # Dado 10 torneios
    Tournament.objects.bulk_create(list_10_tournaments)

    tour_list = tournaments_svc.list_tournaments()

    assert len(tour_list) == 10
