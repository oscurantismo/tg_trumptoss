import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
GAME_SHORT_NAME = "TrumpToss"
GAME_URL = "https://oscurantismo.github.io/trumptoss/"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("👉 Play TrumpToss", callback_game={"game_short_name": GAME_SHORT_NAME})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_game(chat_id=update.effective_chat.id, game_short_name=GAME_SHORT_NAME, reply_markup=reply_markup)

def game_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.game_short_name == GAME_SHORT_NAME:
        context.bot.answer_callback_query(callback_query_id=query.id, url=GAME_URL)
    else:
        context.bot.answer_callback_query(callback_query_id=query.id, text="Unknown game 🤔")

def status(update: Update, context: CallbackContext):
    update.message.reply_text("✅ TrumpToss bot is online and running!")

def set_bot_status(bot):
    try:
        bot.set_my_description("🟢 Online – TrumpToss bot is running!")
        print("✅ Bot description updated.")
    except Exception as e:
        print("❌ Failed to set bot description:", e)

def error_handler(update, context):
    print(f"❌ Error: {context.error}")

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found.")
        return

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    set_bot_status(updater.bot)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CallbackQueryHandler(game_callback))
    dp.add_error_handler(error_handler)

    updater.start_polling()
    print("✅ Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
