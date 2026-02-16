from datetime import datetime
from patcher import in_maintenance_window

def test_window_normal_range_true():
    now = datetime(2026, 2, 11, 2, 0)
    assert in_maintenance_window("01:00", "03:00", now) is True

def test_window_normal_range_false():
    now = datetime(2026, 2, 11, 4, 0)
    assert in_maintenance_window("01:00", "03:00", now) is False

def test_window_cross_midnight_true():
    now = datetime(2026, 2, 11, 1, 0)
    assert in_maintenance_window("23:00", "02:00", now) is True
