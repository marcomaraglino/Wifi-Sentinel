import sys
import os
import time

# Setup per importare il modulo core
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Importiamo la classe semplificata
try:
    from core.subject import WifiMonitor
    from bot_interface import SentinelBot
except ImportError:
    sys.path.append(os.path.join(current_dir, 'src'))
    from core.subject import WifiMonitor
    from bot_interface import SentinelBot

def main():
    print("--- WI-FI SENTINEL (BOT MODE) ---")
    
    # 1. Recupera il Token e Configurazione
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("❌ ERRORE CRITICO: Manca il TELEGRAM_TOKEN nelle variabili d'ambiente!")
        print("Inseriscilo nel docker-compose.yml")
        return
        
    # 2. Inizializza il Monitor (Il Soggetto)
    monitor = WifiMonitor()
    
    # 3. Inizializza il Bot (L'Interfaccia)
    bot = SentinelBot(token, monitor)

    # 4. Avvia tutto
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Arresto del sistema.")

if __name__ == "__main__":
    main()