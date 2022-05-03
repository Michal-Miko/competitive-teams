from app.database import crud
from fastapi import HTTPException, status
from app.firebase.firebase import verify_token


class InvalidRoleException(Exception):
    pass


ROLES = {
    "admin": 10,
    "moderator": 5,
    "player": 1,
    "guest": 0,
}


def is_higher_role(role1, role2):
    if role1 not in ROLES:
        raise InvalidRoleException("{} is not a valid role".format(role1))
    if role2 not in ROLES:
        raise InvalidRoleException("{} is not a valid role".format(role2))
    return ROLES[role1] >= ROLES[role2]


def is_accessible(db, firebase_token, clearance="player"):
    if firebase_token is None or firebase_token == "null":
        db_role = "guest"
    else:
        uid = verify_token(firebase_token)
        db_player = crud.get_player_by_firebase_id(db, uid)
        if db_player is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db_role = db_player.role
    return is_higher_role(db_role, clearance)


def permission_denied(clearance):
    text = "Permission denied. Required role: {}.".format(clearance)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=text)


def check_for_permission(db, firebase_token, clearance):
    if not is_accessible(db, firebase_token, clearance):
        permission_denied(clearance=clearance)