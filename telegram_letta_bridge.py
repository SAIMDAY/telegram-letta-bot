import os
import sys
import logging
import requests
from typing import Final

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ========================= CONFIG ======================== timeout=30)
        
        if response.status_code != 200:
          =
TELEGRAM_TOKEN: Final[str] = os.getenv(await context.bot.send_message(chat_id=chat_id, text="Sorry, I encountered an error. Please try again.")"TELEGRAM_TOKEN")
LETTA_API_KEY: Final[str] = os.getenv = response.json()
        
        # Extract assistant response("LETTA_API_KEY")
            for msg in data["messages"]:
                if msg.get("message_type") == "a
AGENT_ID: Final[str] = os.getenv( and msg.get("content"):
                    reply_text += msg["content"] + "\n"
        
        if not rep"AGENT_ID")
LETTA_API_BASE_URL: Final[str] _text = "Got it!"
        
        # Send reply back to Telegram
        await context.bot.sen= os.getenv("LETTA_API_BASE_URL", "https://api.letta.com")
strip())
        logger.info(f"✅ Sent response to {chat_id}")

    except requests.exceptions.Timeout:
        logger
# ==========_message(chat_id=chat_id, text="Sorry, the request timed out. Please try again.")
    except Exception as e:
        logger.er=============== VALIDATION = processing message: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Sorry, something went wrong. Please try again.")

# =======================================
def main() -> None:
    """Start the Telegram bot with polling."""
    try:
        app = Application.build=============
missing_vars TELEGRAM_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
   = []
if not TELEGRAM_TOKEN:
    missing_vars.append🤖 Bot is starting...")
        print("🤖 Bot is running and liste("TELEGRAM_TOKEN")
if not LETTA_API_KEY:_interval=1.0)
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __n
    missing_vars.append("LETTA_API_KEY")
if 

### FILE not AGENT_ID:
    missing_vars.append("AGENT_ID"):
  - type: worker

if missing_vars:
    print(f"
    buildCommand: pip install -r requirements.txt
    start❌ ERROR: Missing environment variables: {',bridge.py
    envVars:
      - key: TELEGRAM_TOKEN
        scope: all
   '.join(missing_vars)}")
    sys.exit
      - key: AGENT_ID
        scope: all
      - key: LETTA_API_BASE_URL
        value: (1)

print(f"✅ Environment variables loaded successfully What Chang")
print(f"✅ Using Letta API:)
✅ Using plain `requests` instead (minimal, lightweight)
✅ Calling Letta {LETTA_API_BASE_URL}")

# ============ buil============= LOGGING ==========

Replace all three files, p== and deploy.

Should work this tim=============
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========================= MESSAGE HANDLER =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming Telegram messages and send to Letta agent."""
    if not update.message or not update.message.text:
        return

    user_message = update.message.text
    chat_id = update.message.chat_id

    logger.info(f"📨 Received from {chat_id}: {user_message}")

    try:
        # Send message to Letta agent via HTTP
        headers = {
            "Authorization": f"Bearer {LETTA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
        
        url = f"{LETTA_API_BASE_URL}/agents/{AGENT_ID}/messages"
        response = requests.post(url, json=payload, headers=headers,  logger.error(f"❌ Letta API error: {response.status_code} - {response.text}")
            
            return
        
        data
        reply_text = ""
        if "messages" in data:ssistant_message"ly_text.strip():
            replyd_message(chat_id=chat_id, text=reply_text..error(f"❌ Request timeout")
        await context.bot.sendror(f"❌ Error===================== MAIN =er().token(     
        logger.info("ning for messages...")
        app.run_polling(pollame__ == "__main__":
    main()
