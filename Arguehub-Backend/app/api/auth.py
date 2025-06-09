from fastapi import APIRouter, Depends, HTTPException

from pydantic  import BaseModel

from app.database import get_sql_session
from app.services.auth_service import AuthContext

router = APIRouter(prefix="/auth")

class LoginRequest(BaseModel):
    provider: str
    details: object
     
@router.post("/login")
async def login(login_request: LoginRequest, sql_db=Depends(get_sql_session)):
    auth_context = AuthContext(login_request.provider)

    # Create context dict to match strategy interface
    context = {
        "session": sql_db,
        **login_request.details  # Flatten details into the context
    }

    try:
        return auth_context.login(context)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/signup")
async def signup(login_request: LoginRequest, sql_db=Depends(get_sql_session)):
    auth_context = AuthContext(login_request.provider)

    context = {
        "session": sql_db,
        **login_request.details
    }

    try:
        return auth_context.signup(context)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# class SignupDetails(BaseModel):
#     name: str
#     password: str

# @router.post()
# def signup(signup_details: SignupDetails, sql_db = Depends(get_sql_session)):
