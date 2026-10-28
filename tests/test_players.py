from tests.conftest import auth_headers


def test_get_players_is_public(client):
    assert client.get("/players").status_code == 200


def test_leaderboard_is_public(client):
    assert client.get("/leaderboard").status_code == 200


def test_post_player_without_login_gives_401(client):
    r = client.post("/players", json={"username": "speler1", "score": 100})
    assert r.status_code == 401


def test_post_player_sets_owner(client):
    h = auth_headers(client, "chadi")
    me = client.get("/auth/me", headers=h).json()
    r = client.post("/players", json={"username": "speler1", "score": 100}, headers=h)
    assert r.status_code == 201
    assert r.json()["owner_id"] == me["id"]


def test_get_nonexistent_player_gives_404(client):
    assert client.get("/players/9999").status_code == 404


def test_patch_nonexistent_player_gives_404(client):
    h = auth_headers(client, "chadi")
    r = client.patch("/players/9999", json={"score": 5}, headers=h)
    assert r.status_code == 404


def test_other_user_gets_403_on_patch_and_delete(client):
    h1 = auth_headers(client, "chadi")
    h2 = auth_headers(client, "anna2")
    pid = client.post("/players", json={"username": "speler1", "score": 1}, headers=h1).json()["id"]
    assert client.patch(f"/players/{pid}", json={"score": 999}, headers=h2).status_code == 403
    assert client.delete(f"/players/{pid}", headers=h2).status_code == 403


def test_owner_can_delete(client):
    h = auth_headers(client, "chadi")
    pid = client.post("/players", json={"username": "speler1", "score": 1}, headers=h).json()["id"]
    assert client.delete(f"/players/{pid}", headers=h).status_code == 204
    assert client.get(f"/players/{pid}").status_code == 404