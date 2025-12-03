from abc import ABC, abstractmethod

# bozza di observer che riceve aggiornamenti dal subject (Monitor)
class Observer(ABC):
    @abstractmethod
    def update(self, network_data):
        pass

class Subject(ABC):
    """
    Interfaccia base per il Monitor.
    Definisce come gestire la lista di chi ascolta (gli observer).
    In pratica c'è solo un observer (riceve dati -> cerca evil twin -> manda alert)
    però in teoria potrebbero essercene più di uno con compiti differenti
    (così rispettiamo il requisito non funzionale di estensibilità). 
    """
    def __init__(self):
        self._observers = []

    def register_observer(self, observer: Observer):
        """Aggiunge un osservatore alla lista."""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        """Rimuove un osservatore dalla lista."""
        self._observers.remove(observer)

    def notify_observers(self, data):
        """
        Avvisa tutti gli osservatori registrati.
        Questo metodo viene chiamato quando lo scanner trova nuove reti.
        """
        for observer in self._observers:
            observer.update(data)