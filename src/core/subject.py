import subprocess
import platform
import time
from .interfaces import Subject

class WifiMonitor(Subject):
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.current_os = platform.system()

    def start_monitoring(self, interval=5):
        self.is_running = True
        print(f"[MONITOR] Avvio monitoraggio REALE su {self.current_os} (Intervallo: {interval}s)")
        
        while self.is_running:
            networks = self.scan_networks()
            if networks:
                self.notify_observers(networks)
            else:
                # Se vuoi evitare spam nei log quando non trova nulla, commenta la riga sotto
                print("[MONITOR] Nessuna rete rilevata.")
            
            time.sleep(interval)

    def scan_networks(self):
        """
        Esegue SOLO scansioni reali. Niente più mock.
        """
        if self.current_os == "Linux":
            return self._scan_real_linux()
        # Se volessi supportare Windows nativo in futuro, potresti aggiungere qui l'elif
        else:
            print(f"[ERROR] Sistema operativo {self.current_os} non supportato per scansione reale diretta.")
            return []

    def _get_current_connection_info_linux(self):
        """Recupera il BSSID della rete connessa su Linux."""
        try:
            cmd = ['nmcli', '-t', '-f', 'ACTIVE,BSSID', 'dev', 'wifi', 'list']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            for line in result.stdout.strip().split('\n'):
                line = line.replace(r"\:", ":")
                if line.startswith("yes"):
                    parts = line.split(":")
                    if len(parts) >= 2:
                        return ":".join(parts[1:]).strip()
            return None
        except Exception:
            return None

    def _scan_real_linux(self):
        """Scansione reale tramite nmcli."""
        try:
            connected_bssid = self._get_current_connection_info_linux()
            
            cmd = ['nmcli', '-t', '-f', 'SSID,BSSID,SIGNAL,SECURITY', 'dev', 'wifi', 'list']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"[ERROR] nmcli fallito: {result.stderr}")
                return []

            networks = []
            for line in result.stdout.strip().split('\n'):
                if not line: continue
                
                # Gestione escape dei due punti
                safe_line = line.replace(r"\:", "__COLON__")
                parts = safe_line.split(':')
                
                if len(parts) >= 4:
                    real_bssid = parts[1].replace("__COLON__", ":")
                    
                    networks.append({
                        "ssid": parts[0],
                        "bssid": real_bssid,
                        "signal": parts[2] + "%",
                        "encryption": parts[3],
                        "is_connected": (real_bssid == connected_bssid)
                    })
            return networks
        except Exception as e:
            print(f"[ERROR] Eccezione scansione Linux: {e}")
            return []