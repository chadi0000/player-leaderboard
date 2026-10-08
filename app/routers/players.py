from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/players", tags=["players"])


@router.get("", response_model=list[schemas.PlayerResponse])
def get_players(db: Session = Depends(get_db)):
    return db.query(models.Player).all()


@router.get("/{id}", response_model=schemas.PlayerResponse)
def get_player(id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == id).first()

    if player is None:
        raise HTTPException(status_code=404, detail="Speler niet gevonden.")

    return player


@router.post("", status_code=201, response_model=schemas.PlayerResponse)
def create_player(player_data: schemas.PlayerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Player).filter(models.Player.username == player_data.username).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="Username bestaat al.")

    new_player = models.Player(username=player_data.username, score=0)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player


@router.patch("/{id}", response_model=schemas.PlayerResponse)
def update_player(id: int, player_data: schemas.PlayerUpdate, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == id).first()

    if player is None:
        raise HTTPException(status_code=404, detail="Speler niet gevonden.")

    if player_data.username is not None:
        taken = db.query(models.Player).filter(
            models.Player.username == player_data.username,
            models.Player.id != id,
        ).first()
        if taken is not None:
            raise HTTPException(status_code=409, detail="Username bestaat al.")
        player.username = player_data.username

    if player_data.score is not None:
        player.score = player_data.score
        # bewaar de wijziging ook als losse Score-entry (geschiedenis)
        db.add(models.Score(value=player_data.score, player_id=player.id))

    db.commit()
    db.refresh(player)
    return player


@router.delete("/{id}", status_code=204)
def delete_player(id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == id).first()

    if player is None:
        raise HTTPException(status_code=404, detail="Speler niet gevonden.")

    db.delete(player)
    db.commit()