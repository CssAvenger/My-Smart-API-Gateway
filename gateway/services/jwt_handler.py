from jwt import PyJWT, ExpiredSignatureError
from dotenv import load_dotenv
load_dotenv()
import os

class JWTHandler:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt = PyJWT()

    def encode(self, payload: dict) -> str:
        return self.jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode(self, token: str) -> dict:
        try:
            print(f"Decoding token: {token}", f"key {self.secret_key}", f"algorithm {self.algorithm}")
            return self.jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            raise ValueError("Token has expired")
        except Exception as e:
            print(f"Error decoding token: {str(e)}")
            raise ValueError(f"Invalid token: {str(e)}")
