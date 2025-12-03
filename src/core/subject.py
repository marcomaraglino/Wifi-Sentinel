import subprocess
import platform

class WifiMonitor:
    def simple_linux_scan(self):
        """
        Esegue nmcli e restituisce l'output grezzo.
        Serve solo per capire se Docker vede l'antenna.
        """
        print("[MONITOR] Tentativo di scansione con nmcli...")
        
        try:
            # Comando base per vedere se ci sono dispositivi Wi-Fi
            # nmcli dev wifi list
            cmd = ['nmcli', 'dev', 'wifi', 'list']
            
            # Eseguiamo il comando
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Successo! Restituiamo la lista delle reti
                return True, result.stdout
            else:
                # Errore (es. comando non trovato, permessi negati)
                return False, f"ERRORE nmcli: {result.stderr}"

        except FileNotFoundError:
            return False, "ERRORE CRITICO: Il comando 'nmcli' non esiste nel container. Hai installato network-manager nel Dockerfile?"
        except Exception as e:
            return False, f"ECCEZIONE: {str(e)}"