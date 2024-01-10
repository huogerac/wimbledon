import pytest

from unittest.mock import ANY
from wimbledon.core.models import Tournament


# TODO: Mockar o service
@pytest.mark.django_db
def test_deve_retornar_lista_vazia_de_torneios(client):
    resp = client.get("/api/core/tournaments/")
    data = resp.json()

    assert resp.status_code == 200
    assert data == {"tournaments": []}


@pytest.mark.django_db
def test_deve_retornar_lista_com_um_torneio(client):
    # Dado um torneio
    Tournament.objects.create(description="Wimbledon 2024")

    # Quando chamamos o listar
    resp = client.get("/api/core/tournaments/")
    data = resp.json()

    # Então
    assert resp.status_code == 200
    assert data == {
        "tournaments": [{"description": "Wimbledon 2024", "done": False, "id": ANY}]
    }


@pytest.mark.django_db
def test_deve_retornar_lista_com_um_torneio(client, list_42_tournaments):
    # Dado os torneios desde 2000 até 2041
    Tournament.objects.bulk_create(list_42_tournaments)

    # Quando chamamos o listar
    resp = client.get("/api/core/tournaments/")
    data = resp.json()

    # Então
    assert resp.status_code == 200
    assert len(data.get("tournaments")) == 42
