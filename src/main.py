import sys
import os
import time

# Setup per importare il modulo core
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Importiamo la classe semplificata
try:
    from core.subject import WifiMonitor
except ImportError:
    sys.path.append(os.path.join(current_dir, 'src'))
    from core.subject import WifiMonitor

def main():
    print("--- TEST DI CONNETTIVITÀ DOCKER LINUX ---")
    print("Obiettivo: Verificare che Docker veda l'antenna USB.")
    print("-" * 50)

    monitor = WifiMonitor()

    while True:
        # 1. Esegui la scansione
        success, output = monitor.simple_linux_scan()

        # 2. Analizza il risultato
        if success:
            # Se l'output è vuoto o ha solo l'intestazione, non ha trovato reti
            if len(output.strip().split('\n')) <= 1:
                print("⚠️  nmcli funziona ma NON vede reti. L'antenna è collegata?")
            else:
                print("✅ SUCCESSO! Reti rilevate:")
                print(output) # Stampa la tabella grezza di nmcli
        else:
            print("❌ FALLIMENTO.")
            print(output) # Stampa l'errore

        print("\n" + "-"*30 + "\n")
        time.sleep(5)

if __name__ == "__main__":
    main()