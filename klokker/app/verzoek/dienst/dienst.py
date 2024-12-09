import sys
import requests

from requests import Response, RequestException

from ...ondersteuning.constant import urls


def verzoek_dienstregistratie(werknemer_id: str, start_dienst: float, eind_dienst: float) -> tuple[float, int]:
    """
    Verzoekt de registratie van een dienst van een werknemer, en geeft een succescode terug.
    """
    try:
        reactie_dienst_registratie: Response = requests.put(
            f"{urls.KLOKKERSERVER}/dienst/registreer-dienst",
            json={
                "werknemer_id": werknemer_id,
                "start_dienst": start_dienst,
                "eind_dienst": eind_dienst
            }
        )

        sys.stdout.write(
            f"[VERZOEK]\t{urls.KLOKKERSERVER}/werknemer/registreer-dienst"
            f" {reactie_dienst_registratie.status_code}\n"
        )

    except RequestException:
        return 0.0, -1

    if not (reactie_dienst_registratie.status_code == 201):
        return 0.0, -1

    return reactie_dienst_registratie.json()["euros_verdiend"], 0

