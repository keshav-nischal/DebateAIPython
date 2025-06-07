from database import get_sql_session
from models import User
from crud.user import get_user, add_new_user
import bcrypt
import datetime
import jwt

from abc import ABC, abstractmethod

class AuthStrategy(ABC):
    @abstractmethod
    def login(self, request_data):
        pass
    @abstractmethod
    def signup(self, request_data):
        pass


class EmailPasswordAuth(AuthStrategy):
    def login(session, login_request_data):
        user = get_user(session, login_request_data.email)

        if bcrypt.checkpw(login_request_data.password.encode("utf-8"), user.hashed_password.encode("utf-8")):
            jwtToken = EmailPasswordAuth.generate_JWT_token(user)
            return jwtToken
        raise Exception("Wrong Password!")

    def signup(session, userName, password):
        hashed_password = EmailPasswordAuth.hash_password(password)
        try:
            new_user = add_new_user(session, userName, hashed_password)
        except Exception as e:
            raise e
        
        jwtToken = EmailPasswordAuth.generate_JWT(new_user)
        return jwtToken

    @staticmethod
    def generate_JWT(user: User):
        payload = {
            "sub": user.id,  # subject
            "name": user.name,
            "iat": datetime.datetime.now(datetime.timezone.utc),  # issued at
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)  # expires in 1 day
        }
        jwtToken = jwt.encode(payload=payload, key=EmailPasswordAuth.SECRET_KEY,  algorithm=("HS256"))

        return jwtToken
    

    @staticmethod
    def verify_JWT(jwtToken):
        try:
            jwt.decode(jwt=jwtToken, key=EmailPasswordAuth.SECRET_KEY, algorithms=("HS256"))
        except jwt.ExpiredSignatureError:
            print("Token Expired")
        except jwt.InvalidTokenError:
            print("Invalid Token")

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

class GoogleAuth(AuthStrategy):
    def login(self, request_data):
        token = request_data.get("google_token")
        # TODO: Use Google API to verify token
        if token == "valid_token":
            return {"status": "success", "user_id": 99}
        return {"status": "fail", "reason": "Invalid token"}

class AuthContext:
    def __init__(self, provider: str):
        
        if(provider == "IN_HOUSE"):
            self.strategy = EmailPasswordAuth()
        elif(provider == "GOOGLE"):
            self.strategy = GoogleAuth()
        else:
            raise NotImplementedError

    def login(self, sql_db_session, request_data):
        return self.strategy.login(sql_db_session, request_data)
    
    def signup(self, sql_db_session, request_data):
        return self.strategy.signup(sql_db_session, request_data)

