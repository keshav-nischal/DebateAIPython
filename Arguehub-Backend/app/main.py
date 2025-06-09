from dotenv import load_dotenv
from pathlib import Path
env_status = load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env", verbose=True)
print(env_status)
from fastapi import FastAPI
import uvicorn

from app.api.auth import router as auth_router
from sqlalchemy.ext.declarative import declarative_base
import os

from app.database.main import Base, engine


# print("\n".join(router.path))



def main():
    app = FastAPI()

    @app.get("/heartbeat")
    async def heartbeat():
        return {"message": "hello world"}

    app.include_router(auth_router)

    # Base.metadata.create_all(engine) #TODO: remove for prod
    uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("PORT")))


if __name__ == "__main__":
    main()