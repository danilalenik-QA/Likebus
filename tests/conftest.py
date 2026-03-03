import pytest
from playwright.sync_api import sync_playwright

from src.core.config import AppConfig, load_config


@pytest.fixture(scope="session")
def cfg() -> AppConfig:
    return load_config()


@pytest.fixture(scope="session")
def browser(cfg: AppConfig):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=cfg.playwright.headless,
            slow_mo=cfg.playwright.slow_mo_ms,
        )
        yield browser
        browser.close()


@pytest.fixture()
def page(browser, cfg: AppConfig):
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(cfg.timeouts.action_ms)
    page.set_default_navigation_timeout(cfg.timeouts.navigation_ms)
    yield page
    context.close()