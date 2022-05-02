from test_config import client, restart_db


# CREATE
# DELETE
# UPDATE
# CHANGE ROLES
# READ PLAYERS
# COUNT PLAYERS
# SEARCH PLAYERS
# COUNT PLAYERS BY SEARCH
# READ PLAYER
# READ PLAYER BY FIREBASE ID
# READ PLAYER TEAMS
# READ PLAYER CAPTAIN TEAMS

def test_1():
    assert True


def test_check_empty():
    response = client.get(
        "/api/players/",
    )
    assert response.status_code == 200
    assert response.json() == []


def test_add():
    response = client.post(
        "/api/players/",
        json={
            "name": "Tygrys",
            "firebase_id": "admin"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'colour': None,
        'description': None,
        'id': 1,
        'name': 'Tygrys',
        'role': 'admin',
    }


def test_check_not_empty():
    response = client.get(
        "/api/players/",
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            'colour': None,
            'description': None,
            'id': 1,
            'name': 'Tygrys',
            'role': 'admin',
        }
    ]

def test_check_empty2(restart_db):
    response = client.get(
        "/api/players/",
    )
    assert response.status_code == 200
    assert response.json() == []
