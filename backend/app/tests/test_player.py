from test_config import client, restart_db


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
