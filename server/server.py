import sys
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server_.routers.dienst import dienst
from server_.routers.werknemer import werknemer
from server_.databasis.databasis import Base, engine
from server_.ondersteuning.run import geef_serverconfiguratie, Serverconfiguratie


Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(werknemer.router)
app.include_router(dienst.router)


@app.get('/')
async def root() -> dict[str, str]:
    """
    The root address / home page of the server.
    """
    return {"klokker": "welkom!"}


def main() -> None:
    serverconfiguratie: Serverconfiguratie = geef_serverconfiguratie(sys.argv)

    uvicorn.run(
        "server:app",
        host=serverconfiguratie.TOEGESTANE_IP_ADRESSEN,
        port=serverconfiguratie.POORT,
        reload=serverconfiguratie.RELOAD,
        workers=serverconfiguratie.AANTAL_THREADS
    )


if __name__ == "__main__":
    main()
