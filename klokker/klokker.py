import sys
import time

from app.arduino.manager import Arduinomanager
from app.verzoek.dienst.dienst import verzoek_dienstregistratie
from app.verzoek.dienst.ondersteuning import bereken_uren_en_minuten_gewerkt
from app.ondersteuning.constant import teksten


def main() -> None:
    arduinomanager: Arduinomanager = Arduinomanager()

    sys.stdout.write(teksten.START)
    sys.stdout.write(f"\nVerbinding met Arduino  (poort: {arduinomanager.ARDUINOPOORT}) gestart.\n")

    try:
        while True:
            data_verstuurd_door_arduino: str = arduinomanager.geef_uitvoer_arduino()

            if not data_verstuurd_door_arduino or not data_verstuurd_door_arduino.startswith('$'):
                time.sleep(0.3)

                continue

            sys.stdout.write(f"{'-' * 52}\nArduino data: \"{data_verstuurd_door_arduino}\"\n")

            dienstdata: list[str] = data_verstuurd_door_arduino[1:].split(',')
            werknemer_id: str = dienstdata[0]
            start_dienst: float = float(dienstdata[1])
            eind_dienst: float = float(dienstdata[2])

            uren_gewerkt, overige_minuten = bereken_uren_en_minuten_gewerkt(start_dienst, eind_dienst)

            if (uren_gewerkt < 0) and (overige_minuten < 15):
                arduinomanager.schrijf_naar_arduino(
                    "Dienst te kort."
                )

                continue

            euros_verdiend, succescode = verzoek_dienstregistratie(werknemer_id, start_dienst, eind_dienst)

            if succescode == 0:
                arduinomanager.schrijf_naar_arduino(
                    f"{uren_gewerkt} h {overige_minuten} min -> {euros_verdiend} EUR"
                )
            else:
                arduinomanager.schrijf_naar_arduino("-1")

    except KeyboardInterrupt:
        sys.stdout.write(f"\nVerbinding met Arduino (poort: {arduinomanager.ARDUINOPOORT}) is verbroken.\n")

    finally:
        arduinomanager.verbreek_arduinoverbinding()


if __name__ == "__main__":
    main()
