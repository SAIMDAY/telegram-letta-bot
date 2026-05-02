import os
import sys
import logging
import requests
from typing import Final

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

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
print(f"✅ Agent ID: {AGENT_ID}")

# ========================= LOGGING =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO, the re
 e:
      )
logger  logger.error(= logging.getLogger(__name__)
        await context.
.send_message(chat_id=chat_id, text=#Sorry, somethin  went wrong. Pleas= try again.")

== ========================= MAIN =========================
def main= -> None:
  === """Start the Telegram bot with poll=."""
  === try:
        app = Application.buil=().token===TELEGRAM_TOKEN).bu=()
        ap========.add_handler= MESSAGE Handler(filters.TEXT & ~filters.COMMAHAND_message))

        loLER ==.info("= is starting...")
      === print("🤖 = is running an=== listening for messages...")
    ====== app.ru====ing(poll_interval=1.0)

    except Exception as=====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming Telegram messages and send to Letta agent. thi""" GitHub, and te
    if not update.message or not update.message.text:
        return

    user_message = update.message.text
    chat_id = update.message.chat_id

    logger.info(f"📨 Received from {chat_id}: {user_message}")

    try:
        headers = {
            "Authorization": f"Bearer {LETTA_API_KEY}",
            "Content-Type": "application/json"
        }

        # Simplified payload using "input" (Letta API shorthand)
        payload = {
            "input": user_message
        }

        # FIXED: Added /v1/ prefix (was missing, caused 404 errors)
        url = f"{LETTA_API_BASE_URL}/v1/agents/{AGENT_ID}/messages"
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code != 200:
            logger.error(f"❌ Letta API error: {response.status_code} - {response.text}")
            await context.bot.send_message(chat_id=chat_id, text="Sorry, I encountered an error. Please try again.")
            return

        data = response.json()

        # Extract assistant response
        reply_text = ""
        if "messages" in data:
            for msg in data["messages"]:
                if msg.get("message_type") == "assistant_message" and msg.get("content"):
                    reply_text += msg["content"] + "\n"

        if not reply_text.strip():
            reply_text = "Got it!"

        # Send reply back to Telegram
        await context.bot.send_message(chat_id=chat_id, text=reply_text.strip())
        logger.info(f"✅ Sent response to {chat_id}")

    except requests.exceptions.Timeout:
        logger.error(f"❌ Request timeout")
        await context.bot.send_message(chat_id=chat_id, text="Sorryquest timed out. Please try again.")
    except Exception as f"❌ Error processing message: {e}")
bot"ge#() ing der(ildp(MessageND, handlegger🤖 Bot Botd   n_poll e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
