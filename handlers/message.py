from telegram import Update
from telegram.ext import ContextTypes

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    if context.user_data.get("esperando_endereco"):
        context.user_data["endereco"] = texto
        context.user_data["esperando_endereco"] = False

        forma = context.user_data.get("forma_pagamento", "Não especificada")
        tipo = context.user_data.get("tipo_pedido", "promo")

        mensagem = (
            f"✅ *Pedido recebido com sucesso!*\n\n"
            f"💳 Pagamento: {forma}\n"
            f"📍 Endereço: {texto}\n\n"
            f"🚚 Seu pedido será entregue em breve!"
        )

        await update.message.reply_text(mensagem, parse_mode="Markdown")
    else:
        await update.message.reply_text(f"📨 Você disse: {texto}")
