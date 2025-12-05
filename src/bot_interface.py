## riceve i comandi dall'utente e chiama i metodi del Wifi monitor

import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from core.subject import WifiMonitor

class SentinelBot:
    def __init__(self, token, monitor: WifiMonitor):
        self.token = token
        self.monitor = monitor
        self.application = Application.builder().token(self.token).build()

        # Aggiungi i gestori dei comandi
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("scan", self.scan_command))
        self.application.add_handler(CommandHandler("help", self.help_command))

        def run(self):
            """Avvia il bot in modalità long polling (bloccante)."""
            print("[BOT] Avvio del Wifi Sentinel Bot...")
            self.application.run_polling()

            # gestione dei comandi
        async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user.first_name
            await update.message.reply_text(
                f"Ciao {user}! Sono il Wifi Sentinel Bot. \n"
                "Sono pronto a proteggere la tua rete WiFi. \n\n"
                "Comandi disponibili:\n"
                "/scan - Avvia una scansione immediata\n"
                "/help - Mostra messaggio di aiuto"
            )

        async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "🛡️ **Wi-Fi Sentinel Help**\n\n"
                "Questo bot analizza le reti Wi-Fi circostanti per rilevare minacce 'Evil Twin'.\n"
                "Usa /scan per vedere cosa c'è intorno a te."
            )

        async def scan_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Esegue la scansione usando il Monitor e restituisce i risultati via chat."""
            
            await update.message.reply_text("🔍 Avvio della scansione delle reti Wi-Fi...")

            # chiamata al monitor per eseguire la scansione
            networks = self.monitor.scan_networks()

            if not networks:
                await update.message.reply_text("Nessuna rete trovata.")
                return

            response = f"**Scansione completata.**\n" \
                        f"Trovate {len(networks)} reti:\n\n"

            for net in networks[:10]:  # mostra solo le prime 10 reti per non intasare la chat
                icon = "✅" if net.get('is_connected') else "📶"
                ssid = net.get('ssid', 'Unknown SSID')
                signal = net.get('signal', 'N/A')
                bssid = net.get('bssid', 'N/A')

                response += f"{icon} SSID: {ssid}\n" \
                            f"   BSSID: {bssid}\n" \
                            f"   Signal: {signal} dBm\n\n"

            await update.message.reply_text(response, parse_mode='Markdown')

