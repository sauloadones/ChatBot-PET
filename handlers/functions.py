from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from urllib.parse import quote
from telegram.ext import ContextTypes
from handlers.start import start
from handlers.message import responder 
async def domingo():
   text = ("Bem vindo a Saulo's Pizzaria!,\n"
           "Nossa promoção de hoje é:\n"
           "Na compra de 1 Pizza Grande, ganhe 1 refri grátis!\n"
           "Aproveite")
   imagem = "imagens_convertidas/promocao-domingo.jpg"
   return text, imagem

async def terca():
   text = ("Bem vindo a Saulo's Pizzaria!,\n"
           "Nossa promoção de hoje é:\n"
           "Combo Pizza grande + brotinho de chocolate + 1 Refrigerante 1 litro, Por apenas $49,90!\n"
           "Aproveite")
   imagem = "imagens_convertidas/promocao-terca.jpg"
   return text, imagem

async def quarta():
   text = ("Bem vindo a Saulo's Pizzaria!,\n"
           "Nossa promoção de hoje é:\n"
           "Combo Individual Pizza brotinho + 1 Coca-lata, Por apenas $19,90!\n"
           "Aproveite")
   imagem = "imagens_convertidas/promocao-quarta.jpg"
   return text, imagem

async def quinta():
   text = ("Bem vindo a Saulo's Pizzaria!\n"
           "Nossa promoção de hoje é:\n"
           "Combo 2 Pizzas Grande + 1 Refrigerante 1 litro, Por apenas $79,90!\n"
           "Aproveite")
   imagem = "imagens_convertidas/promocao-quinta.jpg"
   return text, imagem

async def sexta():
   text = ("Bem vindo a Saulo's Pizzaria!,\n"
           "Nossa promoção de hoje é:\n"
           "Combo Família 3 Pizzas Grandes + Refrigerante 2 litros, Por apenas $100,00!\n"
           "Aproveite")
   imagem = "imagens_convertidas/promocao-sexta.jpg"
   return text, imagem

async def sabado():
   text = ("Bem vindo a Saulo's Pizzaria!,\n"
           "Nossa promoção de hoje é:\n"
           "Combo Especial Sabores Especiais + Refrigerante 1 litro, Por apenas $50,00!\n"
           "Aproveite")
   imagem = "imagens_convertidas/promocao-sabado.jpg"
   return text, imagem


async def textopadrao():
    text = (
        "📋 *Cardápio Saulo’s Pizzaria:*\n\n"
        "🍕 *Tradicionais:*\n"
        "- Mussarela — R$ 30,00\n"
        "- Calabresa — R$ 32,00\n"
        "- Frango c/ Catupiry — R$ 34,00\n\n"
        "🍕 *Especiais:*\n"
        "- Portuguesa — R$ 38,00\n"
        "- Quatro Queijos — R$ 40,00\n"
        "- Pepperoni — R$ 42,00\n\n"
        "🍕 *Doces:*\n"
        "- Chocolate — R$ 28,00\n"
        "- Romeu e Julieta — R$ 30,00\n\n"
        "🥤 *Bebidas:*\n"
        "- Refrigerante Lata — R$ 6,00\n"
        "- Suco Natural — R$ 8,00\n"
        "- Refrigerante 2L - R$ 12,00\n"
    )
    imagem = "imagens_convertidas/cardapio.jpg"
    return text, imagem

CARDAPIO = {
    "tradicionais": ["Mussarela", "Calabresa", "Frango c/ Catupiry"],
    "especiais": ["Portuguesa", "Quatro Queijos", "Pepperoni"],
    "doces": ["Chocolate", "Romeu e Julieta"],
    "bebidas": [ "Suco Natural", "Coca-cola 2L", "Guarana 2L", "Pepsi 2L", "Coca-Cola 1L", "Guarana 1L", "Pepsi 1L", "Coca-Cola Lata", "Guarana Lata", "Pepsi Lata"],
    "BEBIDAS PROMOCAO 2L": ["Coca-Cola 2L", "Guarana 2L", "Pepsi 2L"],
    "BEBIDAS PROMOCAO 1L": ["Coca-Cola 1L", "Guarana 1L", "Pepsi 1L"],
    "BEBIDAS PROMOCAO LATA": ["Coca-Cola Lata", "Guarana Lata", "Pepsi Lata"]
}
CARDAPIO_PRECOS = {
    # Tradicionais
    "Mussarela": 30.00,
    "Calabresa": 32.00,
    "Frango c/ Catupiry": 34.00,
    # Especiais
    "Portuguesa": 38.00,
    "Quatro Queijos": 40.00,
    "Pepperoni": 42.00,
    # Doces
    "Chocolate": 28.00,
    "Romeu e Julieta": 30.00,
    # Bebidas
    "Suco Natural": 8.00,
    "Coca-cola 2L": 12.00,
    "Guarana 2L": 12.00,
    "Pepsi 2L": 12.00,
    "Coca-Cola 1L": 8.00,
    "Guarana 1L": 8.00,
    "Pepsi 1L": 8.00,
    "Coca-Cola Lata": 6.00,
    "Guarana Lata": 6.00,
    "Pepsi Lata": 6.00
}


def gerar_botoes_categoria(categorias, selecionados):
    botoes = []

    for categoria in categorias:
        botoes.append([InlineKeyboardButton(f"📂 {categoria.upper()}", callback_data="ignore")])
        for item in CARDAPIO[categoria]:
            marcado = "✅" if item in selecionados else "⬜"
            botoes.append([InlineKeyboardButton(f"{marcado} {item}", callback_data=f"toggle_{item}")])
    
    botoes.append([InlineKeyboardButton("✅ Finalizar pedido", callback_data="finalizar_pedido")])
    return InlineKeyboardMarkup(botoes)

async def safe_edit_message_text(query, text, **kwargs):
    try:
        if query.message.text:
            await query.edit_message_text(text=text, **kwargs)
        else:
            await query.message.reply_text(text, **kwargs)
    except Exception as e:
        print("[ERRO edit_message_text]", e)


def gerar_botoes_categoria_livre(categorias, selecionados):
    botoes = []
    selecionados_normalizados = {s.strip().lower() for s in selecionados}

    for categoria in categorias:
        # Cabeçalho da categoria (sem ação no clique)
        botoes.append([InlineKeyboardButton(f"📂 {categoria.upper()}", callback_data="ignore")])
        
        # Botões de itens
        for item in CARDAPIO.get(categoria, []):
            chave = item.strip().lower()
            marcado = "✅" if chave in selecionados_normalizados else "⬜"
            callback = f"livre_toggle:{quote(item)}"

            botoes.append([
                InlineKeyboardButton(
                    f"{marcado} {item}",
                    callback_data=callback
                )
            ])

    # Botão de finalizar pedido
    botoes.append([InlineKeyboardButton("✅ Finalizar pedido", callback_data="livre_finalizar")])
    return InlineKeyboardMarkup(botoes)

async def montar_pedido_livre(update, context):
    # Inicializa o conjunto no contexto, se ainda não existir
    context.user_data.setdefault("pedido_livre", set())
    categorias = ["tradicionais", "especiais", "doces", "bebidas"]
    selecionados = context.user_data["pedido_livre"]

    # Gera o teclado com base nos itens já selecionados (se houver)
    reply_markup = gerar_botoes_categoria_livre(categorias, selecionados)

    # Envia a mensagem inicial
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*Selecione os itens do seu pedido:*",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def montar_resumo_pedido_livre(context):
    pedido = context.user_data.get("pedido_livre", set())

    if not pedido:
        return "🛒 *Seu pedido está vazio.*"

   
    categorias = {
        "tradicionais": [],
        "especiais": [],
        "doces": [],
        "bebidas": [],
    }

   
    nome_para_categoria = {}
    nome_original = {}

    for categoria, itens in CARDAPIO.items():
        if categoria not in categorias:
            continue
        for item in itens:
            chave = item.strip().lower()
            nome_para_categoria[chave] = categoria
            nome_original[chave] = item 

 
    for item in pedido:
        chave = item.strip().lower()
        if chave in nome_para_categoria:
            categoria = nome_para_categoria[chave]
            categorias[categoria].append(nome_original[chave])

  
    texto = "📋 *Resumo do Pedido*\n\n"
    for categoria, itens in categorias.items():
        if itens:
            texto += f"*{categoria.capitalize()}*:\n"
            texto += "\n".join(f"• {item}" for item in itens) + "\n\n"

    return texto.strip()

def montar_resumo_pedido_promocao(context):
    pedido = context.user_data.get("pedido_promo", set())
    if not pedido:
        return "🛒 *Você ainda não selecionou itens para esta promoção.*"

    # Mapeamento reverso para achar o preço dos itens
    preco_total = 0
    linhas = []
    for categoria, itens in CARDAPIO.items():
        for item in itens:
            if item in pedido:
                if " — R$ " in item:
                    nome, preco = item.split(" — R$ ")
                    preco = float(preco.replace(",", "."))
                else:
                    nome = item
                    preco = 0
                preco_total += preco
                linhas.append(f"• {item}")

    texto = "🎁 *Resumo do Pedido Promocional:*\n\n"
    texto += "\n".join(linhas)
    texto += f"\n\n💰 *Total:* R$ {preco_total:.2f}"

    return texto.strip()

def gerar_botoes_pagamento(tipo="promo"): 
    sufixo = "" if tipo == "promo" else "_livre"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💳 Cartão de Crédito", callback_data=f"pagamento_cartao{sufixo}"),
            InlineKeyboardButton("💵 Dinheiro", callback_data=f"pagamento_dinheiro{sufixo}")
        ],
        [InlineKeyboardButton("🔁 PIX", callback_data=f"pagamento_pix{sufixo}")],
        [InlineKeyboardButton("❌ Cancelar Pedido", callback_data=f"cancelar_pedido{sufixo}")]
    ])

async def receber_endereco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("esperando_endereco"):
        endereco = update.message.text.strip()
        context.user_data["endereco"] = endereco
        context.user_data["esperando_endereco"] = False

        forma = context.user_data.get("forma_pagamento", "Não especificada")
        tipo = context.user_data.get("tipo_pedido", "promo")

        texto = (
            f"✅ *Pedido recebido com sucesso!*\n\n"
            f"🛒 Tipo: {'Pedido Livre' if tipo == 'livre' else 'Promoção'}\n"
            f"💳 Pagamento: {forma}\n"
            f"📍 Endereço: {endereco}\n\n"
            f"🚚 Seu pedido será entregue em breve!"
        )

        await update.message.reply_text(texto, parse_mode="Markdown")


async def gerenciar_primeira_interacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("ja_iniciou"):
        context.user_data["ja_iniciou"] = True
        await start(update, context)
    else:
        await responder(update, context)
