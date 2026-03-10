from __future__ import annotations
import re
from dataclasses import dataclass
from playwright.sync_api import expect

from .base_page import BasePage


@dataclass
class SearchResultsPage(BasePage):
    def _trip_boxes(self):
        return self.page.locator(".Trip-box")

    def _no_route(self):
        return self.page.locator(".noRoute")

    def _sorting_count(self):
        return self.page.locator(".sorting-count")

    def _bbc_container(self):
        return self.page.locator("#bbc-routes-container")

    def _bs_container(self):
        return self.page.locator("#bs-routes-container")

    import re

    def wait_loaded(self) -> None:
        # Базовая проверка: страница результатов открылась
        expect(self.page).to_have_url(re.compile(r".*/route/.*"))

        # Ждём, пока либо появились рейсы, либо появился блок "нет рейсов"
        self.page.wait_for_function(
            """() => {
                return document.querySelectorAll('.Trip-box').length > 0
                    || document.querySelector('.noRoute') !== null
                    || document.querySelector('#bbc-routes-container') !== null
                    || document.querySelector('#bs-routes-container') !== null;
            }""",
            timeout=15000,
        )

    def trips_count(self) -> int:
        return self._trip_boxes().count()

    def has_no_routes_block(self) -> bool:
        return self._no_route().count() > 0 and self._no_route().first.is_visible()

    def select_first_trip(self):
        trip = self.page.locator(".Trip-box").first
        expect(trip).to_be_visible(timeout=15000)

        btn = trip.locator(".j-selTick")
        expect(btn).to_be_visible(timeout=15000)

        btn.click()

