

def bereken_uren_en_minuten_gewerkt(starttijd_dienst: float, eindtijd_dienst: float) -> tuple[int, int]:
    """
    Bereken het aantal uren en minuten gewerkt op basis van UNIX-tijdstempels.
    """
    totaal_seconden_gewerkt: float = (eindtijd_dienst - starttijd_dienst)
    uren_gewerkt: float = totaal_seconden_gewerkt // 3600
    resterende_seconden: float = totaal_seconden_gewerkt % 3600
    minuten_gewerkt: float = resterende_seconden // 60

    return round(uren_gewerkt), round(minuten_gewerkt)
