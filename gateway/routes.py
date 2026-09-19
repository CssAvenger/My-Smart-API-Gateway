from fastapi import FastAPI, Request

from gateway.proxy import gateway_forward
from gateway.services.middleware import register_middlewares

routes = FastAPI(
    version="1.0.0",
    title="My Smart Gateway",
    description="This is a smart API gateway with rate limiter and authentication features.",
)

register_middlewares(routes)


@routes.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Smart API Gateway!"}


@routes.api_route("/api/users", methods=["GET", "POST"], tags=["Users"])
async def api_users_collection(request: Request):
    return await gateway_forward(
        method=request.method,
        url=str(request.url),
        headers=request.headers,
        body=await request.body() if request.method in ["POST"] else None,
    )


@routes.api_route("/api/users/{user_id}", methods=["GET", "PATCH", "DELETE"], tags=["Users"])
async def api_users_detail(request: Request, user_id: int):
    return await gateway_forward(
        method=request.method,
        url=str(request.url),
        headers=request.headers,
        body=await request.body() if request.method in ["PATCH"] else None,
    )


@routes.api_route("/api/posts", methods=["GET", "POST"], tags=["Posts"])
async def api_posts_collection(request: Request):
    return await gateway_forward(
        method=request.method,
        url=str(request.url),
        headers=request.headers,
        body=await request.body() if request.method in ["POST"] else None,
    )


@routes.api_route("/api/posts/{post_id}", methods=["GET", "PATCH", "DELETE"], tags=["Posts"])
async def api_posts_detail(request: Request, post_id: int):
    return await gateway_forward(
        method=request.method,
        url=str(request.url),
        headers=request.headers,
        body=await request.body() if request.method in ["PATCH"] else None,
    )
