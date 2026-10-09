
import logging
from wzgram import Client, filters
import config

logging.basicConfig(level=logging.INFO)

app = Client(
    "mini_leech_bot",
    api_id=config.TELEGRAM_API,
    api_hash=config.TELEGRAM_HASH,
    bot_token=config.BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def handle_start(client, message):
    if not message.from_user:
        return

    if message.from_user.id != config.OWNER_ID:
        return

    await message.reply_text(
        "Mini Advance Leech Bot is online and active!"
    )

if __name__ == "__main__":
    print("Starting bot...")
    app.run()