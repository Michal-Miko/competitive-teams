from test_config import client, restart_db, mock_permissions


HEADER_WITH_FIREBASE_TOKEN = {
    "firebase-token": "admin"
}

PLAYER_CREATE_SCHEMA = {
    "name": "Tygrys",
    "description": "DESC",
    "colour": "#ffffff",
    "firebase_token": "admin",
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

TOURNAMENT_CREATE_SCHEMA = {
    "name": "Grand Tournament",
    "description": None,
    "tournament_type": "round-robin",
    "swiss_rounds": None,
    "start_time": None,
    "teams_ids": [1, 2],
}

MATCH_RESULT_SCHEMA = {
    "score1": 21,
    "score2": 37
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
        headers=HEADER_WITH_FIREBASE_TOKEN
    )
    assert response.status_code == 200

    response = client.post(
        "/api/teams/",
        json=TEAM2_CREATE_SCHEMA,
        headers=HEADER_WITH_FIREBASE_TOKEN
    )
    assert response.status_code == 200


def test_create_tournament():
    response = client.post(
        "/api/tournaments/",
        headers=HEADER_WITH_FIREBASE_TOKEN,
        json=TOURNAMENT_CREATE_SCHEMA
    )
    assert response.status_code == 200
    assert len(response.json()["matches"]) == 1


def test_update_tournament_match():
    response = client.patch(
        "/api/tournaments/1/input_match_result",
        headers=HEADER_WITH_FIREBASE_TOKEN,
        json=MATCH_RESULT_SCHEMA,
        params={
            "match_id": 1
        }
    )
    assert response.status_code == 200


def test_read_tournament_scoreboard():
    response = client.get(
        "/api/tournament/1/scoreboard",
        headers=HEADER_WITH_FIREBASE_TOKEN,
    )
    assert response.status_code == 200
    results = response.json()["results"]
    assert results[1]["match_points"] == 21
    assert results[1]["tournament_points"] == 0.0
    assert results[0]["match_points"] == 37
    assert results[0]["tournament_points"] == 1.0
