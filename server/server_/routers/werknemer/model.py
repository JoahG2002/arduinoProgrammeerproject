from typing import Literal
from pydantic import BaseModel


class Werknemer(BaseModel):
    voornaam: str
    achternaam: str
    geboortedatum: str
    werkgever_id: str
    uurloon: float
    is_in_vaste_dienst: bool
    btw_tarief_salaris: float
    is_ziek: bool
    functie: str
    startdatum_dienst: float


class Loonstrookverzoek(BaseModel):
    werknemer_id: str
    maand: Literal['*', "huidige"]


class Loonstrook(BaseModel):
    euros_verdiend_maand: float
    diensten_eenvoudig: list[dict[str, str | float | int | bool]]


class Loonstrookbundel(BaseModel):
    werknemer_id: str
    loonstroken_per_maand: dict[int, list[Loonstrook]]
