from datetime import datetime
from zoneinfo import ZoneInfo

def get_today_be() -> str:
    return datetime.now(ZoneInfo("Europe/Brussels")).strftime("%Y-%m-%d")