from pydantic import BaseModel


class RegistratieverzoekDienst(BaseModel):
    werknemer_id: str
    start_dienst: float
    eind_dienst: float


class CreatieDienst(BaseModel):
    is_geslaagd: bool
    euros_verdiend: float
