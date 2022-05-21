from typing import List
from fastapi import Depends, FastAPI, HTTPException, Header, status
from sqlalchemy.orm import Session
from app.database import crud
from app.database.database import Base, engine
from app.schemas import schemas
from app.database.database import SessionLocal
from app.firebase import firebase
from app.permissions import permissions
from app.exceptions import exceptions
from app.utils.cors import add_cors


Base.metadata.create_all(bind=engine)
app = FastAPI()
add_cors(app)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Teams
@app.post("/api/teams/", response_model=schemas.Team)
def create_team(
    team: schemas.TeamCreate,
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "moderator"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    db_team_name = crud.get_team_by_name(db=db, name=team.name)
    if db_team_name is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name already used")
    return crud.create_team(db=db, team=team)


@app.delete("/api/teams/{team_id}")
def delete_team(
    team_id: int, firebase_id: str = Header(None), db: Session = Depends(get_db)
):
    clearance = "moderator"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_team_existence(db=db, team_id=team_id)
    crud.delete_team(db, team_id)


@app.patch("/api/teams/{team_id}")
def update_team(
    team_id: int,
    team: schemas.TeamUpdate,
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "moderator"
    access = permissions.is_accessible(
        db=db, firebase_id=firebase_id, clearance=clearance
    )

    def update():
        team_check = crud.get_team_by_name(db, name=team.name)
        old_team = crud.get_team(db, team_id=team_id)
        if team_check is not None and old_team.name is not team_check.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name already used")
        crud.update_team(db, team_id=team_id, team=team)
    
    if access:
        exceptions.check_for_team_existence(db=db, team_id=team_id)
        update()
    else:
        exceptions.check_for_team_existence(db=db, team_id=team_id)
        db_player = crud.get_player_by_firebase_id(db, firebase_id=firebase_id)
        if db_player is None:
            permissions.permission_denied(clearance)
        if crud.is_player_captain(db, player_id=db_player.id, team_id=team_id):
            update()
        else:
            permissions.permission_denied(clearance)


@app.get("/api/teams/{team_id}", response_model=schemas.Team)
def read_team(
    team_id: int, firebase_id: str = Header(None), db: Session = Depends(get_db)
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_team_existence(db=db, team_id=team_id)
    return crud.get_team(db, team_id=team_id)


@app.get("/api/teams/", response_model=List[schemas.Team])
def read_teams(
    firebase_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.get_teams(db, skip=skip, limit=limit)


@app.get("/api/teams_count/", response_model=int)
def count_teams(
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.count_teams(db)


@app.get("/api/teams/search/", response_model=List[schemas.Team])
def search_teams(
    firebase_id: str = Header(None),
    name: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.search_teams_by_name(db, name=name, skip=skip, limit=limit)


@app.get("/api/teams_count_by_search/", response_model=int)
def count_teams_by_search(
    firebase_id: str = Header(None),
    name: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.count_teams_by_search(db, name)


# Players
@app.post("/api/players/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    if crud.get_player_by_name(db, name=player.name) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name already used")
    if crud.get_player_by_firebase_id(db, firebase_id=player.firebase_id) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Firebase_id already used")
    return crud.create_player(db=db, player=player)


@app.delete("/api/players/{player_id}")
def delete_player(
    player_id: int, firebase_id: str = Header(None), db: Session = Depends(get_db)
):
    clearance = "admin"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_player_existence(db=db, player_id=player_id)
    crud.delete_player(db, player_id)


@app.patch("/api/players/{player_id}")
def update_player(
    player_id: int,
    player: schemas.PlayerUpdate,
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "admin"
    access = permissions.is_accessible(
        db=db, firebase_id=firebase_id, clearance=clearance
    )
    def update():
        exceptions.check_for_player_existence(db=db, player_id=player_id)
        player_check = crud.get_player_by_name(db, name=player.name)
        old_player = crud.get_player(db, player_id=player_id)
        if player_check is not None and old_player.name is not player_check.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name already used")
        crud.update_player(db, player_id=player_id, player=player)

    if access:
        update()
    else:
        db_player = crud.get_player(db, player_id=player_id)
        db_user = crud.get_player_by_firebase_id(db, firebase_id=firebase_id)
        if db_user is None:
            permissions.permission_denied(clearance)
        if db_player is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
        if db_user.id == db_player.id:
            update()
        else:
            permissions.permission_denied(clearance)


@app.patch("/api/change_role/{player_id}")
def change_role(
    player_id: int,
    player_role: str = Header(None),
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "admin"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_player_existence(db=db, player_id=player_id)
    if player_role not in ["admin", "moderator", "player", "guest"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role: " + str(player_role)
        )
    crud.change_role(db, player_id=player_id, player_role=player_role)


@app.get("/api/players/", response_model=List[schemas.Player])
def read_players(
    firebase_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.get_players(db, skip=skip, limit=limit)


@app.get("/api/players_count/", response_model=int)
def count_players(
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.count_players(db)


@app.get("/api/players/search/", response_model=List[schemas.Player])
def search_players(
    firebase_id: str = Header(None),
    name: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.search_players_by_name(db, name=name, skip=skip, limit=limit)


@app.get("/api/players_count_by_search/", response_model=int)
def count_players_by_search(
    firebase_id: str = Header(None),
    name: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.count_players_by_search(db, name)


@app.get("/api/players/{player_id}", response_model=schemas.Player)
def read_player(
    player_id: int, firebase_id: str = Header(None), db: Session = Depends(get_db)
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_player_existence(db=db, player_id=player_id)
    return crud.get_player(db, player_id=player_id)


@app.get("/api/players/firebase_id/{wanted_firebase_id}", response_model=schemas.Player)
def read_player_by_firebase_id(
    wanted_firebase_id: str,
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "player"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    db_player = crud.get_player_by_firebase_id(db, firebase_id=wanted_firebase_id)
    if db_player is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return db_player


@app.get("/api/players/teams/{player_id}", response_model=List[schemas.Team])
def read_player_teams(
    player_id: int,
    firebase_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_player_existence(db=db, player_id=player_id)
    return crud.get_player_teams(db, player_id=player_id, skip=skip, limit=limit)


@app.get("/api/captain/teams/{player_id}", response_model=List[schemas.Team])
def read_player_captain_teams(
    player_id: int,
    firebase_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_player_existence(db=db, player_id=player_id)
    return crud.get_player_captain_teams(db, player_id=player_id, skip=skip, limit=limit)


# Team - Player operations
@app.put("/api/players/{team_id}")
def link_player_to_team(
    team_id: int,
    player_id: int,
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "moderator"
    access = permissions.is_accessible(
        db=db, firebase_id=firebase_id, clearance=clearance
    )

    def link():
        exceptions.check_for_player_existence(db=db, player_id=player_id)
        exceptions.check_for_team_existence(db=db, team_id=team_id)
        if not crud.is_player_in_team(db, player_id=player_id, team_id=team_id):
            crud.link_player_to_team_with_id(db, team_id, player_id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player already in the team")

    if access:
        link()
    else:
        exceptions.check_for_team_existence(db=db, team_id=team_id)
        db_player = crud.get_player_by_firebase_id(db, firebase_id=firebase_id)
        if db_player is None:
            permissions.permission_denied(clearance)
        flag = crud.is_player_captain(db, player_id=db_player.id, team_id=team_id)
        if flag:
            link()
        else:
            permissions.permission_denied(clearance)


@app.put("/api/unlink_player/{team_id}")
def unlink_player_to_team(
    team_id: int,
    player_id: int,
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "moderator"
    access = permissions.is_accessible(
        db=db, firebase_id=firebase_id, clearance=clearance
    )

    def unlink():
        exceptions.check_for_player_existence(db=db, player_id=player_id)
        exceptions.check_for_team_existence(db=db, team_id=team_id)
        if crud.is_player_in_team(db, player_id=player_id, team_id=team_id):
            crud.unlink_player_to_team_with_id(db, team_id, player_id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player is not in the team")

    if access:
        unlink()
    else:
        exceptions.check_for_team_existence(db=db, team_id=team_id)
        db_player = crud.get_player_by_firebase_id(db, firebase_id=firebase_id)
        if db_player is None:
            permissions.permission_denied(clearance)
        flag = crud.is_player_captain(db, player_id=db_player.id, team_id=team_id)
        if flag or player_id == db_player.id:
            unlink()
        else:
            permissions.permission_denied(clearance)


@app.put("/api/teams/{team_id}")
def set_team_captain(
    team_id: int,
    player_id: int,
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "moderator"
    access = permissions.is_accessible(
        db=db, firebase_id=firebase_id, clearance=clearance
    )

    def set_captain():
        exceptions.check_for_player_existence(db=db, player_id=player_id)
        exceptions.check_for_team_existence(db=db, team_id=team_id)
        if not crud.is_player_in_team(db, player_id=player_id, team_id=team_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player not in team")
        crud.set_team_captain(db, player_id=player_id, team_id=team_id)

    if access:
        set_captain()
    else:
        exceptions.check_for_team_existence(db=db, team_id=team_id)
        db_player = crud.get_player_by_firebase_id(db, firebase_id=firebase_id)
        if db_player is None:
            permissions.permission_denied(clearance)
        flag = crud.is_player_captain(db, player_id=db_player.id, team_id=team_id)
        if flag:
            set_captain()
        else:
            permissions.permission_denied(clearance)


# matches
@app.post("/api/matches/", response_model=schemas.Match)
def create_match(
    match: schemas.MatchCreate,
    team1_id: int = Header(None),
    team2_id: int = Header(None),
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "moderator"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_team_existence(db=db, team_id=team1_id)
    exceptions.check_for_team_existence(db=db, team_id=team2_id)
    return crud.create_match(db=db, match=match, team1_id=team1_id, team2_id=team2_id)


@app.get("/api/matches/", response_model=List[schemas.Match])
def read_matches(
    firebase_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    matches = crud.get_matches(db, skip=skip, limit=limit)
    return matches


@app.get("/api/matches_count/", response_model=int)
def count_matches(
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.count_matches(db)


@app.get("/api/upcoming_matches/", response_model=List[schemas.Match])
def read_upcoming_matches(
    firebase_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.get_upcoming_matches(db, skip=skip, limit=limit)


@app.get(
    "/api/personal_upcoming_matches/{player_id}", response_model=List[schemas.Match]
)
def read_upcoming_personal_matches(
    firebase_id: str = Header(None),
    player_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_player_existence(db=db, player_id=player_id)
    return crud.get_personal_upcoming_matches(db, player_id=player_id, skip=skip, limit=limit)


@app.get("/api/count_personal_upcoming_matches/{player_id}", response_model=int)
def count_upcoming_personal_matches(
    firebase_id: str = Header(None),
    player_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_player_existence(db=db, player_id=player_id)
    return crud.count_personal_upcoming_matches(db, player_id=player_id)


@app.get(
    "/api/personal_finished_matches/{player_id}", response_model=List[schemas.Match]
)
def read_finished_personal_matches(
    firebase_id: str = Header(None),
    player_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_player_existence(db=db, player_id=player_id)
    return crud.get_personal_finished_matches(db, player_id=player_id, skip=skip, limit=limit)


@app.get("/api/count_personal_finished_matches/{player_id}", response_model=int)
def count_finished_personal_matches(
    firebase_id: str = Header(None),
    player_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_player_existence(db=db, player_id=player_id)
    return crud.count_personal_finished_matches(db, player_id=player_id)


@app.get("/api/matches/search/", response_model=List[schemas.Match])
def search_matches(
    firebase_id: str = Header(None),
    name: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.search_matches_by_name(db, name=name, skip=skip, limit=limit)


@app.get("/api/matches_count_by_search/", response_model=int)
def count_matches_by_search(
    firebase_id: str = Header(None),
    name: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.count_matches_by_search(db, name)


@app.get("/api/matches/{match_id}", response_model=schemas.Match)
def read_match(
    match_id: int = Header(None),
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_match_existence(db=db, match_id=match_id)
    db_match = crud.get_match(db, match_id=match_id)
    return crud.get_match(db, match_id=match_id)


@app.patch("/api/matches/{match_id}")
def update_match(
    match: schemas.MatchUpdate,
    match_id: int = None,
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "moderator"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_match_existence(db=db, match_id=match_id)
    crud.update_match(db, match_id=match_id, match=match)


# tournaments
@app.post("/api/tournaments/", response_model=schemas.Tournament)
def create_tournament(
    tournament: schemas.TournamentCreate,
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "moderator"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    if tournament.tournament_type not in [
        "round-robin",
        "swiss",
        "single-elimination",
    ]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tournament type unknown")
    teams_ids = tournament.teams_ids
    for team_id in teams_ids:
        exceptions.check_for_team_existence(db=db, team_id=team_id)
    if tournament.tournament_type == "swiss":
        if len(teams_ids) % 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Swiss tournament: requires even number of teams",
            )
        if len(teams_ids) < tournament.swiss_rounds + 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Swiss tournament: Not enough teams for "
                + str(tournament.swiss_rounds)
                + " number of rounds",
            )
        if tournament.swiss_rounds <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Swiss tournament: non-positive number of rounds",
            )
    elif tournament.tournament_type == "single-elimination":
        if len(teams_ids) not in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Single-elimination tournament: number of teams should be a power of 2",
            )
    return crud.create_tournament(db=db, tournament=tournament)


@app.get("/api/tournaments/", response_model=List[schemas.Tournament])
def read_tournaments(
    firebase_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.get_tournaments(db, skip=skip, limit=limit)


@app.get("/api/tournaments_count/", response_model=int)
def count_tournaments(
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.count_tournaments(db)


@app.get("/api/tournaments/search/", response_model=List[schemas.Tournament])
def search_tournaments(
    firebase_id: str = Header(None),
    name: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.search_tournaments_by_name(db, name=name, skip=skip, limit=limit)


@app.get("/api/tournaments_count_by_search/", response_model=int)
def count_tournaments_by_search(
    firebase_id: str = Header(None),
    name: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    return crud.count_tournaments_by_search(db, name)


@app.get("/api/tournaments/{tournament_id}", response_model=schemas.Tournament)
def read_tournament(
    tournament_id: int = Header(None),
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    db_tournament = crud.get_tournament(db, tournament_id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tournament not found")
    return db_tournament


# Tournament - Matches


@app.patch("/api/tournaments/{tournament_id}/input_match_result")
def update_tournament_match(
    match: schemas.MatchResult,
    match_id: int = None,
    tournament_id: int = None,
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "moderator"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    db_tournament = crud.get_tournament(db, tournament_id=tournament_id)
    exceptions.check_for_match_existence(db=db, match_id=match_id)
    if db_tournament is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tournament not found")
    if not crud.is_match_in_tournament(
        db, tournament_id=tournament_id, match_id=match_id
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Match not in tournament")
    if crud.is_match_empty(db, match_id=match_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Teams are not set in match yet"
        )
    if db_tournament.tournament_type == "single-elimination" and (
        match.score1 == match.score2
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No ties allowed in single-elimination tournament",
        )
    crud.update_tournament_match(
        db, tournament_id=tournament_id, match_id=match_id, match=match
    )


@app.get("/api/tournament/{tournament_id}/matches", response_model=List[schemas.Match])
def read_tournament_matches(
    tournament_id: int = Header(None),
    firebase_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_tournament_existence(db=db, tournament_id=tournament_id)
    return crud.get_tournament_matches(db, tournament_id=tournament_id, skip=skip, limit=limit)


@app.get("/api/tournament_matches_count/", response_model=int)
def count_tournament_matches(
    firebase_id: str = Header(None),
    tournament_id: int = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_tournament_existence(db=db, tournament_id=tournament_id)
    return crud.count_tournament_matches(db, tournament_id=tournament_id)



@app.get(
    "/api/tournament/{tournament_id}/finished_matches",
    response_model=List[schemas.Match],
)
def read_tournament_finished_matches(
    tournament_id: int = Header(None),
    firebase_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_tournament_existence(db=db, tournament_id=tournament_id)
    return crud.get_tournament_finished_matches(db, tournament_id=tournament_id, skip=skip, limit=limit)


@app.get(
    "/api/tournament/{tournament_id}/unfinished_matches",
    response_model=List[schemas.Match],
)
def read_tournament_unfinished_matches(
    tournament_id: int = Header(None),
    firebase_id: str = Header(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_tournament_existence(db=db, tournament_id=tournament_id)
    return crud.get_tournament_unfinished_matches(
        db, tournament_id=tournament_id, skip=skip, limit=limit
    )


@app.get(
    "/api/tournament/{tournament_id}/scoreboard",
    response_model=schemas.TournamentResults,
)
def read_tournament_scoreboard(
    tournament_id: int = Header(None),
    firebase_id: str = Header(None),
    db: Session = Depends(get_db),
):
    clearance = "guest"
    permissions.check_for_permission(db=db, firebase_id=firebase_id, clearance=clearance)
    exceptions.check_for_tournament_existence(db=db, tournament_id=tournament_id)
    return crud.get_tournament_scoreboard(db, tournament_id=tournament_id)
