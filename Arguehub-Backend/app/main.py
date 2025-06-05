from fastapi import FastAPI
import uvicorn

from api.v1.auth import router as auth_router

# print("\n".join(router.path))

app = FastAPI()
app.include_router(auth_router)

@app.get("/heartbeat")
async def root():
    return {"message": "hello world"}


def main():
    uvicorn.run(app, host="127.0.0.1", port=8004)

if __name__ == "__main__":
    main()