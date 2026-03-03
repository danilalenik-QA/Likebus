def test_open_base_url(page, cfg):
    page.goto(cfg.base_url)
    # минимальная проверка: страница открылась
    assert page.url.startswith(cfg.base_url)