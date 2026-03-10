from src.ui.flows.client_flow import ClientFlow
from src.ui.pages.search_results_page import SearchResultsPage


def test_client_can_open_trip(page, cfg):

    flow = ClientFlow(cfg)

    flow.open_root(page)

    flow.search(page, "Одеса", "Кишинів", "12-03-2026")

    results = SearchResultsPage(page)
    results.wait_loaded()

    results.select_first_trip()

    # проверяем что открылась страница выбора мест
    assert (
        "seat" in page.url
        or page.locator(".seat, .bus-seat, .seatmap").count() > 0
    )