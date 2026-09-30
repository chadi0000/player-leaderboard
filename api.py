from fastapi import FastAPI, HTTPException
from player import Player

app = FastAPI()

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