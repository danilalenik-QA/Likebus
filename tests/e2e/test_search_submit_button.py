from datetime import date, timedelta
from src.ui.flows.client_flow import ClientFlow


def _tomorrow_dd_mm_yyyy() -> str:
    d = date.today() + timedelta(days=1)
    return d.strftime("%d-%m-%Y")


def test_search_submit_triggers_navigation(page, cfg):
    flow = ClientFlow(cfg)
    flow.open_root(page)

    before = page.url
    flow.search(page, "Одеса", "Кишинів", _tomorrow_dd_mm_yyyy())

    assert page.url != before