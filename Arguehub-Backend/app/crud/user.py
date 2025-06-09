from fastapi import HTTPException, status
from app.models import User
from sqlalchemy import select
    
# CRUD
def get_user(session, email):
    query = select(User).where(User.email == email)
    return session.execute(query).scalar_one_or_none()

def add_new_user(session, email, hashed_password, name=""):
    user = get_user(session, email)
    if(user):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )    
    if not name:
        name = email.split('@')[0]

    new_user = User(name = name, email=email, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    return new_user