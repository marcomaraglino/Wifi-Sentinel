import time
import subprocess
import random
from .interfaces import Subject

class WifiMonitor(Subject):
    def __init__(self, mock_mode=True):
        """
        Inizializza il Monitor.
        parametro mock_mode: Se True, usa dati finti. 
        Se False, prova a usare la scheda Wi-Fi reale.
        """
        super().__init__()
        self.mock_mode = mock_mode
        self.is_running = False

    def start_monitoring(self, interval=5):
        """
        Avvia il ciclo infinito di scansione ad intervalli regolari.
        """
        self.is_running = True
        print(f"[MONITOR] Avvio monitoraggio ogni {interval} secondi (Mock Mode: {self.mock_mode})")
        
        while self.is_running:
            # 1. Esegui la scansione
            networks = self.scan_networks()
            
            # 2. Se troviamo reti, notifichiamo TUTTI gli observer
            if networks:
                self.notify_observers(networks) # da interfaces.py
            else:
                print("[MONITOR] Nessuna rete trovata (o errore scansione).")

            #3. Aspetta intervallo prima di scansionare di nuovo
            time.sleep(interval)

    def scan_networks(self):
        """
        Sceglie quale metodo di scansione usare.
        """
        if self.mock_mode:
            return self._scan_mock()
        else:
            return self._scan_real_linux()

    def _scan_mock(self):
        """
        GENERA DATI FINTI.
        Da usare per test e sviluppo.
        """
        print("[MONITOR] --- Scansione SIMULATA ---")
        
        # Simuliamo una variazione casuale del segnale per sembrare reale
        signal_strength = random.randint(40, 90)
        
        return [
            {
                "ssid": "WiFi_Casa_Sicura",
                "bssid": "AA:BB:CC:11:22:33",
                "signal": signal_strength,
                "encryption": "WPA2"
            },
            {
                # Questa rete simula un Evil Twin (stesso nome di una nota, ma aperta o diversa)
                "ssid": "Free_Public_WiFi",
                "bssid": "DEAD:BEEF:00:00", 
                "signal": signal_strength - 10,
                "encryption": "None" 
            }
        ]

    def _scan_real_linux(self):
        """
        ESEGUE IL COMANDO REALE SU LINUX.
        Usa 'nmcli' (Network Manager CLI) che è standard su molti sistemi Linux.
        """
        print("[MONITOR] --- Scansione REALE (nmcli) ---")
        try:
            # Eseguiamo: nmcli -t -f SSID,BSSID,SIGNAL,SECURITY dev wifi list
            # -t: output tabulare
            # -f: specifica i campi che vogliamo
            cmd = ['nmcli', '-t', '-f', 'SSID,BSSID,SIGNAL,SECURITY', 'dev', 'wifi', 'list']
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"[ERROR] nmcli ha restituito un errore: {result.stderr}")
                return []

            networks = []
            # Analizziamo l'output riga per riga
            for line in result.stdout.strip().split('\n'):
                # nmcli con -t usa ':' come separatore. 
                # Nota: i BSSID contengono ':', quindi bisogna fare attenzione al parsing.
                # Esempio output: MyWifi:AA\:BB\:CC\:11\:22\:33:80:WPA2
                
                # Una tecnica robusta è un po' complessa, per ora usiamo una tecnica semplice:
                # Poiché sappiamo l'ordine dei campi (SSID, BSSID, SIGNAL, SECURITY), proviamo a splittare.
                # Attenzione: Questo è un parsing semplificato.
                
                parts = line.split(':')
                
                # Se il parsing è difficile a causa dei due punti nel MAC address,
                # un trucco è usare nmcli senza -t e parsare le colonne a larghezza fissa,
                # oppure ricostruire il BSSID. 
                
                # Per questo stadio del progetto, se la stringa è complessa, 
                # potremmo saltarla o gestirla meglio in una feature successiva.
                
                if len(parts) >= 2:
                    # Costruiamo un dizionario grezzo
                    networks.append({
                        "raw_data": line, # Utile per debug
                        "ssid": parts[0],
                        # Nota: il BSSID reale va estratto meglio in futuro
                        "bssid_fragment": parts[1], 
                        "encryption": parts[-1]
                    })

                # Metodo da migliorare
            
            return networks

        except FileNotFoundError:
            print("[ERROR] Comando 'nmcli' non trovato. Stai eseguendo su Linux con NetworkManager installato?")
            return []
        except Exception as e:
            print(f"[ERROR] Eccezione durante la scansione: {e}")
            return []