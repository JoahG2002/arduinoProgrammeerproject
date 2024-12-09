from typing import Any
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from ..ondersteuning.constant import databasistoegang


engine: Engine = create_engine(databasistoegang.SQLALCHEMY_DATABASISLINK)
SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: Any = declarative_base()


def geef_databasis() -> Session:
    """
    Geeft een databasissessie terug.
    """
    databasis: Session = SessionLocal()

    try:
        yield databasis

    finally:
        databasis.close()
