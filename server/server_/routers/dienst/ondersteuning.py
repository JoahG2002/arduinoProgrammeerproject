import random
import string

from datetime import datetime, timedelta

from ...ondersteuning.constant import lengten, tijden


def genereer_dienst_id() -> str:
    """
    Genereert een id voor een dienst.
    """
    return 'D' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(lengten.DIENST_ID))


def geef_aantal_nachturen(starttijd_dienst: datetime, eindtijd_dienst: datetime) -> int:
    """
    Geeft het aantal nachturen in een dienst terug.
    """
    nacht_start: datetime = starttijd_dienst.replace(hour=21, minute=0, second=0, microsecond=0)
    nacht_eind: datetime = starttijd_dienst.replace(hour=6, minute=0, second=0, microsecond=0) + timedelta(days=1)

    if eindtijd_dienst < starttijd_dienst:
        eindtijd_dienst += timedelta(days=1)

    begin_nacht: datetime = max(starttijd_dienst, nacht_start)
    eind_nacht: datetime = min(eindtijd_dienst, nacht_eind)

    if begin_nacht < eind_nacht:
        nachturen: int = (eind_nacht - begin_nacht).seconds // 3600

        return nachturen

    return 0


def is_feestdag(starttijd_dienst: datetime) -> bool:
    """
    Geeft terug of de datum van een dienst een feestdag is. Ondersteunde feestdagen zijn hardcoded en gelden voor Nederland:

    - Nieuwjaarsdag: 1 januari;
    - Koningsdag: 27 april;
    - Eerste Paasdag: variabel;
    - Eerste Kerstdag: 25 december;
    - Tweede Kerstdag: 26 december;
    - Goede Vrijdag: variabel;
    - Hemelvaartsdag: variabel.
    """
    jaar: int = starttijd_dienst.year
    paasdatum: datetime = bereken_paasdatum(jaar)
    goede_vrijdag: datetime = paasdatum - timedelta(days=2)
    hemelvaart: datetime = paasdatum + timedelta(days=39)

    variabele_feestdagen = {
        (goede_vrijdag.day, goede_vrijdag.month),
        (paasdatum.day, paasdatum.month),
        (hemelvaart.day, hemelvaart.month),
    }

    alle_feestdagen: set[tuple[int, int]] = tijden.VASTE_FEESTDAGEN.union(variabele_feestdagen)

    return (starttijd_dienst.day, starttijd_dienst.month) in alle_feestdagen


def bereken_paasdatum(jaar: int) -> datetime:
    """
    Bereken de datum van Eerste Paasdag voor een gegeven jaar — gebaseerd op het algoritme van de "Computus".
    """
    a: int = jaar % 19
    b: int = jaar // 100
    c: int = jaar % 100
    d: int = b // 4
    e: int = b % 4
    f: int = (b + 8) // 25
    g: int = (b - f + 1) // 3
    h: int = (19 * a + b - d - g + 15) % 30
    i: int = c // 4
    k: int = c % 4
    l: int = (32 + 2 * e + 2 * i - h - k) % 7
    m: int = (a + 11 * h + 22 * l) // 451

    maand: int = (h + l - 7 * m + 114) // 31
    dag: int = ((h + l - 7 * m + 114) % 31) + 1

    return datetime(jaar, maand, dag)
