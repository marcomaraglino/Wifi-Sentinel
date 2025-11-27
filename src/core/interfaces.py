from abc import ABC, abstractmethod

# STRATEGY PATTERN: Interfaccia per le strategie di validazione
class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, network_data: dict) -> bool:
        """
        Ritorna True se la rete è PERICOLOSA, False se è sicura.
        """
        pass