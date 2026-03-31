from datetime import datetime

from src.parser import LogEntry
from src.utils import count_by_level, filter_entries, summarize


def _e(level, msg="x", ts=None):
    ts = ts or datetime(2026, 1, 1, 12, 0, 0)
    return LogEntry(timestamp=ts, level=level, message=msg, raw=f"... [{level}] {msg}")


def test_count_by_level():
    entries = [_e("INFO"), _e("INFO"), _e("ERROR")]
    counts = count_by_level(entries)
    assert counts["INFO"] == 2
    assert counts["ERROR"] == 1


def test_filter_by_level():
    entries = [_e("INFO"), _e("ERROR"), _e("DEBUG")]
    out = list(filter_entries(entries, level="error"))
    assert len(out) == 1
    assert out[0].level == "ERROR"


def test_filter_by_time():
    entries = [
        _e("INFO", ts=datetime(2026, 1, 1)),
        _e("INFO", ts=datetime(2026, 1, 5)),
        _e("INFO", ts=datetime(2026, 1, 10)),
    ]
    out = list(filter_entries(entries, since=datetime(2026, 1, 3), until=datetime(2026, 1, 7)))
    assert len(out) == 1
    assert out[0].timestamp == datetime(2026, 1, 5)


def test_filter_contains():
    entries = [_e("INFO", msg="hello world"), _e("INFO", msg="goodbye")]
    out = list(filter_entries(entries, contains="WORLD"))
    assert len(out) == 1
    assert out[0].message == "hello world"


def test_summarize_empty():
    s = summarize([])
    assert s["total"] == 0
    assert s["first"] is None


def test_summarize():
    entries = [
        _e("INFO", ts=datetime(2026, 1, 1, 9, 0)),
        _e("ERROR", ts=datetime(2026, 1, 1, 10, 0)),
    ]
    s = summarize(entries)
    assert s["total"] == 2
    assert s["by_level"] == {"INFO": 1, "ERROR": 1}
    assert s["first"] == "2026-01-01T09:00:00"
    assert s["last"] == "2026-01-01T10:00:00"
