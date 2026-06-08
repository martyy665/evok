import sys
import pytest
from unittest.mock import MagicMock

# Break the modbus_slave ↔ config circular import by stubbing evok.config before
# any evok.modbus_slave import happens.
sys.modules.setdefault('evok.config', MagicMock())


def test_devtype_names_exists():
    from evok.devices import devtype_names
    assert isinstance(devtype_names, dict)


def test_devtype_names_covers_standard_types():
    from evok.devices import devtype_names, num_to_devtype_name
    for name in num_to_devtype_name.values():
        assert name in devtype_names, f"'{name}' missing from devtype_names"
        assert devtype_names[name] == name


def test_devtype_names_used_in_mqtt_handler_import():
    # This will fail with ImportError until the fix is applied
    from evok.handler_mqtt import MqttHandler  # noqa — just checks the import resolves


# ── Register.check_new_data() ────────────────────────────────────────────────

def _make_register(initial_cache_value):
    """Build a Register with a mock arm whose cache returns initial_cache_value."""
    from evok.modbus_slave import Register

    arm = MagicMock()
    arm.modbus_slave.modbus_cache_map.get_register.return_value = [initial_cache_value]
    arm.modbus_address = 1

    return Register("test_40000", arm, 0, 40000)


def test_register_has_check_new_data():
    from evok.modbus_slave import Register
    assert hasattr(Register, 'check_new_data'), "Register must expose check_new_data for event emission"
    assert callable(Register.check_new_data)


async def test_register_check_new_data_fires_on_first_read():
    """First scan: _last_value is None, cached value is 0 → change detected."""
    reg = _make_register(0)
    assert reg._last_value is None
    assert await reg.check_new_data() is True
    assert reg._last_value == 0


async def test_register_check_new_data_no_fire_on_same_value():
    """Second scan with same value → no change."""
    reg = _make_register(0)
    await reg.check_new_data()                  # None → 0, fires
    assert await reg.check_new_data() is False  # 0 → 0, silent


async def test_register_check_new_data_fires_on_value_change():
    """Value changes 0 → 55 → event fires; then 55 → 55 → no event."""
    from evok.modbus_slave import Register

    arm = MagicMock()
    arm.modbus_address = 1
    cache = [0]
    arm.modbus_slave.modbus_cache_map.get_register.side_effect = lambda *a, **kw: [cache[0]]

    reg = Register("test_40000", arm, 0, 40000)
    await reg.check_new_data()   # None → 0

    cache[0] = 55
    assert await reg.check_new_data() is True   # 0 → 55: fires
    assert reg._last_value == 55
    assert await reg.check_new_data() is False  # 55 → 55: silent


async def test_register_check_new_data_no_fire_on_cache_miss():
    """ENoCacheRegister → regvalue() returns None; _last_value stays None → no change."""
    from evok.errors import ENoCacheRegister
    from evok.modbus_slave import Register

    arm = MagicMock()
    arm.modbus_address = 1
    arm.modbus_slave.modbus_cache_map.get_register.side_effect = ENoCacheRegister("no data")

    reg = Register("test_40000_miss", arm, 0, 40000)
    assert await reg.check_new_data() is False  # None → None: silent


async def test_register_eventable_via_board_parse(monkeypatch):
    """parse_feature_register() must register the Register as an eventable device."""
    from evok.modbus_slave import Register, Board, ModbusSlave
    from evok import devices as dev_module

    slave = MagicMock(spec=ModbusSlave)
    slave.eventable_devices = []
    slave.modbus_cache_map = MagicMock()
    slave.modbus_cache_map.get_register.return_value = [0]

    board = Board.__new__(Board)
    board.circuit = "internal_40000"
    board.modbus_address = 1
    board.major_group = 1
    board.legacy_mode = True
    board.modbus_slave = slave

    monkeypatch.setattr(dev_module.Devices, 'register_device', lambda *a, **kw: None)

    board.parse_feature_register(2, {'type': 'REGISTER', 'start_reg': 40000, 'count': 2})

    assert len(slave.eventable_devices) == 2
    for dev in slave.eventable_devices:
        assert isinstance(dev, Register)
        assert hasattr(dev, 'check_new_data')
