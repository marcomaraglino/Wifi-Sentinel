import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from core.subject import WifiMonitor

class SentinelBot:
    def __init__(self, token, monitor: WifiMonitor):
        self.token = token
        self.monitor = monitor
        # Creiamo l'applicazione Telegram
        self.application = Application.builder().token(self.token).build()

        # REGISTRAZIONE COMANDI
        # Qui diciamo al bot: "Quando vedi /start, usa la funzione self.start_command"
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("scan", self.scan_command))
        self.application.add_handler(CommandHandler("help", self.help_command))

    def run(self):
        """Avvia il bot in modalità Long Polling (Bloccante)"""
        print("[BOT] Avvio del Bot Telegram in corso...")
        self.application.run_polling()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user.first_name
        await update.message.reply_text(
            f"👋 Ciao {user}! Sono Wi-Fi Sentinel.\n"
            "Sono pronto a proteggere la tua rete.\n\n"
            "Comandi disponibili:\n"
            "📡 /scan - Esegui una scansione immediata\n"
            "ℹ️ /help - Mostra aiuto"
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🛡️ **Wi-Fi Sentinel Help**\n\n"
            "Questo bot analizza le reti Wi-Fi circostanti per rilevare minacce 'Evil Twin'.\n"
            "Usa /scan per vedere cosa c'è intorno a te."
        )

    async def scan_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Esegue la scansione usando il Monitor e restituisce i risultati via chat.
        """
        await update.message.reply_text("📡 Scansione in corso... attendere prego.")
        
        # Eseguiamo la scansione reale (che ora usa nmcli su Linux)
        networks = self.monitor.scan_networks()

        if not networks:
            await update.message.reply_text("❌ Nessuna rete trovata (o errore nello scanner).")
            return

        # Formattiamo il messaggio di risposta
        response = f"✅ **Scansione Completata**\n" \
                   f"Trovate {len(networks)} reti:\n\n"

        # Limitiamo a 10 reti per leggibilità
        for net in networks[:10]: 
            icon = "✅" if net.get('is_connected') else "📶"
            ssid = net.get('ssid', 'Unknown')
            signal = net.get('signal', 'N/A')
            bssid = net.get('bssid', 'N/A')
            
            # Formattazione Markdown
            response += f"{icon} **{ssid}**\n" \
                        f"   └ MAC: `{bssid}` | Sig: {signal}\n"

        await update.message.reply_text(response)