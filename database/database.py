from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()
Engine = create_engine(os.getenv('DATABASE_URL'))
Session_local = sessionmaker(
    bind=Engine, autoflush=False, autocommit=False)

Base = declarative_base()


@contextmanager
def get_db():
    db: Session = Session_local()
    try:
        yield db
        db.commit()
        db.close()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_db_dependency():
    with get_db() as db:
        yield db
