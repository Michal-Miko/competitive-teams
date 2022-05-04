from test_config import client, restart_db


HEADER_WITH_FIREBASE_ID = {
    "firebase-id": "admin"
}

HEADER_WITH_FIREBASE_ID_AND_TEAMS = {
    "firebase-id": "admin",
    "team1-id": "1",
    "team2-id": "2"
}

PLAYER_CREATE_SCHEMA = {
    "name": "Tygrys",
    "description": "DESC",
    "colour": "#ffffff",
    "firebase_id": "admin",
}

TEAM1_CREATE_SCHEMA = {
    "name": "A",
    "description": "DESC",
    "colour": "#7f7f7f",
}

TEAM2_CREATE_SCHEMA = {
    "name": "B",
    "description": "DESC",
    "colour": "#7f7f7f",
}

MATCH_CREATE_SCHEMA = {
    "name": "Meczyk",
    "description": None,
    "start_time": None,
    "finished": False,
    "score1": 0,
    "score2": 0,
}

MATCH_UPDATE_SCHEMA = {
    "name": "Meczyk",
    "description": None,
    "start_time": None,
    "finished": True,
    "score1": 21,
    "score2": 37,
}

MATCH_SCHEMA = {
    "id": 1,
    "name": "Meczyk",
    "description": None,
    "start_time": None,
    "finished": False,
    "score1": 0,
    "score2": 0,
    "team1": {
        "id": 1,
        "captain_id": None,
        "players": [],
        "name": "A",
        "description": "DESC",
        "colour": "#7f7f7f",
    },
    "team2": {
        "id": 2,
        "captain_id": None,
        "players": [],
        "name": "B",
        "description": "DESC",
        "colour": "#7f7f7f",
    },
    "team1_id": 1,
    "team2_id": 2,
    "tournament_id": None,
    "tournament_place": None,
}

UPDATED_TEAM_SCHEMA = {
    "id": 1,
    "name": "Meczyk",
    "description": None,
    "start_time": None,
    "finished": True,
    "score1": 21,
    "score2": 37,
    "team1": {
        "id": 1,
        "captain_id": None,
        "players": [],
        "name": "A",
        "description": "DESC",
        "colour": "#7f7f7f",
    },
    "team2": {
        "id": 2,
        "captain_id": None,
        "players": [],
        "name": "B",
        "description": "DESC",
        "colour": "#7f7f7f",
    },
    "team1_id": 1,
    "team2_id": 2,
    "tournament_id": None,
    "tournament_place": None,
}


def test_init(restart_db):
    response = client.post(
        "/api/players/",
        json=PLAYER_CREATE_SCHEMA
    )
    assert response.status_code == 200

    response = client.post(
        "/api/teams/",
        json=TEAM1_CREATE_SCHEMA,
        headers=HEADER_WITH_FIREBASE_ID
    )
    assert response.status_code == 200

    response = client.post(
        "/api/teams/",
        json=TEAM2_CREATE_SCHEMA,
        headers=HEADER_WITH_FIREBASE_ID
    )
    assert response.status_code == 200


def test_create_match():
    response = client.post(
        "/api/matches/",
        headers=HEADER_WITH_FIREBASE_ID_AND_TEAMS,
        json=MATCH_CREATE_SCHEMA
    )
    assert response.status_code == 200
    assert response.json() == MATCH_SCHEMA


def test_read_matches():
    response = client.get(
        "/api/matches/",
    )
    assert response.status_code == 200
    assert response.json() == [
        MATCH_SCHEMA
    ]


def test_update_team():
    response = client.patch(
        "/api/matches/1",
        headers=HEADER_WITH_FIREBASE_ID,
        json=MATCH_UPDATE_SCHEMA
    )
    assert response.status_code == 200

    response = client.get(
        "/api/matches/1",
        headers=HEADER_WITH_FIREBASE_ID,
    )
    assert response.status_code == 200
    assert response.json() == UPDATED_TEAM_SCHEMA
