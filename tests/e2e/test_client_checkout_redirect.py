from src.ui.flows.client_flow import ClientFlow
from src.ui.pages.search_results_page import SearchResultsPage
from src.ui.pages.seat_map_page import SeatMapPage

PAYMENT_DOMAINS = [
    "mono",
    "wayforpay",
    "hutko",
    "liqpay",
    "rozetkapay",
]

def test_client_checkout(page, cfg, logger):
    logger.info("TEST START: client checkout flow")

    flow = ClientFlow(cfg)
    flow.open_root(page)
    flow.search(page, "Одеса", "Кишинів", "12-03-2026")

    results = SearchResultsPage(page)
    results.wait_loaded()
    results.select_first_trip()

    seat_map = SeatMapPage(page)
    seat_map.wait_loaded()
    seat_map.select_first_seat()

    seat_map.wait_passenger_form_loaded()
    seat_map.fill_phone("+380680000001")
    seat_map.fill_first_passenger("Ivan", "Ivanov")

    logger.info("STEP: go to payment")
    seat_map.go_to_payment()

    logger.info("STEP: wait acquirer popup")
    seat_map.wait_acquirer_popup()

    logger.info("STEP: select first acquirer")
    payment_page = seat_map.select_first_acquirer_and_wait_redirect()

    logger.info("STEP: payment page url = %s", payment_page.url)

    url = payment_page.url.lower()

    assert any(domain in url for domain in PAYMENT_DOMAINS), \
        f"Unexpected payment gateway URL: {url}"

    logger.info("TEST END: redirected to valid payment gateway")