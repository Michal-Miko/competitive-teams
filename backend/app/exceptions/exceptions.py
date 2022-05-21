from app.database import crud
from fastapi import HTTPException, status


def check_for_team_existence(db, team_id):
    if crud.get_team(db, team_id=team_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team {} not found".format(team_id))


def check_for_player_existence(db, player_id):
    if crud.get_player(db, player_id=player_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player {} not found".format(player_id))


def check_for_match_existence(db, match_id):
    if crud.get_match(db, match_id=match_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match {} not found".format(match_id))


def check_for_tournament_existence(db, tournament_id):
    if crud.get_tournament(db, tournament_id=tournament_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match {} not found".format(tournament_id))
