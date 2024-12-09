from typing import Final


class Url:
    __slots__: tuple[str, ...] = ("KLOKKERSERVER",)

    def __init__(self) -> None:
        self.KLOKKERSERVER: Final[str] = "http://localhost:8000"


class Tekst:
    __slots__: tuple[str, ...] = ("START",)

    def __init__(self) -> None:
        self.START: Final[str] = (
            """
$$\\       $$\\           $$\\       $$\\                           
$$ |      $$ |          $$ |      $$ |                          
$$ |  $$\\ $$ | $$$$$$\\  $$ |  $$\\ $$ |  $$\\  $$$$$$\\   $$$$$$\\  
$$ | $$  |$$ |$$  __$$\\ $$ | $$  |$$ | $$  |$$  __$$\\ $$  __$$\\ 
$$$$$$  / $$ |$$ /  $$ |$$$$$$  / $$$$$$  / $$$$$$$$ |$$ |  \\__|
$$  _$$<  $$ |$$ |  $$ |$$  _$$<  $$  _$$<  $$   ____|$$ |      
$$ | \\$$\\ $$ |\\$$$$$$  |$$ | \\$$\\ $$ | \\$$\\ \\$$$$$$$\\ $$ |      
\\__|  \\__|\\__| \\______/ \\__|  \\__|\\__|  \\__| \\_______|\\__|
"""
        )


urls: Url = Url()
teksten: Tekst = Tekst()
