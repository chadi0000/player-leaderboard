from fastapi import FastAPI

from app import models  # zorgt dat de tabellen bekend zijn bij SQLAlchemy
from app.database import Base, engine
from app.routers import auth, players, leaderboard

# Maakt de tabellen aan in players.db als ze nog niet bestaan
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(players.router)
app.include_router(leaderboard.router)


@app.get("/")
def root():
    return {"message": "API werkt!"}