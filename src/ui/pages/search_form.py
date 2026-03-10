from __future__ import annotations

from dataclasses import dataclass
from playwright.sync_api import expect

from .base_page import BasePage


@dataclass
class SearchForm(BasePage):
    def _from_input(self):
        return self.page.locator(".routeForm .search_field1, .routeForm input[name='from']").first

    def _to_input(self):
        return self.page.locator(".routeForm .search_field2, .routeForm input[name='to']").first

    def _date_input(self):
        return self.page.locator(".routeForm input[name='date']").first

    def _submit_button(self):
        return self.page.locator(".routeForm button.j-route_sbm.s_f_button[type='submit']").first

    def _visible_dropdown(self):
        return self.page.locator(".autocomplete-suggestions").filter(has=self.page.locator(".autocomplete-suggestion")).last

    def _select_city(self, input_locator, city: str) -> None:
        expect(input_locator).to_be_visible(timeout=8000)

        input_locator.click()
        input_locator.fill("")
        input_locator.type(city[:3], delay=80)

        dropdown = self._visible_dropdown()
        expect(dropdown).to_be_visible(timeout=8000)

        option = dropdown.locator(".autocomplete-suggestion", has_text=city).first
        expect(option).to_be_visible(timeout=8000)
        option.click()

        self.page.wait_for_timeout(300)

    def select_from(self, city: str) -> None:
        self._select_city(self._from_input(), city)

    def select_to(self, city: str) -> None:
        self._select_city(self._to_input(), city)

    def select_date(self, value: str) -> None:
        dd_mm_yyyy = value.replace("-", ".")

        inp = self._date_input()
        expect(inp).to_be_visible(timeout=8000)

        self.page.eval_on_selector(
            ".routeForm input[name='date']",
            """(el, v) => {
                el.removeAttribute('readonly');
                el.value = v;
                el.setAttribute('data-v', v);
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                el.blur();
            }""",
            dd_mm_yyyy,
        )

        self.page.wait_for_timeout(300)

    def submit(self) -> None:
        btn = self._submit_button()
        expect(btn).to_be_visible(timeout=8000)

        with self.page.expect_navigation(timeout=15000):
            btn.click()