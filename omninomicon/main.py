import uvicorn
from fastapi import FastAPI

from .routers import router

app = FastAPI(title="Omninomicon")
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
