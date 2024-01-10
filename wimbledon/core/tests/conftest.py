import pytest
from wimbledon.core.models import Tournament


def generate_tournament_list(name_prefix="Wimbledon", count=10):
    year = 2000
    years = list(range(year, year + count))
    tournaments = [Tournament(description=f"${name_prefix} ${y})") for y in years]
    return tournaments


@pytest.fixture
def tournament_mock():
    tournament = Tournament.objects.create(description="Wimbledon 2024")
    return tournament


@pytest.fixture
def list_10_tournaments():
    return generate_tournament_list()


@pytest.fixture
def list_42_tournaments():
    return generate_tournament_list("Wimbledon", 42)
