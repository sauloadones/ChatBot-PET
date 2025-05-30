from telegram import Update
from telegram.ext import ContextTypes
from handlers.functions import *
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    if context.user_data.get("esperando_endereco"):
        # Salva e desativa o estado de espera
        context.user_data["endereco"] = texto
        context.user_data["esperando_endereco"] = False

        # Coleta dados do pedido
        forma = context.user_data.get("forma_pagamento", "Não especificada")
        tipo = context.user_data.get("tipo_pedido", "promo")

        # Mensagem de confirmação
        mensagem = (
            f"✅ *Pedido recebido com sucesso!*\n\n"
            f"🛒 Tipo: {'Pedido Livre' if tipo == 'livre' else 'Promoção'}\n"
            f"💳 Pagamento: {forma}\n"
            f"📍 Endereço: {texto}\n\n"
            f"🚚 Seu pedido será entregue em breve!"
        )

        await update.message.reply_text(mensagem, parse_mode="Markdown")

        limpar_sessao(context)

        await start(update, context)
    else:
        # Caso o bot não esteja esperando um endereço
        await update.message.reply_text(f"📨 Você disse: {texto}")
