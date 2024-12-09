import requests

from requests import RequestException, Response

from ...ondersteuning.constant import urls


def verzoek_creatie_werknemer(voornaam: str, achternaam: str, geboortedatum: str, werkgever: str, uurloon: float,
                              is_in_vaste_dienst: bool, btw_tarief_salaris: float, is_ziek: bool, functie: str,
                              startdatum_dienst: float) -> dict[str, str]:
    """
    Verzoekt de creatie van een werknemer van de server.
    """
    try:
        reactie_creatie_server: Response = requests.put(
            f"{urls.KLOKKERSERVER}/werknemer/creeer-werknemer",
            json={
                "voornaam": voornaam,
                "achternaam": achternaam,
                "geboortedatum": geboortedatum,
                "werkgever_id": werkgever,
                "uurloon": uurloon,
                "is_in_vaste_dienst": is_in_vaste_dienst,
                "btw_tarief_salaris": btw_tarief_salaris,
                "is_ziek": is_ziek,
                "functie": functie,
                "startdatum_dienst": startdatum_dienst
            }
        )

    except RequestException:
        return {}

    if not (reactie_creatie_server.status_code == 201):
        return {}

    return reactie_creatie_server.json()
