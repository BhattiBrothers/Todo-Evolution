# [Spec: SPEC-002 — Authentication]
# JWT verification middleware for FastAPI

import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"
bearer = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer)) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub") or payload.get("id") or payload.get("userId")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: no user ID")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
