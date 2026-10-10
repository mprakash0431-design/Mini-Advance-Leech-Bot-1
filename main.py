import logging
import asyncio
import config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

# ----------------- LOGGING CONFIGURATION -----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ----------------- BOT CLIENT INITIALIZATION -----------------
app = Client(
    "MiniAdvanceLeechBot",
    api_id=config.TELEGRAM_API,
    api_hash=config.TELEGRAM_HASH,
    bot_token=config.BOT_TOKEN,
    workdir="."
)

# ----------------- KEYBOARD BUILDERS -----------------

def start_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("😎 Owner", url=f"tg://user?id={config.OWNER_ID}"),
            InlineKeyboardButton("Updates Channel 🔥", url=config.AUTHOR_URL if config.AUTHOR_URL else "https://t.me/")
        ]
    ])

def main_settings_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Universal Settings", callback_data="uni_settings")],
        [InlineKeyboardButton("Leech Settings", callback_data="leech_settings")],
        [InlineKeyboardButton("Reset Setting", callback_data="reset_setting")],
        [InlineKeyboardButton("Close", callback_data="close_menu")]
    ])

def leech_settings_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Send As Media", callback_data="toggle_media"),
            InlineKeyboardButton("Thumbnail", callback_data="set_thumb")
        ],
        [
            InlineKeyboardButton("Leech Splits", callback_data="set_splits"),
            InlineKeyboardButton("Leech Caption", callback_data="set_caption")
        ],
        [
            InlineKeyboardButton("Leech Prefix", callback_data="set_prefix"),
            InlineKeyboardButton("Leech Suffix", callback_data="set_suffix")
        ],
        [
            InlineKeyboardButton("Leech Remname", callback_data="set_remname"),
            InlineKeyboardButton("Leech Dump", callback_data="set_dump")
        ],
        [
            InlineKeyboardButton("Leech Attachment", callback_data="set_attach"),
            InlineKeyboardButton("Leech Metadata", callback_data="set_meta")
        ],
        [
            InlineKeyboardButton("Audio Track", callback_data="set_audio"),
            InlineKeyboardButton("Subtitle Track", callback_data="set_sub")
        ],
        [
            InlineKeyboardButton("Back", callback_data="back_to_main"),
            InlineKeyboardButton("Close", callback_data="close_menu")
        ]
    ])

# ----------------- COMMAND HANDLERS -----------------

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    welcome_text = (
        "**Now, This bot will send all your files and links here. Start Using ...**"
    )
    await message.reply_text(welcome_text, reply_markup=start_keyboard())

@app.on_message(filters.command(["usetting", "usetting1"]))
async def settings_handler(client: Client, message: Message):
    user = message.from_user
    user_id = user.id if user else "0"
    first_name = user.first_name if user else "User"
    username = f"@{user.username}" if user and user.username else "None"

    settings_text = (
        f"**User Settings :**\n\n"
        f"**Name :** {first_name} ( `{user_id}` )\n"
        f"**Username :** {username}\n"
        f"**Telegram DC :** None\n"
        f"**Language :** English\n\n"
        f"🔄 **Available Args:**\n"
        f"• **-s** or **-set**: Set Directly via Arg"
    )
    await message.reply_text(settings_text, reply_markup=main_settings_keyboard())

# ----------------- CALLBACK QUERY HANDLER -----------------

@app.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    user = callback_query.from_user
    first_name = user.first_name if user else "User"
    user_id = user.id if user else "0"
    username = f"@{user.username}" if user and user.username else "None"

    if data == "leech_settings":
        # Formats leech settings panel matching your UI screen
        leech_text = (
            f"**Leech Settings for {first_name}**\n\n"
            f"**Daily Leech :** ∞ / ∞ per day\n"
            f"**Leech Type :** {'DOCUMENT' if config.AS_DOCUMENT else 'MEDIA'}\n"
            f"**Custom Thumbnail :** Not Exists\n"
            f"**Leech Split Size :** 3.91GB (Default)\n"
            f"**Equal Splits :** Disabled\n"
            f"**Media Group :** Disabled\n"
            f"**Leech Caption :** Not Exists\n"
            f"**Leech Prefix :** Not Exists\n"
            f"**Leech Suffix :** Not Exists\n"
            f"**Leech Logs :** Not Exists\n"
            f"**Leech Remname :** Not Exists\n"
            f"**Leech Attachment :** Not Exists\n"
            f"**Leech Metadata :** Not Exists\n"
            f"**Audio Track :** Not Exists\n"
            f"**Subtitle Track :** Not Exists\n"
            f"**Subtitle Text :** Not Exists"
        )
        await callback_query.message.edit_text(leech_text, reply_markup=leech_settings_keyboard())

    elif data == "uni_settings":
        await callback_query.answer("Universal settings option selected.", show_alert=True)

    elif data == "reset_setting":
        reset_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Yes", callback_data="confirm_reset"),
                InlineKeyboardButton("No", callback_data="leech_settings")
            ],
            [InlineKeyboardButton("Close", callback_data="close_menu")]
        ])
        await callback_query.message.edit_text("Do you want to Reset Settings ?", reply_markup=reset_markup)

    elif data == "confirm_reset":
        await callback_query.answer("Settings Reset Successfully!", show_alert=True)
        await callback_query.message.edit_text("Settings have been reset to default.", reply_markup=main_settings_keyboard())

    elif data == "back_to_main":
        settings_text = (
            f"**User Settings :**\n\n"
            f"**Name :** {first_name} ( `{user_id}` )\n"
            f"**Username :** {username}\n"
            f"**Telegram DC :** None\n"
            f"**Language :** English\n\n"
            f"🔄 **Available Args:**\n"
            f"• **-s** or **-set**: Set Directly via Arg"
        )
        await callback_query.message.edit_text(settings_text, reply_markup=main_settings_keyboard())

    elif data == "close_menu":
        await callback_query.message.delete()

    else:
        await callback_query.answer("Setting updated!", show_alert=False)

# ----------------- SCRIPT EXECUTION -----------------

if __name__ == "__main__":
    print("Starting Mini Advance Leech Bot...")
    app.run()
