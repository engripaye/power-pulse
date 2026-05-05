from datetime import datetime, timedelta, timezone


def estimate_restoration_time(hours: int = 4) -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=hours)

