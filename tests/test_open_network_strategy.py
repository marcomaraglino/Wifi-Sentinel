import json
from pathlib import Path
import pytest
from src.strategies.open_network import OpenNetworkStrategy

DATA_PATH = Path(__file__).parent / "data" / "mock_wifi.json"

@pytest.fixture
def networks():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def strategy():
    return OpenNetworkStrategy()

def test_mock_networks(strategy, networks):
    wifi_casa, free_wifi_open = networks

    assert strategy.validate(wifi_casa) is False      # WPA2 → sicura
    assert strategy.validate(free_wifi_open) is True  # None → pericolosa