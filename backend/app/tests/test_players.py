from test_config import client, restart_db


# DELETE
# UPDATE

PLAYER_CREATE_SCHEMA = {
    "name": "Tygrys",
    "description": "DESC",
    "colour": "#ffffff",
    "firebase_id": "admin",
}

HEADER_WITH_FIREBASE_ID = {
    "firebase-id": "admin"
}

PLAYER_SCHEMA = {
    "id": 1,
    "role": "admin",
    "name": "Tygrys",
    "description": "DESC",
    "colour": "#ffffff",
}


def test_no_players_in_db(restart_db):
    response = client.get(
        "/api/players/",
    )
    assert response.status_code == 200
    assert response.json() == []


def test_create_player():
    response = client.post(
        "/api/players/",
        json=PLAYER_CREATE_SCHEMA
    )
    assert response.status_code == 200
    assert response.json() == PLAYER_SCHEMA


def test_read_players():
    response = client.get(
        "/api/players/",
    )
    assert response.status_code == 200
    assert response.json() == [
        PLAYER_SCHEMA
    ]


def test_read_players():
    response = client.get(
        "/api/players/",
    )
    assert response.status_code == 200
    assert response.json() == [
        PLAYER_SCHEMA
    ]


def test_read_player_by_id():
    response = client.get(
        "/api/players/1",
    )
    assert response.status_code == 200
    assert response.json() == PLAYER_SCHEMA


def test_read_player_by_firebase_id():
    response = client.get(
        "/api/players/firebase_id/admin",
        headers=HEADER_WITH_FIREBASE_ID
    )
    assert response.status_code == 200
    assert response.json() == PLAYER_SCHEMA
