from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    # Tabel met accounts waarmee je kunt inloggen
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # nooit het wachtwoord zelf opslaan

    players = relationship("Player", back_populates="owner")


class Player(Base):
    # Tabel met spelers
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    score = Column(Integer, default=0)  # huidige score, voor het leaderboard

    # Van welke gebruiker (account) is deze speler?
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="players")

    # Eén speler kan meerdere Score-entries hebben (geschiedenis)
    scores = relationship("Score", back_populates="player")


class Score(Base):
    # Tabel met losse score-toevoegingen, gekoppeld aan een speler
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="scores")