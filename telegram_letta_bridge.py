import os
import sys
import logging
from typing import Final

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from letta import Letta

# ========================= CONFIG =========================
TELEGRAM_TOKEN: Final[str] = os.getenv("TELEGRAM_TOKEN")
LETTA_API_KEY: Final[str] = os.getenv("LETTA_API_KEY")
AGENT_ID: Final[str] = os.getenv("AGENT_ID")
LETTA_API_BASE_URL: Final[str] = os.getenv("LETTA_API_BASE_URL", "https://api.letta.com")

# ========================= VALIDATION =========================
missing_vars = []
if not TELEGRAM_TOKEN:
    missing_vars.append("TELEGRAM_TOKEN")
if not LETTA_API_KEY:
    missing_vars.append("LETTA_API_KEY")
if not AGENT_ID:
    missing_vars.append("AGENT_ID")

if missing_vars:
    print(f"❌ ERROR: Missing environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

print(f"✅ Environment variables loaded successfully")
print(f"✅ Using Letta API: {LETTA_API_BASE_URL}")

# ========================= LOGGING =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========================= LETTA CLIENT =========================
try:
    client = Letta(api_key=LETTA_API_KEY, base_url=LETTA_API_BASE_URL)
    logger.info("✅ Letta client initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize Letta client: {e}")
    sys.exit(1)

# ========================= MESSAGE HANDLER =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming Telegram messages and send to Letta agent."""
    if not update.message or not update.message.text:
        return

    user_message = update.message.text
    chat_id = update.message.chat_id

    logger.info(f"📨 Received from {chat_id}: {user_message}")

    try:
        # Send message to Letta agent
        response = client.agents.messages.create(
            agent_id=AGENT_ID,
            messages=[{"role": "user", "content": user_message}]
        )

        # Extract assistant response
        reply_text = ""
        for msg in response.messages:
            if hasattr(msg, 'message_type') and msg.message_type == "assistant_message" and hasattr(msg, 'content') and msg.content:
                reply_text += msg.content + "\n"

        if not reply_text.strip():
            reply_text = "Got it!"

        # Send reply back to Telegram
        await context.bot.send_message(chat_id=chat_id, text=reply_text.strip())
        logger.info(f"✅ Sent response to {chat_id}")

    except Exception as e:
        logger.error(f"❌ Error processing message: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Sorry, something went wrong. Please try again.")

# ========================= MAIN =========================
def main() -> None:
    """Start the Telegram bot with polling."""
    try:
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info("🤖 Bot is starting...")
        print("🤖 Bot is running and listening for messages...")
        app.run_polling(poll_interval=1.0)
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
