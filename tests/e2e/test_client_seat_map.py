from src.ui.flows.client_flow import ClientFlow
from src.ui.pages.search_results_page import SearchResultsPage
from src.ui.pages.seat_map_page import SeatMapPage


def test_client_can_open_seat_map_and_select_seat(page, cfg, logger):
    logger.info("TEST START: client can open seat map and select seat")

    flow = ClientFlow(cfg)
    flow.open_root(page)
    flow.search(page, "Одеса", "Кишинів", "12-03-2026")

    results = SearchResultsPage(page)
    results.wait_loaded()
    results.select_first_trip()

    seat_map = SeatMapPage(page)
    seat_map.wait_loaded()

    available = seat_map.available_seats_count()
    logger.info("STEP: available seats = %s", available)

    assert available > 0

    seat_map.select_first_seat()

    selected = seat_map.selected_seats_count()
    logger.info("STEP: selected seats = %s", selected)

    assert selected == 1

    logger.info("TEST END: seat map works correctly")