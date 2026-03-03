from __future__ import annotations

from dataclasses import dataclass
from playwright.sync_api import Page


@dataclass
class BasePage:
    page: Page

    def goto(self, url: str) -> None:
        self.page.goto(url)