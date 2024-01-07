# coding: utf-8

from django.http import JsonResponse

from ninja import Router
from .schemas import (
    ListTournamentsSchema,
    TournamentSchema,
    TournamentSchemaIn,
    CompetitorSchema,
    CompetitorSchemaIn,
    ListMatchesSchema,
)
from .service import tournaments_svc


router = Router()


@router.get("/tournaments/{tournament_id}", response=TournamentSchema)
def get_tournament(request, tournament_id):
    # TODO:
    # new_tournament = tournaments_svc.add_tournament(tournament.description)
    return JsonResponse({})


@router.post("/tournaments/", response=TournamentSchema)
def add_tournament(request, tournament: TournamentSchemaIn):
    new_tournament = tournaments_svc.add_tournament(tournament.description)
    return JsonResponse(new_tournament)


@router.get("/tournaments/", response=ListTournamentsSchema)
def list_tournaments(request):
    tournaments = tournaments_svc.list_tournaments()
    return JsonResponse({"tournaments": tournaments})


@router.post("/tournaments/{tournament_id}/competitor", response=CompetitorSchema)
def create_competitor(request, tournament_id, competitor: CompetitorSchemaIn):
    new_competitor = tournaments_svc.create_competitor(tournament_id, competitor.name)
    return JsonResponse(new_competitor)


@router.get("/tournaments/{tournament_id}/competitor", response=CompetitorSchema)
def list_competitors(request, tournament_id):
    competitors = {}
    #: TODO
    return JsonResponse(competitors)


@router.post("/tournaments/{tournament_id}/start", response=ListMatchesSchema)
def start_tournament(request, tournament_id):
    matches = tournaments_svc.start_tournament(tournament_id)
    return JsonResponse({"matches": matches})


@router.get("/tournaments/{tournament_id}/match", response=ListMatchesSchema)
def list_matches(request, tournament_id):
    matches = tournaments_svc.list_matches(tournament_id)
    return JsonResponse({"matches": matches})


@router.post("/tournaments/{tournament_id}/match/{match_id}")
def save_match_result(request, tournament_id, match_id, winner_competitor_id: int):
    match = tournaments_svc.save_match_result(
        tournament_id, match_id, winner_competitor_id
    )
    return JsonResponse(match)
