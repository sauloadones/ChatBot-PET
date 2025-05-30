from telegram import Update
from telegram.ext import ContextTypes
from handlers.functions import *
from telegram import Update
from telegram.ext import ContextTypes


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from handlers.functions import limpar_sessao, start
    texto = update.message.text.strip()

    if context.user_data.get("esperando_endereco"):
        # Salva o endereço e finaliza o estado de espera
        context.user_data["endereco"] = texto
        context.user_data["esperando_endereco"] = False

        forma = context.user_data.get("forma_pagamento", "Não especificada")
        tipo = context.user_data.get("tipo_pedido", "promo")

        mensagem = (
            f"✅ *Pedido recebido com sucesso!*\n\n"
            f"🛒 Tipo: {'Pedido Livre' if tipo == 'livre' else 'Promoção'}\n"
            f"💳 Pagamento: {forma}\n"
            f"📍 Endereço: {texto}\n\n"
            f"🚚 Seu pedido será entregue em breve!"
        )

        await update.message.reply_text(mensagem, parse_mode="Markdown")
        limpar_sessao(context)
        

    else:
     
        # Qualquer nova mensagem fora do fluxo de pedido reinicia a conversa
        limpar_sessao(context)
        await update.message.reply_text(
            "🔄 Nova mensagem detectada. Reiniciando conversa...",
            parse_mode="Markdown"
        )
        await start(update, context)

