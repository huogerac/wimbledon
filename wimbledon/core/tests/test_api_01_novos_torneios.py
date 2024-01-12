import pytest
from unittest.mock import ANY

from wimbledon.core.models import Tournament


# TODO: Mockar o service
@pytest.mark.django_db
def test_deve_criar_novo_torneio_passando_todos_campos(client):
    # Dado uma entrada válida
    payload = {"description": "Wimbledon 2024"}

    # Quando
    resp = client.post(
        "/api/core/tournaments/", payload, content_type="application/json"
    )

    # Então
    assert resp.status_code == 201
    assert resp.json() == {
        "id": ANY,
        "description": "Wimbledon 2024",
        "done": False,  # Torneio nao acabou
    }


def test_deve_falhar_com_input_invalido(client):
    # Dado uma entrada inválida
    payload = {}

    # Quando
    resp = client.post(
        "/api/core/tournaments/", payload, content_type="application/json"
    )

    # Então
    assert resp.status_code == 422  # BAD REQUEST
    assert resp.json().get("detail")[0].get("loc") == [
        "body",
        "tournament",
        "description",
    ]
    assert resp.json().get("detail")[0].get("msg") == "field required"
