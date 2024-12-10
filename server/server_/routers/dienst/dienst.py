import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, status, Depends, HTTPException

from ..dienst.ondersteuning import genereer_dienst_id, geef_aantal_nachturen, is_feestdag
from ..dienst.model import RegistratieverzoekDienst, CreatieDienst
from ..werknemer.ondersteuning import seconden_naar_leesbaar, bereken_verdiend_loon_dienst, geef_werknemerdata
from ...databasis.databasis import geef_databasis
from ...databasis.model import Diensttabel, Werknemertabel


router: APIRouter = APIRouter(tags=["Dienst"])  # documentation title


@router.put("/dienst/registreer-dienst", status_code=status.HTTP_201_CREATED, response_model=CreatieDienst)
async def registreer_dienst(registratieverzoek_dienst: RegistratieverzoekDienst,
                            databasis: Session = Depends(geef_databasis)) -> CreatieDienst:
    """
    Registreert de dienst van een werknemer in de databasis.
    """
    seconden_gewerkt: float = (registratieverzoek_dienst.eind_dienst - registratieverzoek_dienst.start_dienst)

    starttijd_dienst: datetime.datetime = datetime.datetime.fromtimestamp(registratieverzoek_dienst.start_dienst)
    eindtijd_dienst: datetime.datetime = datetime.datetime.fromtimestamp(registratieverzoek_dienst.eind_dienst)

    data_werknemer: Werknemertabel = geef_werknemerdata(registratieverzoek_dienst.werknemer_id, databasis)

    if not data_werknemer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Werknemer niet gevonden.")

    aantal_nachturen: int = geef_aantal_nachturen(starttijd_dienst, eindtijd_dienst)
    is_feestdag_: bool = is_feestdag(starttijd_dienst)

    euros_verdiend: float = bereken_verdiend_loon_dienst(
        seconden_gewerkt,
        data_werknemer.uurloon,
        is_feestdag=is_feestdag_,
        aantal_uren_binnen_nachttoeslag=aantal_nachturen
    )

    try:
        dienst: Diensttabel = Diensttabel(
            id_=genereer_dienst_id(),
            werknemer_id=registratieverzoek_dienst.werknemer_id,
            starttijd=registratieverzoek_dienst.start_dienst,
            eindtijd=registratieverzoek_dienst.eind_dienst,
            verdiend_euro=euros_verdiend,
            duur_dienst_leesbaar=seconden_naar_leesbaar(seconden_gewerkt),
            aantal_nachturen=aantal_nachturen,
            feestdagtoeslag=is_feestdag_,
            datum=datetime.datetime.now()
        )

        data_werknemer.meest_recente_dienst = datetime.datetime.now()

        databasis.commit()
        databasis.refresh(data_werknemer)

        databasis.add(dienst)
        databasis.close()

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="server error")

    return CreatieDienst(is_geslaagd=True, euros_verdiend=euros_verdiend)
