import os
import logging
import sys
import time
from typing import Final

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

logger.info("=== Starting Letta-Telegram Bridge ===")

# Environment variables
TELEGRAM_TOKEN: Final[str] = os.getenv("TELEGRAM_TOKEN") or ""
LETTA_API_KEY: Final[str] = os.getenv("LETTA_API_KEY") or ""
AGENT_ID: Final[str] = os.getenv("AGENT_ID") or ""

if not TELEGRAM_TOKEN:
    logger.critical("❌ TELEGRAM_TOKEN is missing")
    sys.exit(1)
if not LETTA_API_KEY:
    logger.critical("❌ LETTA_API_KEY is missing")
    sys.exit(1)
if not AGENT_ID:
    logger.critical("❌ AGENT_ID is missing")
    sys.exit(1)

logger.info("✅ All environment variables loaded")

try:
    from telegram.ext import Application, MessageHandler, filters, ContextTypes
    from telegram import Update
    from letta_client import Letta
    logger.info("✅ Libraries imported")
except Exception as e:
    logger.critical(f"❌ Failed to import libraries: {e}")
    sys.exit(1)

client = Letta(api_key=LETTA_API_KEY)
logger.info("✅ Connected to Letta Cloud")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    
    msg = update.message.text
    chat_id = update.message.chat_id
    logger.info(f"Message from {chat_id}: {msg}")

    try:
        response = client.agents.messages.create(
            agent_id=AGENT_ID,
            messages=[{"role": "user", "content": msg}]
        )
        
        reply = ""
        for m in response.messages:
            if getattr(m, "message_type", None) == "assistant_message" and m.content:
                reply += m.content + "\n"
        
        await context.bot.send_message(chat_id=chat_id, text=reply.strip() or "👍 Got it!")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Sorry, something went wrong.")

def main():
    logger.info("🚀 Starting Telegram polling...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot is now listening...")
    app.run_polling(poll_interval=1.0, drop_pending_updates=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Bot crashed: {e}")
        time.sleep(5)  # Give Render time to see the log
