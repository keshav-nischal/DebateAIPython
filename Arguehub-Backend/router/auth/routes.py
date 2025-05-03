from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
def login():
    print("logging in")

@router.get("/signup")
def signup():
    print("signing up")

@router.get("/logout")
def signup():
    print("logging out")