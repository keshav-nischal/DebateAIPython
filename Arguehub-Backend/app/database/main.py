from sqlalchemy import create_engine, select
from sqlalchemy import text, Column, Integer, Enum as SqlEnum, Text, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from enum import Enum as PyEnum
import bcrypt
import jwt
import datetime
# engine = create_engine('sqlite:///example.db')

# with engine.connect() as connection:
#     result = connection.execute("Select * from users")
#     print(result)


def main_core():
    engine = create_engine('sqlite:///example.db')

    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                hashed_password TEXT
            )
        """))
        connection.execute(
            text(
                """
            INSERT INTO users(id, name, hashed_password)
            VALUES (1, 'keshav', 'password')
            """
            )
        )
        result = connection.execute(text("SELECT * FROM users"))
        for row in result:
            print(row)

Base = declarative_base()

class SenderType(PyEnum):
    USER = "User"
    AGENT = "Agent"

class AgentChatHistory(Base):
    __tablename__ = "agent_chat_history"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer)
    sender = Column(SqlEnum(SenderType))
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<AgentChatHistory(message_id={self.message_id}, session_id={self.session_id}, sender='{self.sender.value}', content='{self.content}', timestamp='{self.timestamp}')>"

# class AgentHistorySessionId(Base):
#     __tablename__ = "agent_chat_history_session_id"

    
# CRUD
def getSessionId(userId):
    pass

def addToAgentChatHistory(message):
    pass

def main():
    engine = create_engine("sqlite:///example.db")
    Base.metadata.create_all(engine)

    session = Session(bind=engine)

    new_message_1 = AgentChatHistory(session_id=1, sender=SenderType.USER, content="Hello buddy")
    new_message_2 = AgentChatHistory(session_id=1, sender=SenderType.AGENT, content="Hi")

    session.add(new_message_1)
    session.commit()
    session.add(new_message_2)
    session.commit()

    rows = session.query(AgentChatHistory).all()
    for row in rows:
        print(row)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    hashed_password = Column(Text)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', hashed_password='{self.hashed_password}')>"
    

# CRUD
def get_user(session, name):
    query = select(User).where(User.name == name)
    return session.execute(query).scalar_one_or_none()

def add_new_user(session, name, password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    new_user = User(name=name, hashed_password=hashed_password.decode())
    session.add(new_user)
    return new_user

SECRET_KEY = "secret"
PUBLIC_KEY = "public" #will be used when we will set public and private key for auth

def generate_JWT_token(user):
    payload = {
        "sub": user.id,  # subject
        "name": user.name,
        "iat": datetime.datetime.now(datetime.timezone.utc),  # issued at
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)  # expires in 1 day
    }
    jwtToken = jwt.encode(payload=payload, key=SECRET_KEY,  algorithm=("HS256"))

    return jwtToken

def verify_JWT_token(jwtToken):
    try:
        jwt.decode(jwt=jwtToken, key=SECRET_KEY, algorithms=("HS256"))
    except jwt.ExpiredSignatureError:
        print("Token Expired")
    except jwt.InvalidTokenError:
        print("Invalid Token")

def login(session, userName, password):
    user = get_user(session, userName)
    if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8")):
        jwtToken = generate_JWT_token(user)
        return jwtToken
    raise Exception("Wrong Password!")

def signup(session, userName, password):
    new_user = add_new_user(session, userName, password)
    jwtToken = generate_JWT_token(new_user)
    return jwtToken

def auth_main():
    engine = create_engine("sqlite:///examples.dp")
    Base.metadata.create_all(engine)
    session = Session(engine)
    print(signup(session, "keshav", "Reduce10!!"))
    
    print(login(session, "keshav", "Reduce10!!"))


def get_session():
    DB_URL = "sqlite:///examples.dp" # change to env
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine) #TODO: remove for prod
    session = Session(engine)
    # print(signup(session, "keshav", "Reduce10!!"))
    
    # print(login(session, "keshav", "Reduce10!!"))
    return session
# authMain()

