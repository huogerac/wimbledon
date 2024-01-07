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
