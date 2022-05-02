from app.database import crud
from fastapi import HTTPException
from app.utils.exceptions import InvalidRoleException


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


def is_accessible(db, firebase_id, clearance="player"):
    if firebase_id is None or firebase_id == "null":
        db_role = "guest"
    else:
        db_player = crud.get_player_by_firebase_id(db, firebase_id)
        if db_player is None:
            raise HTTPException(status_code=404, detail="User not found")
        db_role = db_player.role
    return is_higher_role(db_role, clearance)


def permission_denied(clearance):
    text = "Permission denied"
    raise HTTPException(status_code=403, detail=text)
