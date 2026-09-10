class Player:
    """Representeert een speler met een id, username en score."""

    def __init__(self, id, username, score=0):
        self.id = id
        self.username = username
        self.score = score

    def __str__(self):
        return f"[{self.id}] {self.username} - score: {self.score}"