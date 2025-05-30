from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
from datetime import datetime
import os
from PIL import Image
from urllib.parse import quote, unquote
from handlers.functions import *





async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "sobre":
        keyboard = [
            [InlineKeyboardButton("Faça o pedido aqui!", callback_data="fazer_pedido")],
            [InlineKeyboardButton("Sair", callback_data="sair")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=(
                "🍕 *Bem-vindo à Saulo's Pizzaria!*\n\n"
                "Desde nossa inauguração, combinamos ingredientes frescos e receitas artesanais para entregar a melhor experiência em pizzas. "
                "Nosso forno à lenha garante sabor e crocância únicos!\n\n"
                "Temos opções tradicionais, veganas, sem glúten e muito mais. E claro: delivery rápido, atendimento caloroso e aquele cheirinho irresistível no ar!\n\n"
                "Escolha uma opção abaixo:"
            ),
            reply_markup=reply_markup
        )

    elif query.data == "fazer_pedido":
        dia = datetime.now().weekday()
        texto, imagem_png = None, None

        if dia == 6:
                texto, imagem_png = await domingo()
        elif dia == 0:
                await query.edit_message_text("Estamos fechados às segundas-feiras!")
                return
        elif dia == 1:
                texto, imagem_png = await terca()
        elif dia == 2:
                texto, imagem_png = await quarta()
        elif dia == 3:
                texto, imagem_png = await quinta()
        elif dia == 4:
                texto, imagem_png = await sexta()
        elif dia == 5:
            texto, imagem_png = await sabado()
        else:
            await query.edit_message_text("Dia inválido.")
            return

        print(f"[DEBUG] Caminho da imagem: {imagem_png}")
        print(f"[DEBUG] Existe? {os.path.exists(imagem_png)}")
        print(f"[DEBUG] Tamanho (bytes): {os.path.getsize(imagem_png) if os.path.exists(imagem_png) else 'Arquivo não encontrado'}")        
  

        with open(imagem_png, 'rb') as f:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=f,
                caption=texto,
                parse_mode="Markdown"
        )
        
        texto_cardapio, imagem_cardapio = await textopadrao()
    
            
        keyboard = [
        [
            InlineKeyboardButton("Quero a promoção", callback_data="escolher_promocao"),
            InlineKeyboardButton("Montar meu pedido", callback_data="montar_pedido")
        ],
            [InlineKeyboardButton("❌ Cancelar Pedido", callback_data="cancelar_pedido")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(imagem_cardapio, 'rb') as f:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=f,
                caption=texto_cardapio,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )

    elif query.data == "horario":
        await query.edit_message_text("Nosso horário de atendimento é de *Terça a Domingo*, das *19h às 00h*.")

    elif query.data == "sair":
        await query.edit_message_text("Até logo! Esperamos você em breve novamente por aqui.")

    elif query.data == "escolher_promocao":
        PROMOCOES = {
            "sunday": {
                "descricao": "Na compra de 1 Pizza Grande, ganhe 1 refri grátis!",
                "quantidade_pizzas": 1,
                 "preco": 39.90,
                "quantidade_refrigerantes": 1,
                "categorias_permitidas": ["tradicionais", "BEBIDAS PROMOCAO 1L"],
               
            },
            "tuesday": {
                "descricao": "Combo Pizza grande + brotinho de chocolate + 1 Refrigerante 1 litro, Por apenas $49,90!",
                 "preco": 49.90,
                "quantidade_pizzas": 1,
                "quantidade_refrigerantes": 1,
                "categorias_permitidas": ["tradicionais","BEBIDAS PROMOCAO 1L"]
              
            },
            "wednesday": {
                "descricao": "Combo Individual Pizza brotinho + 1 Coca-lata, Por apenas $19,90!",
                 "preco": 19.90,
                "quantidade_pizzas": 1,
                "quantidade_refrigerantes": 1,
                "categorias_permitidas": ["tradicionais","doces", "BEBIDAS PROMOCAO LATA"]
            
            },
            "thursday": {
                "descricao": "2 Pizzas Grandes + 1 Refrigerante 1 litro por R$79,90",
                 "preco": 79.90,
                "quantidade_pizzas": 2,
                "quantidade_refrigerantes": 1,
                "categorias_permitidas": ["tradicionais", "doces", "BEBIDAS PROMOCAO 1L"]
             
            },
             "friday": {
                "descricao": "Combo Família 3 Pizzas Grandes + Refrigerante 2 litros, Por apenas $100,00",
                 "preco": 100.00,
                "quantidade_pizzas": 3,
                "quantidade_refrigerantes": 1,
                "categorias_permitidas": ["tradicionais", "doces", "BEBIDAS PROMOCAO 2L"]
          
             },
             "saturday": {
                "descricao": "Combo Especial Sabores Especiais + Refrigerante 1 litro, Por apenas $50,00!",
                 "preco": 50.90,
                "quantidade_pizzas": 1,
                "categorias_permitidas": ["especiais", "BEBIDAS PROMOCAO 1L" ]
                
             }
        }
        dia = datetime.now().strftime("%A").lower()
        promocao = PROMOCOES.get(dia)

        if not promocao:
            await safe_edit_message_text(query, "Não há promoção ativa hoje.")
            return

        context.user_data["promo_ativa"] = promocao
        context.user_data["pedido_promo"] = set()
        categorias = promocao["categorias_permitidas"]
        selecionados = context.user_data["pedido_promo"]
        reply_markup = gerar_botoes_categoria(categorias, selecionados)

        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"Promoção ativa: *{promocao['descricao']}*\n\n"
                    f"Selecione até *{promocao['quantidade_pizzas']}* sabor(es) das categorias *{', '.join([c.capitalize() for c in categorias])}*:"
                ),
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )

    elif query.data.startswith("toggle_"):
        item = query.data.replace("toggle_", "")
        pedido = context.user_data.get("pedido_promo", set())
        promocao = context.user_data.get("promo_ativa", {})
        categorias = promocao.get("categorias_permitidas", [])



        CATEGORIAS_PIZZA = {"tradicionais", "doces", "especiais"}

      
        CATEGORIAS_BEBIDA = {
            cat for cat in categorias if cat.startswith("BEBIDAS") or cat == "bebidas"
        }

        categoria_item = next((cat for cat in categorias if item in CARDAPIO.get(cat, [])), None)
        if not categoria_item:
            await query.answer("Item inválido para essa promoção.", show_alert=True)
            return

       
        pizzas_selecionadas = [i for i in pedido if any(i in CARDAPIO.get(cat, []) for cat in CATEGORIAS_PIZZA)]
        bebidas_selecionadas = [i for i in pedido if any(i in CARDAPIO.get(cat, []) for cat in CATEGORIAS_BEBIDA)]

        limite_pizzas = promocao.get("quantidade_pizzas", 0)
        limite_bebidas = promocao.get("quantidade_refrigerantes", 0)

        if item in pedido:
            pedido.remove(item)
        else:
            if categoria_item in CATEGORIAS_PIZZA:
                if len(pizzas_selecionadas) >= limite_pizzas:
                    await query.answer(f"Você já selecionou {limite_pizzas} pizza(s).", show_alert=True)
                    return
            elif categoria_item in CATEGORIAS_BEBIDA:
                if len(bebidas_selecionadas) >= limite_bebidas:
                    await query.answer(f"Você já selecionou {limite_bebidas} bebida(s).", show_alert=True)
                    return
            pedido.add(item)

        context.user_data["pedido_promo"] = pedido

        reply_markup = gerar_botoes_categoria(categorias, pedido)
        texto_msg = (
            f"🍕 Promoção ativa: *{promocao['descricao']}*\n\n"
            f"Selecione até:\n"
            f"{promocao[]}"
            
        )
        await safe_edit_message_text(query, texto_msg, reply_markup=reply_markup, parse_mode="Markdown")
    elif query.data.startswith("livre_toggle:"):
        await query.answer()
        item = unquote(query.data.split(":", 1)[1]).strip().lower()

        pedido = context.user_data.get("pedido_livre", set())
        if item in (s.lower() for s in pedido):
            pedido = {s for s in pedido if s.lower() != item}
        else:
            pedido.add(item)

        context.user_data["pedido_livre"] = pedido
        reply_markup = gerar_botoes_categoria_livre(["tradicionais", "especiais", "doces", "bebidas"], pedido)

        await safe_edit_message_text(query, "🍕 *Monte seu pedido livremente!*", reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "livre_finalizar":
        pedido_raw = context.user_data.get("pedido_livre", set())

        if not pedido_raw:
            await query.answer("Você ainda não selecionou itens.", show_alert=True)
            return

     
        pedido = set()
        for item_preco in CARDAPIO_PRECOS:
            if item_preco.strip().lower() in {p.strip().lower() for p in pedido_raw}:
                pedido.add(item_preco)

        total = 0.0
        texto = "📋 *Resumo do Pedido Livre*\n\n"

        for item in sorted(pedido):
            preco = CARDAPIO_PRECOS.get(item, 0.0)
            total += preco
            texto += f"• {item} — R$ {preco:.2f}\n"

        texto += f"\n💰 *Total:* R$ {total:.2f}\n"
        texto += "\nSelecione a forma de pagamento abaixo:"

        botoes = [
            [
                InlineKeyboardButton("💳 Cartão de Crédito", callback_data="pagamento_cartao"),
                InlineKeyboardButton("💵 Dinheiro", callback_data="pagamento_dinheiro")
            ],
            [InlineKeyboardButton("🔁 PIX", callback_data="pagamento_pix")],
            [InlineKeyboardButton("❌ Cancelar Pedido", callback_data="cancelar_pedido")]
        ]
        reply_markup = InlineKeyboardMarkup(botoes)

        await safe_edit_message_text(
            query,
            texto,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif query.data == "montar_pedido":
        await montar_pedido_livre(update, context)

    elif query.data == "pagar_pedido":
        await query.answer("Pagamento registrado!", show_alert=True)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="✅ Pedido pago com sucesso! Obrigado por comprar na Saulo’s Pizzaria 🍕"
        )
        context.user_data["pedido_livre"] = set()  

    elif query.data == "cancelar_pedido":
        await query.answer("Pedido cancelado.", show_alert=True)

        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Pedido cancelado. Você pode iniciar um novo quando quiser."
        )

     
        context.user_data.clear() 
        
      
        context.user_data["pedido_livre"] = set()  

       
        limpar_sessao_usuario(context)

    elif query.data == "finalizar_pedido":
        pedido = context.user_data.get("pedido_promo", set())
        promocao = context.user_data.get("promo_ativa", {})

        if not pedido:
            await query.answer("Você ainda não selecionou itens para o pedido.", show_alert=True)
            return

        preco = promocao.get("preco", 0.0)
        descricao = promocao.get("descricao", "Promoção Especial")

        texto = (
            f"📦 *Resumo do Pedido Promocional*\n\n"
            f"📝 *Descrição:* {descricao}\n"
            f"🍕 *Itens Selecionados:*\n"
        )

        for item in pedido:
            texto += f"• {item}\n"

        texto += f"\n💰 *Total:* R$ {preco:.2f}\n"
        texto += "\nSelecione a forma de pagamento abaixo:"

    
        botoes = [
            [
                InlineKeyboardButton("💳 Cartão de Crédito", callback_data="pagamento_cartao"),
                InlineKeyboardButton("💵 Dinheiro", callback_data="pagamento_dinheiro")
            ],
            [InlineKeyboardButton("🔁 PIX", callback_data="pagamento_pix")],
            [InlineKeyboardButton("❌ Cancelar Pedido", callback_data="cancelar_pedido")]
        ]
        reply_markup = InlineKeyboardMarkup(botoes)

        await safe_edit_message_text(
            query,
            texto,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

  
     

    elif query.data == "escolher_pagamento_promo":
        await query.answer()
        
        botoes = InlineKeyboardMarkup([
            [InlineKeyboardButton("💸 PIX", callback_data="pagamento_pix")],
            [InlineKeyboardButton("💵 Dinheiro", callback_data="pagamento_dinheiro")],
            [InlineKeyboardButton("💳 Cartão de Crédito", callback_data="pagamento_cartao")]
            [InlineKeyboardButton("❌ Cancelar Pedido", callback_data="cancelar_pedido")]
        ])

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🧾 *Escolha a forma de pagamento:*",
            reply_markup=botoes,
            parse_mode="Markdown"
        )
   

    elif query.data in ["pagamento_pix", "pagamento_cartao", "pagamento_dinheiro"]:
        await query.answer()


        tipo_pagamento = query.data.replace("pagamento_", "").replace("_livre", "")
        tipo_pedido = "livre" if "_livre" in query.data else "promo"

      
        context.user_data["forma_pagamento"] = tipo_pagamento
        context.user_data["tipo_pedido"] = tipo_pedido
        context.user_data["esperando_endereco"] = True

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="📍 *Informe o endereço para entrega:*",
            parse_mode="Markdown"
        )
        await update.message.reply_text(texto, parse_mode="Markdown")
        limpar_sessao_usuario(context)
