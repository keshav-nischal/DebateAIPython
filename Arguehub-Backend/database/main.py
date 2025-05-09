from sqlalchemy import create_engine
from sqlalchemy import text, Column, Integer, Enum, Text, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base



# engine = create_engine('sqlite:///example.db')

# with engine.connect() as connection:
#     result = connection.execute("Select * from users")
#     print(result)


def main():
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

class AgentChatHistory(Base):
    __tablename__ = "agent_chat_history"

    sessionId = Column(Integer, primary_key=True)
    sender = Column(Enum("User", "Agent"))
    content = Column(Text)
    timestamp = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<AgentChatHistory(id={self.sessionId}, name='{self.sender}', email='{self.content}', timestamp='{self.timestamp}')>"
    
def main():
    # using ORM
    engine = create_engine()
    session = Session(bind=engine)
    # make it work, that other user is not accessing other users chat
    
    # session.
    
main()
