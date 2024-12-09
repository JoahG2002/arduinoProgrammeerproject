import os
import sys


def lees_env_variabelen() -> dict[str, str]:
    """
    Lees omgevingsvariabelen uit een .env-bestand.
    """
    pad_env_bestand: str = f"{os.getcwd().replace("\\", '/')}/.env"

    if os.path.exists(pad_env_bestand):
        omgevingsvariabelen: dict[str, str] = {}

        with open(pad_env_bestand, 'r') as env_file:
            env_bestandregels: list[str] = env_file.read().splitlines()

            for regel in env_bestandregels:
                variabele, waarde = regel.split('=', maxsplit=1)
                omgevingsvariabelen[variabele] = waarde

            return omgevingsvariabelen
    else:
        sys.stdout.write("\n.env file not found.\n\n")

        return {}
