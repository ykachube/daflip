# 🎰 Split-Flap Display

A fullscreen split-flap board for your browser — rotating quotes, live weather, fun facts, and the current time. Built with Python + Flask, no database, no API keys.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3+-black?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## Preview

![Split-Flap Display](screenshot.png)

> Fullscreen black board. Tiles flip one by one with authentic click sounds.  
> Content rotates every 12 seconds. Click anywhere to skip ahead.

---

## Features

- **Authentic flip animation** — each tile flips individually with a staggered cascade
- **Procedural click sounds** — generated via Web Audio API, no audio files needed
- **Live weather** — pulled from [wttr.in](https://wttr.in), auto-detects your location, no API key required
- **Rotating content pool** — quotes, weather, fun facts, time & date
- **Fullscreen adaptive grid** — tiles fill the entire viewport, rebuilds on window resize
- **Click to advance** — click anywhere on screen to jump to the next content

---

## Project Structure

```
flipboard/
├── app.py              # Flask server + content logic
├── requirements.txt    # Python dependencies
└── static/
    └── index.html      # Frontend (single file, no build step)
```

---

## Quick Start

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/flipboard.git
cd flipboard
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run**
```bash
python app.py
```

**4. Open your browser**
```
http://localhost:5000
```

That's it. No `.env` files, no API keys, no build tools.

---

## Configuration

Everything is at the top of `app.py`:

| Variable | Default | Description |
|---|---|---|
| `FLIP_INTERVAL` | `12000` ms | Time between content changes |
| `TILE_DELAY` | `14` ms | Stagger delay between tile flips |
| `QUOTES` | built-in list | Add your own quotes here |

To add your own quotes, edit the `QUOTES` list in `app.py`:

```python
QUOTES = [
    ("YOUR QUOTE\nGOES HERE", "AUTHOR NAME"),
    ...
]
```

---

## Content Sources

The board cycles through a shuffled pool of:

| Type | Source |
|---|---|
| **Time & Date** | Local system clock |
| **Weather** | [wttr.in](https://wttr.in) (IP-based geolocation) |
| **Quotes** | Hardcoded in `app.py` — easy to edit |
| **Fun Facts** | Hardcoded in `app.py` — easy to edit |

The pool is reshuffled each time it's exhausted, so content never repeats consecutively.

---

## Keyboard & Mouse

| Action | Effect |
|---|---|
| **Click** anywhere | Skip to next content immediately |
| **Resize window** | Grid rebuilds to fill new dimensions |

---

## Dependencies

```
flask>=2.3
requests>=2.31
```

Frontend uses only vanilla JS + CSS — no npm, no bundler.  
Font loaded from Google Fonts (`Oswald`).

---

## Running on Boot (optional)

**Windows** — create a `.bat` file:
```bat
@echo off
cd /d C:\path\to\flipboard
python app.py
```

**Linux/macOS** — add to crontab:
```bash
@reboot cd /path/to/flipboard && python app.py
```

Or use a `systemd` service for a proper daemon setup.

---

## License

MIT — do whatever you want with it.
