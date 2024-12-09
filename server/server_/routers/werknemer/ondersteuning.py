import string
import random

from typing import Optional
from sqlalchemy.orm import Session

from ...databasis.model import Werknemertabel
from ...ondersteuning.constant import toeslagen, lengten


def bereken_uren_en_minuten_gewerkt(seconden_gewerkt: float) -> tuple[int, int]:
    """
    Bereken het aantal uren en minuten gewerkt op basis van UNIX-tijdstempels.
    """
    uren_gewerkt: float = seconden_gewerkt // 3600
    resterende_seconden: float = seconden_gewerkt % 3600
    minuten_gewerkt: float = resterende_seconden // 60

    return round(uren_gewerkt), round(minuten_gewerkt)


def seconden_naar_leesbaar(seconden_gewerkt: float) -> str:
    """
    Ontvangt de tijd die een werknemer heeft gewerkt in seconden, en geeft deze in leesbaar vorm terug.
    """
    uren_gewerkt, overige_minuten = bereken_uren_en_minuten_gewerkt(seconden_gewerkt)

    return f"{uren_gewerkt} h {overige_minuten} min"


def bereken_verdiend_loon_dienst(seconden_gewerkt: float,
                                 uurloon_werknemer: float,
                                 is_feestdag: bool,
                                 aantal_uren_binnen_nachttoeslag: int
                                 ) -> float:
    """
    Berekent het verdiende loon van een werknemer — op basis van het aantal seconden gewerkt, of het al dan niet een feestdag is vandaag en of deze recht heeft op nachttoeslag.
    """
    loon_verdiend_dienst: float = (seconden_gewerkt / 60.0 / 60.0 * uurloon_werknemer)

    if aantal_uren_binnen_nachttoeslag > 0:
        loon_verdiend_dienst -= (float(aantal_uren_binnen_nachttoeslag) * uurloon_werknemer)
        loon_verdiend_dienst += (float(aantal_uren_binnen_nachttoeslag) * toeslagen.NACHTDIENST)

    if is_feestdag:
        loon_verdiend_dienst *= toeslagen.FEESTDAGEN

    return round(loon_verdiend_dienst, 2)


def geef_werknemerdata(werknemer_id: str, databasis: Session) -> Optional[Werknemertabel]:
    """
    Geeft de databasisdata van een werknemer terug.
    """
    return databasis.query(Werknemertabel).filter(Werknemertabel.id_ == werknemer_id).first()


def genereer_werknemer_id() -> str:
    """
    Genereert een id voor een werknemer.
    """
    return 'W' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(lengten.WERKNEMER_ID))
