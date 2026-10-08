from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models

# Maakt de tabellen aan in players.db als ze nog niet bestaan
Base.metadata.create_all(bind=engine)

app = FastAPI()


class PlayerCreate(BaseModel):
    """Wat een gebruiker moet meesturen om een nieuwe speler aan te maken."""
    username: str = Field(min_length=1, max_length=50)


class PlayerUpdate(BaseModel):
    """Wat een gebruiker kan meesturen om een bestaande speler te wijzigen.
    Beide velden zijn optioneel: je hoeft alleen mee te sturen wat je wilt wijzigen."""
    username: str | None = Field(default=None, min_length=1, max_length=50)
    score: int | None = Field(default=None, ge=0)


@app.get("/")
def root():
    """Test-endpoint om te checken of de API draait."""
    return {"message": "API werkt!"}


@app.get("/players")
def get_players(db: Session = Depends(get_db)):
    """Geeft alle spelers terug als JSON."""
    players = db.query(models.Player).all()
    return [
        {"id": p.id, "username": p.username, "score": p.score}
        for p in players
    ]


@app.get("/players/{id}")
def get_player(id: int, db: Session = Depends(get_db)):
    """Geeft één specifieke speler terug op basis van id."""
    player = db.query(models.Player).filter(models.Player.id == id).first()

    if player is None:
        raise HTTPException(status_code=404, detail="Speler niet gevonden.")

    return {"id": player.id, "username": player.username, "score": player.score}


@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    """Geeft alle spelers terug, gesorteerd op score (hoogste eerst)."""
    players = db.query(models.Player).order_by(models.Player.score.desc()).all()
    return [
        {"id": p.id, "username": p.username, "score": p.score}
        for p in players
    ]


@app.post("/players", status_code=201)
def create_player(player_data: PlayerCreate, db: Session = Depends(get_db)):
    """Maakt een nieuwe speler aan op basis van de meegestuurde username."""
    new_player = models.Player(username=player_data.username, score=0)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)  # haalt het door de database toegekende id op
    return {"id": new_player.id, "username": new_player.username, "score": new_player.score}


@app.patch("/players/{id}")
def update_player(id: int, player_data: PlayerUpdate, db: Session = Depends(get_db)):
    """Wijzigt username en/of score van een bestaande speler."""
    player = db.query(models.Player).filter(models.Player.id == id).first()

    if player is None:
        raise HTTPException(status_code=404, detail="Speler niet gevonden.")

    if player_data.username is not None:
        player.username = player_data.username

    if player_data.score is not None:
        player.score = player_data.score
        # bewaar deze wijziging ook als losse Score-entry (geschiedenis)
        db.add(models.Score(value=player_data.score, player_id=player.id))

    db.commit()
    db.refresh(player)
    return {"id": player.id, "username": player.username, "score": player.score}


@app.delete("/players/{id}", status_code=204)
def delete_player(id: int, db: Session = Depends(get_db)):
    """Verwijdert een speler op basis van id."""
    player = db.query(models.Player).filter(models.Player.id == id).first()

    if player is None:
        raise HTTPException(status_code=404, detail="Speler niet gevonden.")

    db.delete(player)
    db.commit()
    return