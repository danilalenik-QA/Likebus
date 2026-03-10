from __future__ import annotations

from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from src.core.config import AppConfig, load_config
from src.core.logger import get_logger


@pytest.fixture(scope="session")
def cfg() -> AppConfig:
    return load_config()


@pytest.fixture(scope="session")
def logger():
    return get_logger("e2e")


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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    yield

    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        artifacts_dir = Path("artifacts")
        artifacts_dir.mkdir(exist_ok=True)

        file_name = f"{request.node.name}.png"
        page.screenshot(path=str(artifacts_dir / file_name), full_page=True)