from sqlalchemy import Column, Integer, Text
from app.database.main import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    email = Column(Text)
    hashed_password = Column(Text)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', hashed_password='{self.hashed_password}')>"




