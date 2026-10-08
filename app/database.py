from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite-bestand dat in je projectmap wordt aangemaakt
DATABASE_URL = "sqlite:///./players.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # nodig voor SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Geeft een database-sessie, en sluit hem weer af als we klaar zijn."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()