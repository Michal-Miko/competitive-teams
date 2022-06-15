from test_config import client, restart_db, mock_permissions


PLAYER_CREATE_SCHEMA = {
    "name": "Tygrys",
    "description": "DESC",
    "colour": "#ffffff",
    "firebase_token": "admin",
}

HACKER_CREATE_SCHEMA = {
    "name": "Hacker",
    "description": "DESC",
    "colour": "#ffffff",
    "firebase_token": "hacker",
}

TEAM_CREATE_SCHEMA_1 = {
    "name": "Szybcy",
}

TEAM_CREATE_SCHEMA_2 = {
    "name": "Wspaniali",
}

USER_WITH_PERMISSION = {
    "firebase-token": "admin"
}

USER_WITHOUT_PERMISSION = {
    "firebase-token": "hacker"
}


def test_init(restart_db):
    response = client.post(
        "/api/players/",
        json=PLAYER_CREATE_SCHEMA
    )
    assert response.status_code == 200

    response = client.post(
        "/api/players/",
        json=HACKER_CREATE_SCHEMA
    )
    assert response.status_code == 200

    response = client.patch(
        "/api/change_role/2",
        headers={
            "player-role": "guest",
            "firebase_token": "admin"
        }
    )
    assert response.status_code == 200


def test_use_not_permitted_endpoint():
    response = client.post(
        "/api/teams/",
        headers=USER_WITHOUT_PERMISSION,
        json=TEAM_CREATE_SCHEMA_1
    )
    assert response.status_code == 403


def test_use_permitted_endpoint():
    response = client.post(
        "/api/teams/",
        headers=USER_WITH_PERMISSION,
        json=TEAM_CREATE_SCHEMA_2
    )
    assert response.status_code == 200
