

class Serverconfiguratie:
    __slots__: tuple[str, ...] = ("TOEGESTANE_IP_ADRESSEN", "POORT", "AANTAL_THREADS", "RELOAD")

    def __init__(self) -> None:
        self.TOEGESTANE_IP_ADRESSEN: str = "0.0.0.0"
        self.POORT: int = 8000
        self.AANTAL_THREADS: int = 1
        self.RELOAD: bool = False

    def __str__(self) -> str:
        return (f"ServerConfiguration(ALLOW_IP_ADDRESSES={self.TOEGESTANE_IP_ADRESSEN},"
                f" PORT={self.POORT}, THREAD_COUNT={self.AANTAL_THREADS}, RELOAD={self.RELOAD})")


class Configuratiefout(Exception):
    def __str__(self) -> str:
        return (
            f"\n{'-' * 115}\nConfiguratiefout: geef de volgende vlaggen:\n"
            "1. --host <host_ip_address>\n"
            "2. --port <port number>\n"
            "3. *optioneel*: --reload\n"
            "4. *optioneel*: --workers <thread count>\n"
            "\nOntwikkeling: python3.12 server.py --host 127.0.0.1 --port 8000 --workers 1 --reload\n"
            "Productie: python3.12 server.py --host 0.0.0.0 --port <IP address server> --workers <X>\n\n"
        )


def geef_serverconfiguratie(argv: list[str]) -> Serverconfiguratie:
    """
    Construeert de servers configuratie op basis van commandlineargumenten.
    """
    if len(argv) == 1:
        raise Configuratiefout()

    serverconfiguratie: Serverconfiguratie = Serverconfiguratie()

    for i, command_line_argument in enumerate(argv):
        if command_line_argument == "--host":
            serverconfiguratie.TOEGESTANE_IP_ADRESSEN = argv[i + 1]

            continue

        if command_line_argument == "--port":
            serverconfiguratie.POORT = int(argv[i + 1])

            continue

        if command_line_argument == "--reload":
            serverconfiguratie.RELOAD = True

            continue

        if command_line_argument == "--workers":
            serverconfiguratie.AANTAL_THREADS = int(argv[i + 1])

            continue

    return serverconfiguratie
