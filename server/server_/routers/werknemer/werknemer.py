import datetime

from sqlalchemy import extract
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends, HTTPException

from .model import Loonstrookverzoek, Loonstrook, Loonstrookbundel, Werknemer
from .ondersteuning import genereer_werknemer_id
from ...databasis.databasis import geef_databasis
from ...databasis.model import Diensttabel, Werknemertabel
from ...ondersteuning.constant import tijden

router: APIRouter = APIRouter(tags=["Werknemer"])  # documentation title


@router.put("/werknemer/creeer-werknemer", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
def creeer_werknemer(werknemer: Werknemer, databasis: Session = Depends(geef_databasis)) -> dict[str, str]:
    """
    Geeft één of meer loonstroken van een werknemer terug.
    """
    werknemer_id: str = genereer_werknemer_id()

    nieuwe_werknemer: Werknemertabel = Werknemertabel(
        id_=werknemer_id,
        voornaam=werknemer.voornaam,
        achternaam=werknemer.achternaam,
        geboortedatum=werknemer.geboortedatum,
        werkgever=werknemer.werkgever,
        uurloon=werknemer.uurloon,
        is_in_vaste_dienst=werknemer.is_in_vaste_dienst,
        btw_tarief_salaris=werknemer.btw_tarief_salaris,
        is_ziek=werknemer.is_ziek,
        functie=werknemer.functie,
        startdatum_dienst=datetime.datetime.fromtimestamp(werknemer.startdatum_dienst),
    )

    try:
        databasis.add(nieuwe_werknemer)
        databasis.close()

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Creatie werknemer mislukt.")

    return {"werknemer_id": werknemer_id}


@router.get("/werknemer/geef-loonstrook", status_code=status.HTTP_200_OK, response_model=Loonstrookbundel)
def geef_loonstrook(loonstrookverzoek: Loonstrookverzoek, databasis: Session = Depends(geef_databasis)) -> Loonstrookbundel:
    """
    Geeft één of meer loonstroken van een werknemer terug.
    """
    if loonstrookverzoek.maand == '*':
        diensten: list[Diensttabel] = (
            databasis.query(Diensttabel)
            .filter(Diensttabel.werknemer_id == loonstrookverzoek.werknemer_id)
            .all()
        )
    else:
        maandnummer: int = tijden.MAANDEN_MET_NUMMER.get(loonstrookverzoek.maand.lower(), -1)

        if maandnummer == -1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ongeldige maand: {loonstrookverzoek.maand}"
            )

        diensten: list[Diensttabel] = (
            databasis.query(Diensttabel).filter(
                Diensttabel.werknemer_id == loonstrookverzoek.werknemer_id,
                extract("month", Diensttabel.datum) == maandnummer
            ).all()
        )

    if not diensten:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Geen loonstroken beschikbaar.")

    maanden_met_loonstroken: dict[int, list[Loonstrook]] = {
        maandnummer: [] for maandnummer in {dienst.datum.month for dienst in diensten}
    }

    for unieke_maand in maanden_met_loonstroken.keys():
        loonstrook: Loonstrook = Loonstrook(
            euros_verdiend_maand=0.0,
            diensten_eenvoudig=[]
        )

        for i, dienst in enumerate(diensten):
            if not (dienst.datum.month == unieke_maand):
                continue

            loonstrook.euros_verdiend_maand += dienst.verdiend_euro

            loonstrook.diensten_eenvoudig.append(
                {
                    "datum_dienst": dienst.datum,
                    "duur_dienst_leesbaar": dienst.duur_dienst_leesbaar,
                    "starttijd": dienst.starttijd,
                    "eindtijd": dienst.eindtijd,
                    "aantal_nachturen": dienst.aantal_nachturen,
                    "feestdagtoeslag": dienst.feestdagtoeslag
                }
            )

        maanden_met_loonstroken[unieke_maand].append(loonstrook)

    return Loonstrookbundel(
        werknemer_id=loonstrookverzoek.werknemer_id,
        loonstroken_per_maand=maanden_met_loonstroken
    )
