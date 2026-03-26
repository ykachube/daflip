#!/usr/bin/env python3
"""
Split-Flap Display Web App
Run: pip install flask requests  &&  python app.py
Then open: http://localhost:5000
"""

from flask import Flask, jsonify, send_from_directory
import requests, datetime, random, os, json

app = Flask(__name__, static_folder="static")

# ── Content sources ────────────────────────────────────────────────────────────

QUOTES = [
    ("STAY HUNGRY\nSTAY FOOLISH", "STEVE JOBS"),
    ("THE ONLY WAY\nTO DO GREAT WORK\nIS TO LOVE IT", "STEVE JOBS"),
    ("IN THE MIDDLE\nOF DIFFICULTY\nLIES OPPORTUNITY", "EINSTEIN"),
    ("SIMPLICITY IS\nTHE ULTIMATE\nSOPHISTICATION", "DA VINCI"),
    ("DONE IS BETTER\nTHAN PERFECT", "ZUCKERBERG"),
    ("MOVE FAST AND\nBREAK THINGS", "ZUCKERBERG"),
    ("THE FUTURE\nIS ALREADY HERE\nJUST UNEVENLY\nDISTRIBUTED", "GIBSON"),
    ("BE THE CHANGE\nYOU WISH TO\nSEE IN THE WORLD", "GANDHI"),
    ("IMAGINATION IS\nMORE IMPORTANT\nTHAN KNOWLEDGE", "EINSTEIN"),
    ("LIFE IS WHAT\nHAPPENS WHILE\nYOU MAKE PLANS", "LENNON"),
    ("TWO ROADS\nDIVERGED IN\nA WOOD AND I\nTOOK THE ONE\nLESS TRAVELED", "FROST"),
    ("FIRST SOLVE\nTHE PROBLEM\nTHEN WRITE\nTHE CODE", "JOHNSON"),
    ("TALK IS CHEAP\nSHOW ME THE CODE", "TORVALDS"),
    ("ANY SUFFICIENTLY\nADVANCED TECH\nIS INDISTINGUISHABLE\nFROM MAGIC", "CLARKE"),
]

def get_weather():
    """Fetch weather from wttr.in (no API key needed)."""
    try:
        r = requests.get("https://wttr.in/?format=j1", timeout=4)
        d = r.json()
        area   = d["nearest_area"][0]["areaName"][0]["value"]
        region = d["nearest_area"][0]["region"][0]["value"]
        current= d["current_condition"][0]
        temp_f = current["temp_F"]
        temp_c = current["temp_C"]
        desc   = current["weatherDesc"][0]["value"].upper()
        humidity = current["humidity"]
        wind_mph = current["windspeedMiles"]
        lines = [
            f"{area.upper()}, {region.upper()[:12]}",
            f"{temp_f}F / {temp_c}C",
            desc[:20],
            f"HUMIDITY {humidity}%",
            f"WIND {wind_mph} MPH",
        ]
        return "\n".join(lines), "WEATHER"
    except Exception:
        return None, None

def get_time_panel():
    now = datetime.datetime.now()
    lines = [
        now.strftime("%A").upper(),
        now.strftime("%B %d %Y").upper(),
        now.strftime("%I:%M %p").upper().lstrip("0"),
        "─" * 14,
        "HAVE A GREAT DAY",
    ]
    return "\n".join(lines), "TIME & DATE"

def get_fun_fact():
    facts = [
        ("A DAY ON VENUS\nIS LONGER THAN\nA YEAR ON VENUS", "SPACE FACT"),
        ("HONEY NEVER\nSPOILS FOUND IN\n3000 YR OLD TOMBS", "FUN FACT"),
        ("OCTOPUSES HAVE\nTHREE HEARTS AND\nBLUE BLOOD", "FUN FACT"),
        ("THE EIFFEL TOWER\nGROWS 6 INCHES\nIN SUMMER HEAT", "FUN FACT"),
        ("A GROUP OF\nFLAMINGOS IS\nCALLED A FLAMBOYANCE", "FUN FACT"),
        ("THERE ARE MORE\nSTARS THAN GRAINS\nOF SAND ON EARTH", "SPACE FACT"),
        ("CROWS CAN\nRECOGNIZE AND\nREMEMBER FACES", "ANIMAL FACT"),
        ("BANANAS ARE\nTECHNICALLY BERRIES\nBUT STRAWBERRIES\nARE NOT", "FOOD FACT"),
    ]
    text, src = random.choice(facts)
    return text, src

# ── Content rotation state ─────────────────────────────────────────────────────

_content_pool = []
_index = 0

def _build_pool():
    global _content_pool
    pool = []
    # Always include time
    pool.append(("time", None))
    # 3 quotes
    for q in random.sample(QUOTES, min(3, len(QUOTES))):
        pool.append(("quote", q))
    # weather
    pool.append(("weather", None))
    # 2 fun facts
    for _ in range(2):
        pool.append(("fact", None))
    random.shuffle(pool)
    _content_pool = pool

_build_pool()

@app.route("/api/content")
def api_content():
    global _index, _content_pool
    if _index >= len(_content_pool):
        _build_pool()
        _index = 0

    kind, data = _content_pool[_index]
    _index += 1

    if kind == "time":
        text, source = get_time_panel()
    elif kind == "quote":
        text, source = data
    elif kind == "weather":
        text, source = get_weather()
        if text is None:
            text, source = random.choice(QUOTES)
    else:
        text, source = get_fun_fact()

    return jsonify({"text": text, "source": source, "kind": kind})

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    print("\n  Split-Flap Display running at  http://localhost:5000\n")
    app.run(debug=False, port=5000)
