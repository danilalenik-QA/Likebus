from src.ui.flows.client_flow import ClientFlow


def test_client_search(page, cfg):
    flow = ClientFlow(cfg)
    flow.open_root(page)

    # пример даты: сегодня/завтра — подставь актуальную строку в формате dd-mm-yyyy
    flow.search(page, "Одеса", "Кишинів", "04-03-2026")

    # дальше уже будем проверять, что перешли на результаты (когда покажешь URL/DOM)
    assert "route" in page.url or "search" in page.url