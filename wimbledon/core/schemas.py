from typing import List, Optional

from ninja import Schema


class TournamentSchemaIn(Schema):
    description: str


class TournamentSchema(Schema):
    id: Optional[int]
    description: str
    done: bool = False


class ListTournamentsSchema(Schema):
    tournaments: List[TournamentSchema]


class CompetitorSchema(Schema):
    id: Optional[int]
    tournament_id: int
    name: str


class CompetitorSchemaIn(Schema):
    name: str


class ListCompetitorsSchema(Schema):
    competitors: List[CompetitorSchema]


class MatchSchema(Schema):
    id: int
    tournament_id: int
    level_number: int
    game_number: int
    competitor1: Optional[CompetitorSchema]
    competitor2: Optional[CompetitorSchema]
    winner: Optional[CompetitorSchema]


class ListMatchesSchema(Schema):
    matches: List[MatchSchema]
