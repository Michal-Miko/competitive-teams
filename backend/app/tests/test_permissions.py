from test_config import client, restart_db


PLAYER_CREATE_SCHEMA = {
    "name": "Tygrys",
    "description": "DESC",
    "colour": "#ffffff",
    "firebase_id": "admin",
}

HACKER_CREATE_SCHEMA = {
    "name": "Hacker",
    "description": "DESC",
    "colour": "#ffffff",
    "firebase_id": "hacker",
}

USER_WITH_PERMISSION = {
    "firebase-id": "admin"
}

USER_WITHOUT_PERMISSION = {
    "firebase-id": "hacker"
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
            "firebase-id": "admin"
        }
    )
    assert response.status_code == 200


def test_use_permitted_endpoint():
    response = client.get(
        "/api/players/firebase_id/admin",
        headers=USER_WITH_PERMISSION
    )
    assert response.status_code == 200


def test_use_not_permitted_endpoint():
    response = client.get(
        "/api/players/firebase_id/admin",
        headers=USER_WITHOUT_PERMISSION
    )
    assert response.status_code == 403
