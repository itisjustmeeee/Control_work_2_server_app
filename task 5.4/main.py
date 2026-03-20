from fastapi import FastAPI, Header, HTTPException, Depends, Response
import re

app = FastAPI()

def validate_language(accept_language: str | None = Header(None)):
    if accept_language is None:
        raise HTTPException(status_code=400, detail="Accepted-languge header is requred")
    
    pattern = r"^([a-zA-Z]{2,3}(-[a-zA-Z0-9]+)?)(,[a-zA-Z]{2,3}(-[a-zA-Z0-9]+)?(;q=[0-9.]+)?)*$"

    if not re.match(pattern, accept_language.strip()):
        raise HTTPException(status_code=400, detail="Invalid Accept-language format. Correct example: ru-RU,ru;q=0.9,en;q=0.8")
    
    return accept_language

@app.get('/headers')
async def get_browser_and_language(response: Response, user_agent: str | None = Header(None), accept_language: str = Depends(validate_language)):
    response.headers["Cache-Control"] = "no-store"
    if user_agent is None or accept_language is None:
        raise HTTPException(status_code=400, detail="Missing required header")
        
    return {
        "User-agent": user_agent,
        "Accept-language": accept_language
    }
