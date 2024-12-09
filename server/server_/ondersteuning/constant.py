import os
import sys

from typing import Final

from .env import lees_env_variabelen


current_working_directory: str = os.getcwd().replace("\\", '/')


class ToegangDatabasis:
    __slots__: tuple[str, ...] = (
        "WACHTWOORD_DATABASIS", "POORT_DATABASIS", "HOSTNAME_DATABASIS", "GEBRUIKERNAAM_DATABASIS", "NAAM_DATABASIS",
        "SQLALCHEMY_DATABASISLINK"
    )

    def __init__(self) -> None:
        ENV_VARIABLES: dict[str, str] = lees_env_variabelen()

        if not ENV_VARIABLES:
            sys.stdout.write(f"\nCould not read .env.\n")

            quit()

        self.WACHTWOORD_DATABASIS: Final[str] = ENV_VARIABLES["PASSWORD_DATABASE"]
        self.POORT_DATABASIS: Final[str] = ENV_VARIABLES["PORT_DATABASE"]
        self.HOSTNAME_DATABASIS: Final[str] = ENV_VARIABLES["HOSTNAME_DATABASE"]
        self.GEBRUIKERNAAM_DATABASIS: Final[str] = ENV_VARIABLES["USERNAME_DATABASE"]
        self.NAAM_DATABASIS: Final[str] = ENV_VARIABLES["NAME_DATABASE"]
        self.SQLALCHEMY_DATABASISLINK: str = (
            f"postgresql://{self.GEBRUIKERNAAM_DATABASIS}:{self.WACHTWOORD_DATABASIS}@"
            f"{self.HOSTNAME_DATABASIS}:{self.POORT_DATABASIS}/{self.NAAM_DATABASIS}"
        )


class Toeslag:
    __slots__: tuple[str, ...] = ("FEESTDAGEN", "NACHTDIENST")

    def __init__(self) -> None:
        self.FEESTDAGEN: Final[float] = 2.0
        self.NACHTDIENST: Final[float] = 1.6


class Lengte:
    __slots__: tuple[str, ...] = ("DIENST_ID", "WERKNEMER_ID")

    def __init__(self) -> None:
        self.DIENST_ID: Final[int] = 55
        self.WERKNEMER_ID: Final[int] = 15


class Tijd:
    __slots__: tuple[str, ...] = ("MAANDEN_MET_NUMMER", "VASTE_FEESTDAGEN")

    def __init__(self) -> None:
        self.MAANDEN_MET_NUMMER: dict[str, int] = {
            "januari": 1, "februari": 2, "maart": 3, "april": 4, "mei": 5,
            "juni": 6, "juli": 7, "augustus": 8, "september": 9, "oktober": 10,
            "november": 11, "december": 12
        }

        self.VASTE_FEESTDAGEN: set[tuple[int, int]] = {(1, 1), (27, 4), (25, 12), (26, 12)}


databasistoegang: ToegangDatabasis = ToegangDatabasis()
toeslagen: Toeslag = Toeslag()
lengten: Lengte = Lengte()
tijden: Tijd = Tijd()
