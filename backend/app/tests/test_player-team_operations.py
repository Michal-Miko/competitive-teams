from test_config import client, restart_db


HEADER_WITH_FIREBASE_ID = {
    "firebase-id": "admin"
}

PLAYER_CREATE_SCHEMA = {
    "name": "Tygrys",
    "description": "DESC",
    "colour": "#ffffff",
    "firebase_id": "admin",
}

TEAM_CREATE_SCHEMA = {
    "name": "Szybcy",
    "description": "DESC",
    "colour": "#7f7f7f",
}


TEAM_SCHEMA = {
    "id": 1,
    "captain_id": None,
    "players": [],
    "name": "Szybcy",
    "description": "DESC",
    "colour": "#7f7f7f",
}


def test_init(restart_db):
    response = client.post(
        "/api/players/",
        json=PLAYER_CREATE_SCHEMA
    )
    assert response.status_code == 200

    response = client.post(
        "/api/teams/",
        headers=HEADER_WITH_FIREBASE_ID,
        json=TEAM_CREATE_SCHEMA
    )
    assert response.status_code == 200


def test_link_player_to_team():
    response = client.put(
        "/api/players/1",
        params={
            "player_id": 1,
        },
        headers=HEADER_WITH_FIREBASE_ID,
    )
    assert response.status_code == 200

    response = client.get(
        "/api/teams/",
    )
    assert response.status_code == 200
    assert response.json()[0]["players"] != []


def test_unlink_player_from_team():
    response = client.put(
        "/api/unlink_player/1",
        params={
            "player_id": 1,
        },
        headers=HEADER_WITH_FIREBASE_ID,
        json=PLAYER_CREATE_SCHEMA
    )
    assert response.status_code == 200

    response = client.get(
        "/api/teams/",
    )
    assert response.status_code == 200
    assert response.json() == [
        TEAM_SCHEMA
    ]
