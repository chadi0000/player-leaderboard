from tests.conftest import auth_headers


def test_register_success(client):
    r = client.post("/auth/register", json={"username": "chadi", "password": "Welkom1234"})
    assert r.status_code == 201
    assert "password" not in r.json()
    assert "hashed_password" not in r.json()


def test_register_duplicate_gives_409(client):
    body = {"username": "chadi", "password": "Welkom1234"}
    client.post("/auth/register", json=body)
    assert client.post("/auth/register", json=body).status_code == 409


def test_register_short_password_gives_422(client):
    r = client.post("/auth/register", json={"username": "x", "password": "abc"})
    assert r.status_code == 422


def test_register_missing_field_gives_422(client):
    assert client.post("/auth/register", json={"username": "x"}).status_code == 422


def test_login_wrong_password_gives_401(client):
    client.post("/auth/register", json={"username": "chadi", "password": "Welkom1234"})
    r = client.post("/auth/login", data={"username": "chadi", "password": "fout12345"})
    assert r.status_code == 401


def test_me_without_token_gives_401(client):
    assert client.get("/auth/me").status_code == 401


def test_me_with_invalid_token_gives_401(client):
    r = client.get("/auth/me", headers={"Authorization": "Bearer onzin"})
    assert r.status_code == 401


def test_me_with_token(client):
    h = auth_headers(client, "chadi")
    r = client.get("/auth/me", headers=h)
    assert r.status_code == 200
    assert r.json()["username"] == "chadi"