from __future__ import annotations

from dataclasses import dataclass
from playwright.sync_api import expect

from .base_page import BasePage


@dataclass
class RootPage(BasePage):
    def assert_loaded(self) -> None:
        expect(self.page.locator("body")).to_be_visible()

    def accept_cookies_if_present(self) -> None:
        candidates = [
            "button:has-text('Прийняти')",
            "button:has-text('Принять')",
            "button:has-text('Accept')",
            "button:has-text('OK')",
        ]
        for sel in candidates:
            loc = self.page.locator(sel)
            try:
                if loc.first.is_visible(timeout=500):
                    loc.first.click()
                    break
            except Exception:
                pass