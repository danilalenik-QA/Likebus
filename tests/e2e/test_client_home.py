from src.ui.flows.client_flow import ClientFlow


def test_root_loads(page, cfg):
    flow = ClientFlow(cfg)
    flow.open_root(page)