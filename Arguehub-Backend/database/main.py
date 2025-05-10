from sqlalchemy import create_engine
from sqlalchemy import text, Column, Integer, Enum as SqlEnum, Text, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from enum import Enum as PyEnum

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

class AgentHistorySessionId(Base):
    __tablename__ = "agent_chat_history_session_id"

    userI
# CRUD
def getSessionId(userId):

def addToAgentChatHistory(message):


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


    


