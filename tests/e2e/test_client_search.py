from src.ui.flows.client_flow import ClientFlow
from src.ui.pages.search_results_page import SearchResultsPage


def test_client_can_open_search_results(page, cfg, logger):
    logger.info("TEST START: client can open search results")

    flow = ClientFlow(cfg)
    flow.open_root(page)
    flow.search(page, "Одеса", "Кишинів", "12-03-2026")

    logger.info("STEP: wait results loaded")
    results = SearchResultsPage(page)
    results.wait_loaded()

    assert results.trips_count() > 0 or results.has_no_routes_block()

    logger.info("TEST END: search results page opened successfully")