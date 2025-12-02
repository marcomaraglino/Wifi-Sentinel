import sys
import os
import time

# TRUCCO PER I PERCORSI:
# Aggiungiamo la cartella corrente al path di Python per trovare i moduli 'core'
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from core.subject import WifiMonitor
except ImportError as e:
    # Fallback se eseguiamo dalla root del progetto
    sys.path.append(os.path.join(current_dir, 'src'))
    from core.subject import WifiMonitor

def main():
    print("--- WI-FI SENTINEL (TEST MODE) ---")
    print("Premi CTRL+C per fermare la scansione.\n")
    
    # 1. ISTANZIA IL MONITOR
    # mock_mode=False forza l'uso di 'netsh' su Windows
    monitor = WifiMonitor(mock_mode=False)
    
    # Creiamo un finto observer per vedere i dati a video
    class SimplePrinter:
        def update(self, data):
            print(f"\n[OBSERVER] Ricevuti dati di {len(data)} reti:")
            for network in data:
                # Controlliamo se questa è la rete a cui siamo connessi
                # Se 'is_connected' è True, mettiamo la spunta verde
                is_connected = network.get('is_connected', False)
                prefix = "✅ CONNESSO ->" if is_connected else "   Rete     ->"
                
                # Stampiamo i dati incolonnati
                ssid = network.get('ssid')
                bssid = network.get('bssid')
                signal = network.get('signal')
                
                print(f"{prefix} SSID: {ssid:<25} | BSSID: {bssid} | Segnale: {signal}")

    # 2. COLLEGA L'OBSERVER
    printer = SimplePrinter()
    monitor.register_observer(printer)
    
    # 3. AVVIA IL MONITOR
    try:
        # Intervallo di 5 secondi
        monitor.start_monitoring(interval=5)
    except KeyboardInterrupt:
        print("\n\n[SYSTEM] Test interrotto dall'utente. Uscita.")

if __name__ == "__main__":
    main()