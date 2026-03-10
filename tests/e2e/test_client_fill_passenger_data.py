from src.ui.flows.client_flow import ClientFlow
from src.ui.pages.search_results_page import SearchResultsPage
from src.ui.pages.seat_map_page import SeatMapPage


def test_client_can_fill_passenger_data(page, cfg, logger):
    logger.info("TEST START: client can fill passenger data")

    flow = ClientFlow(cfg)
    flow.open_root(page)
    flow.search(page, "Одеса", "Кишинів", "12-03-2026")

    results = SearchResultsPage(page)
    results.wait_loaded()
    results.select_first_trip()

    seat_map = SeatMapPage(page)
    seat_map.wait_loaded()
    seat_map.select_first_seat()

    logger.info("STEP: wait passenger form")
    seat_map.wait_passenger_form_loaded()

    logger.info("STEP: fill phone")
    seat_map.fill_phone("+380680000001")

    logger.info("STEP: fill first passenger")
    seat_map.fill_first_passenger(name="Ivan", surname="Ivanov")

    logger.info("TEST END: passenger data filled successfully")