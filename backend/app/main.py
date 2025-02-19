from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pymongo import MongoClient
import os
import asyncio
from backend.app.bot.discord_bot import start_bot

# Load environment variables
load_dotenv()

app = FastAPI(title="Discord AI Friend")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = MongoClient(os.getenv("MONGODB_URI"))
    app.mongodb = app.mongodb_client.ai_friend_db

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Start Discord bot in the background
@app.on_event("startup")
async def start_discord_bot():
    asyncio.create_task(start_bot())

@app.get("/")
async def root():
    return {"status": "running"}