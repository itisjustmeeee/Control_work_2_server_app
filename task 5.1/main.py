from fastapi import FastAPI, Response, Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uuid

app = FastAPI()

users_bd = {
    "Oli": "3421J",
    "Will": "336284",
    "Guy": "3548Kj"
}

sessions = {}
security = HTTPBasic()

async def login_user(credentails: HTTPBasicCredentials = Depends(security)):
    username = credentails.username
    password = credentails.password

    if username not in users_bd or users_bd[username] != password:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    session_token = str(uuid.uuid4())
    sessions[session_token] = username

    response = Response(status_code=200)
    response.set_cookie(key="session_token", value=session_token, max_age=3600, httponly=True, secure=False, samesite="lax")
    return response

async def find_user(session_token: str | None = Cookie(default=None)):
    if not session_token or session_token not in sessions:
        raise HTTPException(status_code=401, detail="unauthorized")
    return sessions[session_token]

@app.post('/login')
def log_in_session(response: Response = Depends(login_user)):
    return response

@app.get('/user')
def get_to_user(user: str = Depends(find_user)):
    return {"username": user, "message": "защищенная страница"}
    
# Проверка через запуск: python -m uvicorn main:app --reload и python test_api_httpx.py в отдельных терминалах 