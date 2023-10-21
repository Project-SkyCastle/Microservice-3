from fastapi import FastAPI

# I like to launch directly and not use the standard FastAPI startup
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello SkyCastle Team, im microservice 3 on Google Cloud"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012)
