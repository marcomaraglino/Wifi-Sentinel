FROM python:3.9-slim

# Strumenti di sistema utili per la scansione delle reti:
# wireless-tools include 'iwconfig', network-manager include 'nmcli'
RUN apt-get update && apt-get install -y \
    wireless-tools \
    network-manager \
    && rm -rf /var/lib/apt/lists/*

    
WORKDIR /app

# Copiamo il file delle dipendenze e installiamo le librerie
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamo tutto il codice sorgente dentro il container
COPY . .

# Comando di avvio: esegue il main nella cartella src/
CMD ["python", "src/main.py"]