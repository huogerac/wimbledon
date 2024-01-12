# coding: utf-8

from django.http import JsonResponse

from ninja import Router
from .schemas import (
    ListTournamentsSchema,
    TournamentSchema,
    TournamentSchemaIn,
    CompetitorSchema,
    CompetitorSchemaIn,
    ListCompetitorsSchema,
    ListMatchesSchema,
)
from .service import tournaments_svc


router = Router()


@router.get("/tournaments/{tournament_id}", response=TournamentSchema)
def get_tournament(request, tournament_id):
    # TODO:
    # new_tournament = tournaments_svc.add_tournament(tournament.description)
    return JsonResponse({})


@router.post("/tournaments/", response={201: TournamentSchema})
def add_tournament(request, tournament: TournamentSchemaIn):
    new_tournament = tournaments_svc.add_tournament(tournament.description)
    return JsonResponse(new_tournament, status=201)


@router.get("/tournaments/", response=ListTournamentsSchema)
def list_tournaments(request):
    tournaments = tournaments_svc.list_tournaments()
    return JsonResponse({"tournaments": tournaments})


@router.post("/tournaments/{tournament_id}/competitor", response=CompetitorSchema)
def create_competitor(request, tournament_id, competitor: CompetitorSchemaIn):
    new_competitor = tournaments_svc.create_competitor(tournament_id, competitor.name)
    return JsonResponse(new_competitor)


@router.get("/tournaments/{tournament_id}/competitor", response=ListCompetitorsSchema)
def list_competitors(request, tournament_id):
    competitors = tournaments_svc.list_competitors(tournament_id)
    return JsonResponse({"competitors": competitors})


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


@router.get("/tournaments/{tournament_id}/result", response=ListCompetitorsSchema)
def list_top4_competitors(request, tournament_id):
    matches = tournaments_svc.list_competitors_top4(tournament_id)
    return JsonResponse({"competitors": matches})
