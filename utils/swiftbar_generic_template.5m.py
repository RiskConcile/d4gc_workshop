#!/usr/bin/env python3
# <bitbar.title>iRail Liveboard</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>RiskConcile Workshop Participant</bitbar.author>
# <bitbar.desc>Shows NMBS/SNCB liveboard for a station (updates frequently).</bitbar.desc>
# <bitbar.dependencies>python3,requests</bitbar.dependencies>

import datetime as dt
import requests

API_BASE = "https://api.irail.be"
UA = "irail-liveboard-swiftbar/1.1 (contact: test@riskconcile.com)"

# --- Basic config ---
# Either set STATION_ID (preferred) or STATION name
STATION_ORIGIN_ID = "BE.NMBS.008833001" # Leuven
STATION_ORIGIN = "Leuven"
STATION_DEST_ID = "BE.NMBS.008813003" # Brussels-Central
STATION_DEST = "Brussels-Central"
ARRDEP = "departure"
LANG = "en"
MAX_ROWS = 10

def _get(path, params):
    headers = {"User-Agent": UA}
    params = dict({"format": "json", "lang": LANG}, **params)
    r = requests.get(f"{API_BASE}{path}", params=params, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()

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


# Your code starts here

def get_liveboard():
    return

def passes_by(vehicle_id, target):
    return

 
# -----------------------------------------------------------------

def main():
    try:
        data = get_liveboard()
    except Exception as e:
        print("🚂 iRail: error"); print("---"); print(str(e)); return

    key = "departures" if ARRDEP == "departure" else "arrivals"
    rows = (data.get(key, {}) or {}).get(key[:-1], [])
    if isinstance(rows, dict):
        rows = [rows]

    # ------- NEW: apply via filter using vehicle endpoint -------
    filtered = []
    for item in rows:
        vehicle_id = item.get("vehicle")
        try:
            if passes_by(vehicle_id, STATION_DEST):
                filtered.append(item)
        except Exception:
            # If vehicle lookup fails, just skip that item
            pass
        if len(filtered) >= MAX_ROWS:
            break
    rows = filtered
    # ------------------------------------------------------------
    if len(rows) > 0:
        print(f"🚂 Next Departure: {fmt_time(rows[0].get('time'))}")
        print("---")
    else:
        print("No matching trains (via Brussels-Central)."); return

    # Render lines
    href = "https://irail.be/"
    for item in rows:
        ts = item.get("time")
        when = fmt_time(ts) if ts else "??:??"
        dest = item.get("station", "?")
        platform = (item.get("platform", {}) or {}).get("name") if isinstance(item.get("platform"), dict) else item.get("platform") or "?"
        delay = fmt_delay(item.get("delay", 0))
        canceled = str(item.get("canceled", "0")) in ("1", "true", "True")
        status = "❌" if canceled else ("⏱" if delay else "•")
        print(f"{status} {when}  {dest}  (pf {platform}) {delay} | href={href}")

    print("---")
    print("Refresh now ↻ | refresh=true")

if __name__ == "__main__":
    main()
