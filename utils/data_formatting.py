import datetime as dt

def fmt_time(ts):
    try:
        return dt.datetime.fromtimestamp(int(ts)).strftime("%H:%M")
    except Exception:
        return "??:??"

def fmt_delay(delay_seconds):
    try:
        d = int(delay_seconds)
        return "" if d <= 0 else f"+{d//60}′"
    except Exception:
        return ""