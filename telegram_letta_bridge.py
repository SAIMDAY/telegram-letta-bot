import os
import logging
from typing import Final

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from letta_client import Letta

# ========================= CONFIG =========================
TELEGRAM_TOKEN: Final[str] = os.getenv("TELEGRAM_TOKEN")
LETTA_API_KEY: Final[str] = os.getenv("LETTA_API_KEY")
AGENT_ID: Final[str] = os.getenv("AGENT_ID")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

client = Letta(api_key=LETTA_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    user_message = update.message.text
    chat_id = update.message.chat_id

    logger.info(f"Received from {chat_id}: {user_message}")

    try:
        response = client.agents.messages.create(
            agent_id=AGENT_ID,
            messages=[{"role": "user", "content": user_message}]
        )

        reply_text = ""
        for msg in response.messages:
            if msg.message_type == "assistant_message" and msg.content:
                reply_text += msg.content + "\n"

        if not reply_text.strip():
            reply_text = "Got it!"

        await context.bot.send_message(chat_id=chat_id, text=reply_text.strip())

    except Exception as e:
        logger.error(f"Error: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Sorry, something went wrong.")

def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    app.run_polling(poll_interval=1.0)

if __name__ == "__main__":
    main()