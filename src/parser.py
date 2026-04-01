from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    message: str
    raw: str = ""


def parse_line(line: str) -> Optional[LogEntry]:
    if not line or not line.strip():
        return None

    raw = line.rstrip("\n")
    parts = raw.strip().split(maxsplit=3)

    # Expected format:
    # YYYY-MM-DD HH:MM:SS LEVEL message...
    if len(parts) < 4:
        return None

    date_part, time_part, level_part, message = parts
    ts_str = f"{date_part} {time_part}"

    try:
        timestamp = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

    return LogEntry(
        timestamp=timestamp,
        level=level_part.strip("[]").upper(),
        message=message,
        raw=raw,
    )
