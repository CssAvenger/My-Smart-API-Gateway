import redis.asyncio as redis

RATE_LIMIT = 10
WINDOW_SECONDS = 60


class RateLimiter:

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def is_allowed(self, client_id: str) -> bool:

        key = f"rate_limit:{client_id}"

        count = await self.redis.incr(key)

        if count == 1:
            await self.redis.expire(key, WINDOW_SECONDS)

        return count <= RATE_LIMIT


import time
class MemoryRateLimiter:

    def __init__(self, requests=None):
        self.requests = requests if requests is not None else {}

    async def is_allowed(self, client_id: str) -> bool:
        now = time.time()

        if client_id not in self.requests:
            self.requests[client_id] = {
                "count": 1,
                "window_start": now
            }
            return True

        data = self.requests[client_id]
        print(f"MemoryRateLimiter: client_id={client_id}, count={data['count']}, window_start={data['window_start']}, now={now}")

        if now - data["window_start"] >= WINDOW_SECONDS:
            data["count"] = 1
            data["window_start"] = now
            return True

        data["count"] += 1

        return data["count"] <= RATE_LIMIT
