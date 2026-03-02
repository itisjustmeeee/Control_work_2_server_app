from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", example="ivan@example.com")
    age: int = Field(..., gt=0, example=25)
    is_subscribed: bool = True

@app.post('/create_user')
async def get_user(user: UserCreate):
    return {
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "is_subscribed": user.is_subscribed
    }

@app.get('/')
async def root():
    return {"message": "йееей, сервер работает. Перейди в /docs для создания пользователя"}

# перейдите в /docs для создания пользователя