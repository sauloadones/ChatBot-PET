# bot.py
from handlers.start import start
from telegram.ext import CallbackQueryHandler
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv
from handlers.callbacks import handle_callback
from handlers.functions import *

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    print(os.path.exists("imagens_convertidas/promocao-domingo.jpg"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gerenciar_primeira_interacao))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    
    print("Bot está rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
