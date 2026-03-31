from datetime import datetime

from src.parser import parse_line


def test_parse_valid_line():
    e = parse_line("2026-03-31 10:15:42 [ERROR] connection refused")
    assert e is not None
    assert e.level == "ERROR"
    assert e.message == "connection refused"
    assert e.timestamp == datetime(2026, 3, 31, 10, 15, 42)


def test_parse_lowercase_level():
    e = parse_line("2026-03-31 10:15:42 [info] ok")
    assert e is not None
    assert e.level == "INFO"


def test_parse_invalid_line():
    assert parse_line("garbage") is None
    assert parse_line("") is None


def test_parse_bad_date():
    assert parse_line("2026-13-99 10:15:42 [INFO] x") is None
