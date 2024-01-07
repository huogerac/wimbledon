# coding: utf-8

from django.http import JsonResponse

from ninja import Router
from .schemas import ListTournamentsSchema, TournamentSchema, TournamentSchemaIn
from .service import tournaments_svc


router = Router()


@router.post("/tournaments/", response=TournamentSchema)
def add_tournament(request, tournament: TournamentSchemaIn):
    new_tournament = tournaments_svc.add_tournament(tournament.description)

    return JsonResponse(new_tournament)


@router.get("/tournaments/", response=ListTournamentsSchema)
def list_tournaments(request):
    tournaments = tournaments_svc.list_tournaments()
    return JsonResponse({"tournaments": tournaments})
