from __future__ import annotations

import random

from playwright.sync_api import Page, expect


class SeatMapPage:
    def __init__(self, page: Page):
        self.page = page

        # seat map
        self.free_seats = page.locator("a.tosel.free")
        self.selected_seats = page.locator("a.theChosen")

        # contact / passenger form
        self.phone_input = page.locator("[name='tel']").first
        self.phone2_input = page.locator("[name='tel2']").first
        self.email_input = page.locator("[name='email']").first

        self.first_passenger_block = page.locator("#j-ins_passengers_1 .Pas_el").first

        self.first_passenger_surname = self.first_passenger_block.locator(
            '[name="surnamep[]"]'
        )

        self.first_passenger_name = self.first_passenger_block.locator(
            '[name="namep[]"]'
        )

        # next / payment buttons on the same route page
        self.next_button = page.locator(".r_c_go_next").first
        self.pay_button = page.locator(
            ".bbc-submit-btn, .bs-submit-btn, button[type='submit'], input[type='submit']"
        ).first

    def wait_loaded(self):
        expect(self.free_seats.first).to_be_visible(timeout=15000)

    def available_seats_count(self) -> int:
        return self.free_seats.count()

    def selected_seats_count(self) -> int:
        return self.selected_seats.count()

    def select_first_seat(self):
        available = self.available_seats_count()
        if available == 0:
            raise Exception("No free seats available")

        before_selected = self.selected_seats_count()
        self.free_seats.first.click()
        expect(self.selected_seats).to_have_count(before_selected + 1, timeout=5000)

    def select_random_seat(self):
        available = self.available_seats_count()
        if available == 0:
            raise Exception("No free seats available")

        before_selected = self.selected_seats_count()
        index = random.randint(0, available - 1)
        self.free_seats.nth(index).click()
        expect(self.selected_seats).to_have_count(before_selected + 1, timeout=5000)

    def wait_passenger_form_loaded(self):
        self.page.wait_for_function(
            """() => document.querySelectorAll('#j-ins_passengers_1 .Pas_el').length > 0""",
            timeout=15000,
        )

        expect(self.phone_input).to_be_visible(timeout=10000)
        expect(self.first_passenger_block).to_be_visible(timeout=10000)

    def fill_phone(self, phone: str):
        expect(self.phone_input).to_be_visible(timeout=10000)
        self.phone_input.click()
        self.phone_input.fill(phone)

    def fill_email(self, email: str):
        if self.email_input.count() > 0:
            self.email_input.click()
            self.email_input.fill(email)

    def fill_first_passenger(self, name: str, surname: str):
        expect(self.first_passenger_surname).to_be_visible(timeout=10000)
        expect(self.first_passenger_name).to_be_visible(timeout=10000)

        self.first_passenger_surname.fill(surname)
        self.first_passenger_name.fill(name)

    def go_next(self):
        if self.next_button.count() == 0:
            raise Exception("Next button (.r_c_go_next) not found")
        expect(self.next_button).to_be_visible(timeout=10000)
        self.next_button.click()

    def wait_acquirer_popup(self):
        popup = self.page.locator("#provider_buttons, #providerButtonsContainer").first
        expect(popup).to_be_visible(timeout=10000)

    def select_first_acquirer(self):
        acquirer_btn = self.page.locator(
            "#providerButtonsContainer .provider-account-btn:visible"
        ).first

        expect(acquirer_btn).to_be_visible(timeout=10000)
        acquirer_btn.click()

    def select_first_acquirer_and_wait_redirect(self):
        acquirer_btn = self.page.locator(
            "#providerButtonsContainer .provider-account-btn:visible"
        ).first

        expect(acquirer_btn).to_be_visible(timeout=10000)

        with self.page.expect_navigation():
            acquirer_btn.click()

        return self.page

    def go_to_payment(self):
        """
        Нажать кнопку перехода к оплате / создания заказа
        """
        submit_btn = self.page.locator(
            ".bbc-submit-btn:visible, "
            ".bs-submit-btn:visible, "
            "button:has-text('Перейти до оплати'):visible, "
            "button:has-text('Оплатити'):visible, "
            "button:has-text('Продовжити'):visible, "
            "input[type='submit']:visible"
        ).first

        expect(submit_btn).to_be_visible(timeout=10000)
        submit_btn.click()