from __future__ import annotations

from dataclasses import dataclass

from src.core.config import AppConfig
from src.ui.pages.root_page import RootPage


@dataclass
class ClientFlow:
    cfg: AppConfig

    def open_root(self, page) -> RootPage:
        root = RootPage(page=page)
        root.goto(self.cfg.base_url)  # https://like99.akstor.com.ua/
        root.assert_loaded()
        root.accept_cookies_if_present()
        return root