# conftest.py (configuração do pytest)
import pytest
import pygame

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Inicializa pygame para os testes e finaliza após"""
    pygame.init()
    yield
    pygame.quit()

def pytest_configure(config):
    """Configuração adicional do pytest"""
    config.addinivalue_line(
        "markers", "slow: marca teste como lento (pular com -m 'not slow')"
    )