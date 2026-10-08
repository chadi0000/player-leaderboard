from pydantic import BaseModel, ConfigDict, Field


# Wat een gebruiker moet meesturen om een speler aan te maken
class PlayerCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)


# Wat een gebruiker kan meesturen om een speler te wijzigen (alles optioneel)
class PlayerUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    score: int | None = Field(default=None, ge=0)


# Wat de API teruggeeft als er een speler getoond wordt
class PlayerResponse(BaseModel):
    id: int
    username: str
    score: int

    model_config = ConfigDict(from_attributes=True)