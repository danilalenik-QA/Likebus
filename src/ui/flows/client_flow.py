from __future__ import annotations

from dataclasses import dataclass


from src.core.config import AppConfig
from src.core.logger import get_logger
from src.ui.pages.root_page import RootPage
from src.ui.pages.search_form import SearchForm


@dataclass
class ClientFlow:
    cfg: AppConfig

    def __post_init__(self):
        self.logger = get_logger("client-flow")

    def open_root(self, page) -> RootPage:
        self.logger.info("STEP: open root")
        root = RootPage(page=page)
        root.goto(self.cfg.base_url)
        root.assert_loaded()
        root.accept_cookies_if_present()
        return root

    def search(self, page, from_city: str, to_city: str, date_dd_mm_yyyy: str):
        form = SearchForm(page=page)

        self.logger.info("STEP: select from = %s", from_city)
        form.select_from(from_city)

        self.logger.info("STEP: select to = %s", to_city)
        form.select_to(to_city)

        self.logger.info("STEP: select date = %s", date_dd_mm_yyyy)
        form.select_date(date_dd_mm_yyyy)

        self.logger.info("STEP: submit search")
        form.submit()

        self.logger.info("STEP: redirected to results page")
        return form