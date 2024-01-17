from fastapi import FastAPI

from app.routes.ticket import router as ticket_router
from config.config import initialize_queues

app = FastAPI()


# @app.on_event("startup")
# async def start_database():
#     await initiate_database()


@app.on_event("startup")
async def init_queues():
    await initialize_queues()


@app.get("/health")
async def healthcheck():
    return {"message": "Flixbus is great, they have a great customer service."}


app.include_router(ticket_router, tags=["ticket_router"], prefix="/ticket")
