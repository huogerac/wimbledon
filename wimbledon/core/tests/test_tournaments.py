from unittest.mock import ANY

from wimbledon.accounts.models import User
from wimbledon.accounts.tests import fixtures
from wimbledon.core.models import Tournament


def test_criar_tournament_com_login(client, db):
    payload = {"description": "Wimbledon 2024"}
    resp = client.post(
        "/api/core/tournaments/", payload, content_type="application/json"
    )
    assert resp.status_code == 200


def test_listar_tournament(client, db):
    Tournament.objects.create(description="Wimbledon 2024")

    resp = client.get("/api/core/tournaments/")
    data = resp.json()

    assert resp.status_code == 200
    assert data == {
        "tournaments": [{"description": "Wimbledon 2024", "done": False, "id": ANY}]
    }
