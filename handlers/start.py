
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Faça seu pedido", callback_data="fazer_pedido")],
        [InlineKeyboardButton("Conheça a pizzaria", callback_data="sobre")],
        [InlineKeyboardButton("Descubra se estamos abertos, horario de atendimento", callback_data="horario")],
        [InlineKeyboardButton("Sair", callback_data="sair")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Ola!, Escolha uma das opções abaixo",
        reply_markup=reply_markup
        )
