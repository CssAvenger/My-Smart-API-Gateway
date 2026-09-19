import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

DATA_FILE = Path(__file__).with_name("posts.json")


class PostBase(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)


class PostCreate(PostBase):
    id: Optional[int] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None


class Post(PostBase):
    id: Optional[int] = None


app = FastAPI(
    title="Dummy Post APIs for Smart Gateway",
    version="1.0.0",
    description="Fake post API endpoints for testing the smart gateway.",
)


def load_posts() -> List[Dict[str, Any]]:
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


def save_posts(posts: List[Dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(posts, file, indent=2)


@app.get("/posts", tags=["Posts"])
def fetch_posts() -> List[Dict[str, Any]]:
    return load_posts()


@app.get("/posts/{post_id}", tags=["Posts"])
def fetch_single_post(post_id: int) -> Dict[str, Any]:
    posts = load_posts()
    for post in posts:
        if post.get("id") == post_id:
            return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {post_id} not found",
    )


@app.post("/posts", tags=["Posts"], status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate) -> Dict[str, Any]:
    posts = load_posts()
    new_id = max((item.get("id", 0) for item in posts), default=0) + 1

    new_post = {
        "id": new_id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
    }
    posts.append(new_post)
    save_posts(posts)
    return new_post


@app.patch("/posts/{post_id}", tags=["Posts"])
def update_post(post_id: int, post_update: PostUpdate) -> Dict[str, Any]:
    posts = load_posts()

    for index, post in enumerate(posts):
        if post.get("id") == post_id:
            update_data = post_update.model_dump(exclude_unset=True)
            post.update(update_data)
            posts[index] = post
            save_posts(posts)
            return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {post_id} not found",
    )


@app.delete("/posts/{post_id}", tags=["Posts"])
def delete_post(post_id: int) -> Dict[str, str]:
    posts = load_posts()

    for index, post in enumerate(posts):
        if post.get("id") == post_id:
            posts.pop(index)
            save_posts(posts)
            return {"message": f"Post {post_id} deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {post_id} not found",
    )


@app.get("/", tags=["Root"])
def root() -> Dict[str, str]:
    return {"message": "Dummy post backend is running"}


post_backend_app = app
