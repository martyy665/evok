import json
import pytest
from unittest.mock import MagicMock, patch


def test_on_close_removes_from_registered_devents():
    """on_close must remove self from registered_devents, not crash on registered_ws."""
    from evok.handlers_base import registered_devents
    from evok.handler_websocket import WebsocketHandler

    handler = WebsocketHandler.__new__(WebsocketHandler)
    registered_devents['all'] = {handler}

    # Patch stop_scanning to avoid needing real MODBUS_SLAVE devices
    with patch('evok.handler_websocket.Devices') as mock_devices:
        mock_devices.by_int.return_value = []
        handler.on_close()

    assert handler not in registered_devents.get('all', set())


def test_websocket_handler_imports_are_complete():
    """logging and traceback must be importable via the handler module."""
    import evok.handler_websocket as ws_mod
    assert hasattr(ws_mod, 'logging')
    assert hasattr(ws_mod, 'traceback')


def test_cmd_all_uses_correct_device_constants():
    """The 'all' command path must not reference undefined INPUT/RELAY names."""
    import ast, inspect, textwrap
    import evok.handler_websocket as ws_mod

    src = textwrap.dedent(inspect.getsource(ws_mod.WebsocketHandler.on_message))
    tree = ast.parse(src)
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    assert 'INPUT' not in names, "INPUT is undefined — use DI"
    assert 'RELAY' not in names, "RELAY is undefined — use RO"


# ── Register event helpers ────────────────────────────────────────────────────

def _make_ws_handler(filter_list=None):
    """Build a WebsocketHandler with a mocked write_message."""
    from evok.handler_websocket import WebsocketHandler
    handler = WebsocketHandler.__new__(WebsocketHandler)
    handler.filter = filter_list if filter_list is not None else ["default"]
    handler.write_message = MagicMock()
    return handler


def _make_register_proxy(circuit="internal_40000", value=42):
    """Proxy-like object whose full() returns a list with one register device state."""
    proxy = MagicMock()
    proxy.full.return_value = [{"dev": "register", "circuit": circuit, "value": value}]
    return proxy


# ── on_event tests ────────────────────────────────────────────────────────────

def test_on_event_register_default_filter_sends_event():
    """Default filter: register change events must be forwarded."""
    handler = _make_ws_handler()
    handler.on_event(_make_register_proxy())

    handler.write_message.assert_called_once()
    sent = json.loads(handler.write_message.call_args[0][0])
    assert any(d.get('dev') == 'register' for d in sent)


def test_on_event_register_included_in_explicit_filter():
    """Filter ['register']: register events must pass through."""
    handler = _make_ws_handler(["register"])
    handler.on_event(_make_register_proxy())

    handler.write_message.assert_called_once()
    sent = json.loads(handler.write_message.call_args[0][0])
    assert sent[0]['dev'] == 'register'
    assert sent[0]['value'] == 42


def test_on_event_register_excluded_from_filter():
    """Filter ['di', 'do']: register events must be suppressed."""
    handler = _make_ws_handler(["di", "do"])
    handler.on_event(_make_register_proxy())

    handler.write_message.assert_not_called()


def test_on_event_register_mixed_changeset():
    """Changeset with register + di: filter ['di'] passes only di."""
    handler = _make_ws_handler(["di"])
    proxy = MagicMock()
    proxy.full.return_value = [
        {"dev": "register", "circuit": "internal_40000", "value": 7},
        {"dev": "di", "circuit": "1_01", "value": 1},
    ]
    handler.on_event(proxy)

    handler.write_message.assert_called_once()
    sent = json.loads(handler.write_message.call_args[0][0])
    assert len(sent) == 1
    assert sent[0]['dev'] == 'di'


# ── cmd "all" test ────────────────────────────────────────────────────────────

async def test_cmd_all_all_filtered_includes_register():
    """cmd=all with all_filtered=true must include register devices in the response."""
    import evok.handler_websocket as ws_mod

    reg_state = {"dev": "register", "circuit": "internal_40000", "value": 99}
    di_state  = {"dev": "di",       "circuit": "1_01",            "value": 0}

    def fake_by_int(dev_type):
        if dev_type == 20:    # REGISTER int key
            m = MagicMock(); m.full.return_value = reg_state; return [m]
        if dev_type == 1:     # DI int key
            m = MagicMock(); m.full.return_value = di_state;  return [m]
        return []

    handler = _make_ws_handler()          # default filter
    handler.write_message = MagicMock()

    ws_mod.websocket_config = {"all_filtered": True}
    try:
        with patch('evok.handler_websocket.Devices') as mock_devs:
            mock_devs.by_int.side_effect = fake_by_int
            msg = json.dumps({"cmd": "all"})
            await handler.on_message(msg)
    finally:
        ws_mod.websocket_config = {}

    handler.write_message.assert_called_once()
    result = json.loads(handler.write_message.call_args[0][0])
    devs_in_result = [d['dev'] for d in result]
    assert 'register' in devs_in_result, f"register missing from all response: {devs_in_result}"
    assert 'di' in devs_in_result
