from typing import Final
from serial import Serial


class Arduinomanager:
    __slots__: tuple[str, ...] = ("ARDUINOPOORT", "BAUDSNELHEID", "LUISTER_TIMEOUT_SECONDEN", "_verbinding")

    def __init__(self) -> None:
        self.ARDUINOPOORT: Final[str] = "COM5"
        self.BAUDSNELHEID: Final[int] = 9600
        self.LUISTER_TIMEOUT_SECONDEN: Final[int] = 1

        self._verbinding: Serial = Serial(
            self.ARDUINOPOORT,
            self.BAUDSNELHEID,
            timeout=self.LUISTER_TIMEOUT_SECONDEN
        )

    def geef_uitvoer_arduino(self) -> str:
        """
        Geeft de uitvoer van de verbonden Arduino terug als string.
        """
        return self._verbinding.readline().decode("ascii").strip()

    def schrijf_naar_arduino(self, string: str) -> None:
        """
        Schrijft een string naar de verbonden Arduino als bytes.
        """
        self._verbinding.write(string.encode("ascii"))

    def verbreek_arduinoverbinding(self) -> None:
        """
        Verbreekt de verbinding met de Arduino.
        """
        self._verbinding.close()
