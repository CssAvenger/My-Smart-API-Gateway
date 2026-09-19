import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

DATA_FILE = Path(__file__).with_name("users.json")


class UserBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=10, max_length=15)
    username: str = Field(..., min_length=6, max_length=20)


class User(UserBase):
    id: int


app = FastAPI(
    title="Dummy User APIs for Smart Gateway",
    version="1.0.0",
    description="Fake user API endpoints for testing the smart gateway.",
)


def load_users() -> List[Dict[str, Any]]:
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []
    return data


def save_users(users: List[Dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)


@app.get("/users", tags=["Users"])
def fetch_users() -> List[Dict[str, Any]]:
    return load_users()


@app.get("/users/{user_id}", tags=["Users"])
def fetch_single_user(user_id: int) -> Dict[str, Any]:
    users = load_users()
    for user in users:
        if user.get("id") == user_id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found",
    )


@app.post("/users", tags=["Users"], status_code=status.HTTP_201_CREATED)
def create_user(user: UserBase) -> Dict[str, Any]:
    users = load_users()
    new_id = max((item.get("id", 0) for item in users), default=0) + 1

    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "username": user.username,
    }
    users.append(new_user)
    save_users(users)
    return new_user


@app.patch("/users/{user_id}", tags=["Users"])
def update_user(user_id: int, user_update: UserBase) -> Dict[str, Any]:
    users = load_users()

    for index, user in enumerate(users):
        if user.get("id") == user_id:
            update_data = user_update.model_dump(exclude_unset=True)
            user.update(update_data)
            users[index] = user
            save_users(users)
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found",
    )


@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int) -> Dict[str, str]:
    users = load_users()

    for index, user in enumerate(users):
        if user.get("id") == user_id:
            deleted_user = users.pop(index)
            save_users(users)
            return {"message": f"User {user_id} deleted successfully", "deleted_user": deleted_user["name"]}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found",
    )


@app.get("/", tags=["Root"])
def root() -> Dict[str, str]:
    return {"message": "Dummy user backend is running"}


backend_app = app
