from firebase_admin import auth, initialize_app
from fastapi import HTTPException

default_app = initialize_app()

def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token, check_revoked=True)
        return decoded_token['uid']
    except auth.RevokedIdTokenError:
        # Token revoked, inform the user to reauthenticate or signOut().
        HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is revoked, please reauthenticate.")
    except auth.InvalidIdTokenError:
        # Token is invalid
        HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid, please reauthenticate.")
    except auth.ExpiredTokenError:
        # Token is expired
        HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token has expired, please reauthenticate.")
