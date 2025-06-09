from abc import ABC, abstractmethod
import bcrypt
import datetime
import jwt
from app.models import User
from app.crud.user import get_user, add_new_user
import os

# === Base Strategy ===
class AuthStrategy(ABC):
    @abstractmethod
    def login(self, context: dict):
        pass

    @abstractmethod
    def signup(self, context: dict):
        pass


# === Email/Password Strategy ===
class EmailPasswordAuth(AuthStrategy):
    SECRET_KEY = os.getenv("AUTH_SECRET_KEY")

    def login(self, context: dict):
        session = context.get("session")
        email = context.get("email")
        password = context.get("password")

        user = get_user(session, email)
        if not user:
            raise Exception("User not found")

        if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8")):
            return {"token": self.generate_JWT(user)}

        raise Exception("Wrong password!")

    def signup(self, context: dict):
        session = context.get("session")
        email = context.get("email")
        password = context.get("password")

        hashed_password = self.hash_password(password)

        try:
            new_user = add_new_user(session, email, hashed_password)
        except Exception as e:
            raise e

        return {"token": self.generate_JWT(new_user)}

    def generate_JWT(self, user: User):
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
        }

        token = jwt.encode(payload=payload, key=EmailPasswordAuth.SECRET_KEY, algorithm="HS256")
        return token 

    @staticmethod
    def verify_JWT(jwtToken):
        try:
            return jwt.decode(jwt=jwtToken, key=EmailPasswordAuth.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as e:
            print(e)
        except jwt.InvalidTokenError as e:
            print(e)
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


# === Google Auth Strategy ===
class GoogleAuth(AuthStrategy):
    def login(self, context: dict):
        token = context.get("google_token")
        # TODO: Use Google API to verify token
        if token == "valid_token":
            return {"status": "success", "user_id": 99}
        return {"status": "fail", "reason": "Invalid token"}

    def signup(self, context: dict):
        raise NotImplementedError("Google signup not supported (yet)")


# === Context Class ===
class AuthContext:
    def __init__(self, provider: str):
        if provider == "IN_HOUSE":
            self.strategy = EmailPasswordAuth()
        elif provider == "GOOGLE":
            self.strategy = GoogleAuth()
        else:
            raise NotImplementedError(f"Auth provider '{provider}' not supported.")

    def login(self, context: dict):
        return self.strategy.login(context)

    def signup(self, context: dict):
        return self.strategy.signup(context)
