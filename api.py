from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from player import Player

app = FastAPI()


class PlayerCreate(BaseModel):
    """Wat een gebruiker moet meesturen om een nieuwe speler aan te maken."""
    username: str = Field(min_length=1, max_length=50)


class PlayerUpdate(BaseModel):
    """Wat een gebruiker kan meesturen om een bestaande speler te wijzigen.
    Beide velden zijn optioneel: je hoeft alleen mee te sturen wat je wilt wijzigen."""
    username: str | None = Field(default=None, min_length=1, max_length=50)
    score: int | None = Field(default=None, ge=0)

# Voorlopig wat testdata, zodat er iets is om op te testen
players = [
    Player(1, "anna", 50),
    Player(2, "bram", 80),
    Player(3, "chris", 20),
]


@app.get("/")
def root():
    """Test-endpoint om te checken of de API draait."""
    return {"message": "API werkt!"}


@app.get("/players")
def get_players():
    """Geeft alle spelers terug als JSON."""
    return [
        {"id": p.id, "username": p.username, "score": p.score}
        for p in players
    ]


@app.get("/players/{id}")
def get_player(id: int):
    """Geeft één specifieke speler terug op basis van id."""
    for p in players:
        if p.id == id:
            return {"id": p.id, "username": p.username, "score": p.score}

    raise HTTPException(status_code=404, detail="Speler niet gevonden.")


@app.get("/leaderboard")
def get_leaderboard():
    """Geeft alle spelers terug, gesorteerd op score (hoogste eerst)."""
    sorted_players = sorted(players, key=lambda p: p.score, reverse=True)
    return [
        {"id": p.id, "username": p.username, "score": p.score}
        for p in sorted_players
    ]


@app.post("/players", status_code=201)
def create_player(player_data: PlayerCreate):
    """Maakt een nieuwe speler aan op basis van de meegestuurde username."""
    new_id = len(players) + 1
    new_player = Player(new_id, player_data.username)
    players.append(new_player)
    return {"id": new_player.id, "username": new_player.username, "score": new_player.score}


@app.patch("/players/{id}")
def update_player(id: int, player_data: PlayerUpdate):
    """Wijzigt username en/of score van een bestaande speler."""
    for p in players:
        if p.id == id:
            if player_data.username is not None:
                p.username = player_data.username
            if player_data.score is not None:
                p.score = player_data.score
            return {"id": p.id, "username": p.username, "score": p.score}

    raise HTTPException(status_code=404, detail="Speler niet gevonden.")


@app.delete("/players/{id}", status_code=204)
def delete_player(id: int):
    """Verwijdert een speler op basis van id."""
    for p in players:
        if p.id == id:
            players.remove(p)
            return

    raise HTTPException(status_code=404, detail="Speler niet gevonden.")