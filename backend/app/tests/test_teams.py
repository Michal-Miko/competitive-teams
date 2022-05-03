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

TEAM_UPDATE_SCHEMA = {
    "description": "Szybcy jak wiatr.",
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

UPDATED_TEAM_SCHEMA = {
    "id": 1,
    "captain_id": None,
    "players": [],
    "name": "Szybcy",
    "description": "Szybcy jak wiatr.",
    "colour": "#7f7f7f",
}


def test_init(restart_db):
    response = client.post(
        "/api/players/",
        json=PLAYER_CREATE_SCHEMA
    )
    assert response.status_code == 200


def test_create_team():
    response = client.post(
        "/api/teams/",
        headers=HEADER_WITH_FIREBASE_ID,
        json=TEAM_CREATE_SCHEMA
    )
    assert response.status_code == 200
    assert response.json() == TEAM_SCHEMA


def test_read_teams():
    response = client.get(
        "/api/teams/",
    )
    assert response.status_code == 200
    assert response.json() == [
        TEAM_SCHEMA
    ]


def test_update_team():
    response = client.patch(
        "/api/teams/1",
        headers=HEADER_WITH_FIREBASE_ID,
        json=TEAM_UPDATE_SCHEMA
    )
    assert response.status_code == 200

    response = client.get(
        "/api/teams/1",
    )
    assert response.status_code == 200
    assert response.json() == UPDATED_TEAM_SCHEMA


def test_remove_player():
    response = client.delete(
        "/api/teams/1",
        headers=HEADER_WITH_FIREBASE_ID,
    )
    assert response.status_code == 200

    response = client.get(
        "/api/teams/",
    )
    assert response.status_code == 200
    assert response.json() == []
