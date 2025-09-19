import time
import threading
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8361419760:AAFc2bf6Iyha0WZZVfksAPGdjACJrqO4dzI"
CHAT_ID = -1003093896581

# Config ciclo lunare
FASI = ["Luna Piena 🌕", "Fase 2", "Fase 3", "Fase 4",
        "Luna Vuota 🌑", "Fase 6", "Fase 7", "Fase 8"]
DURATA_FASE = 20 * 60  # 20 minuti in secondi
fase_attuale = 0
inizio_fase = time.time()

bot = Bot(token=TOKEN)

def ciclo_lunare():
    global fase_attuale, inizio_fase
    while True:
        fase = FASI[fase_attuale]

        if fase == "Luna Piena 🌕":
            bot.send_message(chat_id=CHAT_ID, text="🌕 È arrivata la **Luna Piena**!")
        elif fase == "Luna Vuota 🌑":
            bot.send_message(chat_id=CHAT_ID, text="🌑 È arrivata la **Luna Vuota**!")

        inizio_fase = time.time()
        time.sleep(DURATA_FASE)
        fase_attuale = (fase_attuale + 1) % len(FASI)

async def luna(update: Update, _):
    fase = FASI[fase_attuale]
    minuti_passati = int((time.time() - inizio_fase) / 60)
    await update.message.reply_text(f"Adesso siamo in: **{fase}**\n(iniziata {minuti_passati} minuti fa).", parse_mode="Markdown")

# Main
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Aggiungi comando
    app.add_handler(CommandHandler("luna", luna))

    # Thread per il ciclo lunare
    threading.Thread(target=ciclo_lunare, daemon=True).start()

    # Avvia il bot
    app.run_polling()

if __name__ == "__main__":
    main()
