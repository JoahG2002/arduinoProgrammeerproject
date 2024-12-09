import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, ForeignKey, INTEGER, Float, Boolean, TIMESTAMP

from .databasis import Base


class Werknemertabel(Base):
    __tablename__: str = "Werknemer"

    id_: Mapped[str] = mapped_column(VARCHAR, primary_key=True, nullable=False)
    voornaam: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    achternaam: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    geboortedatum: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    werkgever_id: Mapped[str] = mapped_column(VARCHAR, ForeignKey("Werkgever.id_", ondelete="CASCADE"), nullable=False)
    uurloon: Mapped[float] = mapped_column(Float, nullable=False)
    is_in_vaste_dienst: Mapped[bool] = mapped_column(Boolean, nullable=False)
    btw_tarief_salaris: Mapped[float] = mapped_column(Float, nullable=False)
    is_ziek: Mapped[bool] = mapped_column(Boolean, nullable=False)
    functie: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    startdatum_dienst: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False)
    einde_dienst: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=True)
    meest_recente_dienst: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=True)

    def __str__(self) -> str:
        return f"Werknemertabel(id_={self.id_}, voornaam={self.voornaam}, achternaam={self.achternaam}, uurloon={self.uurloon})"


class Werkgevertabel(Base):
    __tablename__: str = "Werkgever"

    id_: Mapped[str] = mapped_column(VARCHAR, primary_key=True, nullable=False)
    voornaam: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    achternaam: Mapped[str] = mapped_column(VARCHAR, nullable=False)

    def __str__(self) -> str:
        return f"Werkgevertabel(id_={self.id_}, voornaam={self.voornaam}, achternaam={self.achternaam})"


class Diensttabel(Base):
    __tablename__: str = "Dienst"

    id_: Mapped[str] = mapped_column(VARCHAR, primary_key=True, nullable=False)
    werknemer_id: Mapped[str] = mapped_column(VARCHAR, ForeignKey("Werknemer.id_", ondelete="CASCADE"), nullable=False)
    starttijd: Mapped[float] = mapped_column(Float, nullable=False)
    eindtijd: Mapped[float] = mapped_column(Float, nullable=False)
    verdiend_euro: Mapped[float] = mapped_column(Float, nullable=False)
    duur_dienst_leesbaar: Mapped[float] = mapped_column(Float, nullable=False)
    aantal_nachturen: Mapped[int] = mapped_column(INTEGER, nullable=False)
    feestdagtoeslag: Mapped[bool] = mapped_column(Boolean, nullable=False)
    datum: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False)

    def __str__(self) -> str:
        return f"Diensttabel(id_={self.id_}, datum={self.datum}, duur_dienst_leesbaar={self.duur_dienst_leesbaar})"
