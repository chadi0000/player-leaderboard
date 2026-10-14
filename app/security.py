import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

# Geheime sleutel waarmee tokens worden ondertekend.
# Op school mag deze hier staan, in een echt project zet je hem NIET op GitHub.
SECRET_KEY = os.getenv("SECRET_KEY", "verander-dit-naar-een-lange-willekeurige-tekst")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()  # gebruikt Argon2

# Zegt tegen FastAPI: tokens worden opgehaald via /auth/login
# (dit zorgt ook voor de Authorize-knop in Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    # Leest de token uit het request en zoekt de bijbehorende gebruiker op
    credentials_error = HTTPException(
        status_code=401,
        detail="Ongeldige of verlopen token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except InvalidTokenError:
        raise credentials_error

    if username is None:
        raise credentials_error

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_error

    return user