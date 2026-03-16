from fastapi import FastAPI, Response, Depends, HTTPException, status, Cookie, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uuid
from itsdangerous import URLSafeSerializer, BadSignature, BadData
from datetime import datetime, timedelta

app = FastAPI()
SECRET = "roof_access_denied_forever"
token_serializer = URLSafeSerializer(secret_key=SECRET)

MAX_IDLE_MINUTES = 5
INACTIVITY_MINUTES = 3

sessions: dict[str, dict] = {}

users_bd = {
    "Oli": "3421J",
    "Will": "336284",
    "Guy": "3548Kj"
}

security = HTTPBasic()

async def login_user(credentails: HTTPBasicCredentials = Depends(security)):
    username = credentails.username
    password = credentails.password

    if username not in users_bd or users_bd[username] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    
    user_id = str(uuid.uuid4())
    session_token = token_serializer.dumps({"uid": user_id})

    now = datetime.now()
    sessions[session_token] = {
        "user_id": user_id,
        "username": username,
        "last_active": now,
        "expires_at": now + timedelta(minutes=MAX_IDLE_MINUTES)
    }

    response = Response(status_code=200)
    response.set_cookie(
        key="session_token", 
        value=session_token,
        httponly=True, 
        secure=False, 
        samesite="lax"
    )
    return response

async def find_user(request: Request, session_token: str | None = Cookie(default=None)):
    if not session_token:
        raise HTTPException(status_code=401, detail="No session token")
    
    try:
        payload = token_serializer.loads(session_token)
    except (BadSignature, BadData):
        raise HTTPException(status_code=401, detail="Invalid or tampered token")
    
    if session_token not in sessions:
        raise HTTPException(status_code=401, detail="Session not found")
    
    session = sessions[session_token]
    now = datetime.now()

    if now > session["expires_at"]:
        del sessions[session_token]
        raise HTTPException(status_code=401, detail="Session expired")
    
    inactive_seconds = (now - session["last_active"]).total_seconds()

    if INACTIVITY_MINUTES * 60 <= inactive_seconds <= MAX_IDLE_MINUTES * 60:
        session["expires_at"] = now + timedelta(minutes=5)

    session["last_active"] = now

    return session["user_id"]

@app.post('/login')
def log_in_session(response: Response = Depends(login_user)):
    return response

@app.get('/user')
def get_to_user(user_id: str = Depends(find_user)):
    return {"user_id": user_id, "message": "защищенная страница"}
    
# Проверка через запуск: python -m uvicorn main:app --reload и python test_api_httpx.py в отдельных терминалах 