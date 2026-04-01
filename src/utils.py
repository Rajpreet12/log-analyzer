from collections import Counter
from datetime import datetime
from typing import Iterable, List, Optional

from src.parser import LogEntry


def count_by_level(entries: Iterable[LogEntry]) -> dict:
    return dict(Counter(entry.level for entry in entries))


def filter_entries(
    entries: Iterable[LogEntry],
    level: Optional[str] = None,
    contains: Optional[str] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    **kwargs,
) -> List[LogEntry]:
    items = list(entries)

    if start is None:
        start = kwargs.get("since") or kwargs.get("after")
    if end is None:
        end = kwargs.get("until") or kwargs.get("before")

    if level is not None:
        level = level.upper()
        items = [e for e in items if e.level == level]

    if contains is not None:
        needle = contains.lower()
        items = [e for e in items if needle in e.message.lower()]

    if start is not None:
        items = [e for e in items if e.timestamp >= start]

    if end is not None:
        items = [e for e in items if e.timestamp <= end]

    return items


def summarize(entries: Iterable[LogEntry]) -> dict:
    items = list(entries)

    if not items:
        return {
            "total": 0,
            "by_level": {},
            "first": None,
            "last": None,
        }

    timestamps = [e.timestamp for e in items]

    return {
        "total": len(items),
        "by_level": count_by_level(items),
        "first": min(timestamps).isoformat(),
        "last": max(timestamps).isoformat(),
    }
