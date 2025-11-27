from src.core.interfaces import ValidationStrategy

class OpenNetworkStrategy(ValidationStrategy):
    def validate(self, network_data: dict) -> bool:
        # Logica semplice: Se la cifratura è "None", è pericolosa
        if network_data.get("Encryption") == "None":
            return True
        return False