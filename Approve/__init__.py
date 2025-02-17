import asyncio
import logging
import time
from pyrogram import *
from aiohttp import ClientSession
from os import environ, getenv, listdir, path
from dotenv import load_dotenv
from pyrogram import Client
from config import *
import config


loop = asyncio.get_event_loop()
load_dotenv()
boot = time.time()


logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)




Approve = Client(
    ":Approve:",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)


async def Approve_bot():
    global API_ID, API_HASH, SESSION_STRING
    await Approve.start()
    


loop.run_until_complete(Approve_bot())

