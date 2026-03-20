from fastapi import FastAPI, Header, HTTPException, Depends, Response
import re
from pydantic import BaseModel, field_validator
from datetime import datetime, timezone

app = FastAPI()

def get_headers(
    user_agent: str | None = Header(None),
    accept_language: str | None = Header(None)
):
    return CommonHeaders(
        User_Agent=user_agent,
        Accept_Language=accept_language
    )

class CommonHeaders(BaseModel):
    User_Agent: str | None
    Accept_Language: str | None

    @field_validator("Accept_Language")
    @classmethod
    def validate_language(cls, value):
        if value is None:
            return value
        
        pattern = r"^([a-zA-Z]{2,3}(-[a-zA-Z0-9]+)?)(,[a-zA-Z]{2,3}(-[a-zA-Z0-9]+)?(;q=[0-9.]+)?)*$"

        if not re.match(pattern, value.strip()):
            raise HTTPException(status_code=400, detail="Invalid Accept-Language format. Example: ru-RU,ru;q=0.9,en;q=0.8")
        
        return value

@app.get('/headers')
async def get_browser_and_language(response: Response, headers: CommonHeaders = Depends(get_headers)):
    response.headers["Cache-Control"] = "no-store"
    if headers.User_Agent is None or headers.Accept_Language is None:
        raise HTTPException(status_code=400, detail="Missing required header")
    return {
        "User-agent": headers.User_Agent,
        "Accept-language": headers.Accept_Language
    }

@app.get('/info')
async def get_header_with_dop(response: Response, headers: CommonHeaders = Depends(get_headers)):
    response.headers["Cache-Control"] = "no-store"
    if headers.User_Agent is None or headers.Accept_Language is None:
        raise HTTPException(status_code=400, detail="Missing required header")
    
    server_time = datetime.now(timezone.utc).strftime("%H:%M:%S")

    return {
        "message": "Добро пожаловать, выши заголовки успешно обработаны",
        "headers": {
            "User-agent": headers.User_Agent,
            "Accept-language": headers.Accept_Language
        },
        "X-Server-Time": server_time
    }

