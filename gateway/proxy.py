import httpx
from dotenv import load_dotenv
from fastapi import Response
from urllib.parse import urlparse

load_dotenv()

import os


async def gateway_forward(
    method: str,
    url: str,
    headers: dict,
    body: bytes | None = None,
):
    parsed = urlparse(url)
    path = parsed.path or "/"

    print(f"Forwarding request: method={method}, path={path}")

    if "/api/" in path:
        path = path.replace("/api/", "/", 1)

    if "/users" in path:
        backend_url = os.getenv("USERS_URL")
    elif "/posts" in path:
        backend_url = os.getenv("POSTS_URL")
    else:
        backend_url = None

    if not backend_url:
        return Response(content='{"detail":"Not Found"}', status_code=404, media_type="application/json")

    target_url = backend_url.rstrip("/") + path
    if parsed.query:
        target_url = f"{target_url}?{parsed.query}"

    print(f"Forwarding request to backend: {target_url}")

    async with httpx.AsyncClient() as client:
        upstream = await client.request(
            method=method,
            url=target_url,
            headers=headers,
            content=body,
        )

    excluded_headers = {
        "content-length",
        "transfer-encoding",
        "connection",
        "content-encoding",
    }
    response_headers = {
        key: value
        for key, value in upstream.headers.items()
        if key.lower() not in excluded_headers
    }

    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=response_headers,
        media_type=upstream.headers.get("content-type"),
    )
