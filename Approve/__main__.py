from config import API_ID, API_HASH, SESSION_STRING, LOG_CHANNEL_ID
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os

# Your API Credentials
API_ID = API_ID
API_HASH = API_HASH
SESSION_STRING = SESSION_STRING

# Channel where requests need to be approved
CHANNEL_USERNAME = "GameStakePredictions"  # No '@' required

# Initialize Pyrogram Bot (For Userbot, Use Session String)
app = Client("approve_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Ensure LOG_CHANNEL_ID is defined in your config.py
# Or raise an exception

async def log_error(client: Client, message: str):
    """Sends an error message to the log channel."""
    try:
        await client.send_message(LOG_CHANNEL_ID, message)
    except Exception as e:
        print(f"Error sending log message: {e}") #Print to console if logging fails

@app.on_message(filters.command("approve"))
async def approve_requests(client: Client, message: Message):
    try:
        # Parse the number of approvals from the command
        args = message.text.split()
        if len(args) < 2 or not args[1].isdigit():
            await message.reply_text("Usage: /approve <count>\nExample: /approve 1000")
            return
        
        count = int(args[1])
        approved_count = 0
        skipped_channels_limit = 0  # Skipped due to USER_CHANNELS_TOO_MUCH
        skipped_deactivated = 0  # Skipped due to INPUT_USER_DEACTIVATED
        await message.reply_text("Processing...")
        # Fetch pending join requests
        async for req in client.get_chat_join_requests(CHANNEL_USERNAME):
            if approved_count >= count:
                break
            try:
                await client.approve_chat_join_request(CHANNEL_USERNAME, req.user.id)
                approved_count += 1
                await asyncio.sleep(1)  # Prevent Telegram flood limits
            except Exception as e:
                error_message = str(e)
                if "USER_CHANNELS_TOO_MUCH" in error_message:
                    skipped_channels_limit += 1  # Count skipped users
                elif "INPUT_USER_DEACTIVATED" in error_message:
                    skipped_deactivated += 1  # Count deactivated users
                else:
                    log_message = f"⚠️ Error approving user {req.user.id}: {error_message}"
                    await log_error(client, log_message)


        # Send final report message
        await message.reply_text(
            f"✅ Approved {approved_count} requests!\n"
            f"⚠️ Skipped {skipped_channels_limit} users (Too many channels limit).\n"
            f"⚠️ Skipped {skipped_deactivated} deactivated users."
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app.run()
