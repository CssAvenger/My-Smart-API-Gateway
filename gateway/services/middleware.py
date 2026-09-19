import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from gateway.services.access_control import AccessControl
from gateway.services.jwt_handler import JWTHandler
from gateway.services.rate_limiter import MemoryRateLimiter


limiter = {}


def register_middlewares(app: FastAPI) -> None:

    # Request Logging Middleware
    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid.uuid4())
        )
        start_time = time.perf_counter()

        response = await call_next(request)

        duration = time.perf_counter() - start_time

        print(
            f"request_id={request_id} "
            f"method={request.method} "
            f"path={request.url.path} "
            f"status={response.status_code} "
            f"duration={duration:.4f}s"
        )

        response.headers["X-Request-ID"] = request_id

        return response

    #   Rate Limiting Middleware
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"

        rate_limiter = MemoryRateLimiter(limiter)
        allowed = await rate_limiter.is_allowed(client_ip)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit_exceeded",
                    "message": "Too many requests"
                }
            )

        response = await call_next(request)

        return response
    
    # JWT Authentication Middleware
    @app.middleware("http")
    async def jwt_authentication_middleware(request: Request, call_next):
        if request.url.path.startswith("/api/"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "unauthorized",
                        "message": "Missing or invalid Authorization header"
                    }
                )

            token = auth_header.split(" ")[1]

            jwt_handler = JWTHandler()
            try:
                if not jwt_handler.decode(token):
                    return JSONResponse(
                        status_code=401,
                        content={
                            "error": "unauthorized",
                            "message": "Invalid token"
                        }
                    )
            except Exception as e:
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "unauthorized",
                        "message": str(e)
                    }
                )

        response = await call_next(request)
        return response
    

    # RBAC Middleware
    @app.middleware("http")
    async def rbac_middleware(request: Request, call_next):
        if request.url.path.startswith("/api/"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "unauthorized",
                        "message": "Missing or invalid Authorization header"
                    }
                )

            token = auth_header.split(" ")[1]

            jwt_handler = JWTHandler()
            try:
                payload = jwt_handler.decode(token)
                user_role = payload.get("role")
                if not user_role:
                    return JSONResponse(
                        status_code=403,
                        content={
                            "error": "forbidden",
                            "message": "User role not found in token"
                        }
                    )
                # Example RBAC logic: Only allow 'admin' role to access certain endpoints
                if AccessControl.is_allowed(user_role, request.url.path, request.method) is False:
                    return JSONResponse(
                        status_code=403,
                        content={
                            "error": "forbidden",
                            "message": "You do not have permission to access this resource"
                        }
                    )
            except Exception as e:
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "unauthorized",
                        "message": str(e)
                    }
                )

        response = await call_next(request)
        return response