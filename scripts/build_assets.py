"""Build the SVG images used in the profile README.

  assets/header-{light,dark}.svg            slim navy header
  assets/card-<slug>-{light,dark}.svg       one card per selected project

GitHub shows the light or dark file to match the viewer's theme.
Edit PROFILE / PROJECTS below, then run:  python scripts/build_assets.py
No third-party packages needed (Pillow, if installed, measures text more exactly).
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

PROFILE = {
    "name": "Harsh Patil",
    "role": "Operations, Data & Automation",
    "areas": ["Ad Operations", "Supply Chain Analytics"],
}

PROJECTS = [
    {"slug": "inventory-lp", "area": "SUPPLY CHAIN",
     "title": "Optimal Inventory Control",
     "desc": "Linear programming model for inventory decisions",
     "context": "M.Sc. coursework, SRH"},
    {"slug": "customer-personality", "area": "MARKETING ANALYTICS",
     "title": "Customer Personality Analysis",
     "desc": "Customer segmentation with clustering for targeted marketing; Streamlit app",
     "context": "Internship, Ai Variant"},
    {"slug": "sentiment", "area": "NLP",
     "title": "Sentiment Analysis of Customer Reviews",
     "desc": "NLP on 568k Amazon reviews, six models compared; Streamlit app",
     "context": "Internship, Ai Variant"},
    {"slug": "insurance", "area": "REGRESSION",
     "title": "Insurance Premium Analysis",
     "desc": "Regression models to predict medical costs; interactive dashboard",
     "context": "Internship, Ai Variant"},
    {"slug": "smart-ats", "area": "LLM APPLICATION",
     "title": "Smart ATS",
     "desc": "Resume vs. job description checker using an LLM (OpenAI API, Streamlit)",
     "context": "Personal project"},
]

# Navy, one muted brass accent, neutral greys.
NAVY = "#1B2A41"
BANNER = {"bg": NAVY, "name": "#FFFFFF", "role": "#D4B27A", "text": "#D5DCE5", "muted": "#9AA7B8"}
THEMES = {
    "light": {"frame": "#D0D7DE", "card": "#FFFFFF", "border": "#D0D7DE", "title": NAVY,
              "text": "#424A53", "muted": "#6E7781", "accent": "#8A6A3B"},
    "dark": {"frame": "#30363D", "card": "#0D1117", "border": "#30363D", "title": "#E6EDF3",
             "text": "#C9D1D9", "muted": "#8B949E", "accent": "#D4B27A"},
}

try:
    from PIL import ImageFont
    _FONTS = {b: ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf", 10)
              for b in (False, True)}
except Exception:  # Pillow or font missing: fall back to an estimate
    _FONTS = {}


def width(s, size, bold=False):
    """Text width in px. DejaVu is wider than system UI fonts, so this errs safe."""
    f = _FONTS.get(bold)
    return f.getlength(s) * size / 10 if f else len(s) * size * (0.62 if bold else 0.56)


def wrap(s, size, max_w, bold=False):
    lines, line = [], ""
    for w in s.split():
        if width(f"{line} {w}".strip(), size, bold) <= max_w:
            line = f"{line} {w}".strip()
        else:
            lines.append(line)
            line = w
    return lines + [line] if line else lines


def text(x, y, s, size, fill, weight=400, anchor="start", spacing=None):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{ls}>{escape(s)}</text>')


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>{body}</svg>\n')


def banner(th):
    W, H, b, p = 1200, 200, BANNER, PROFILE
    parts = [
        f'<rect width="{W}" height="{H}" rx="10" fill="{b["bg"]}"/>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{THEMES[th]["frame"]}"/>',
        text(64, 92, p["name"], 50, b["name"], 600, spacing="-0.5"),
        text(64, 132, p["role"], 22, b["role"], 400, spacing="0.3"),
        f'<rect x="64" y="152" width="36" height="2" fill="{b["role"]}"/>',
        text(W - 64, 80, "FOCUS", 13, b["muted"], 600, "end", spacing="2"),
        text(W - 64, 112, p["areas"][0], 21, b["name"], 400, "end"),
        text(W - 64, 140, p["areas"][1], 21, b["name"], 400, "end"),
    ]
    return svg(W, H, "".join(parts), f'{p["name"]}: {p["role"]}. Focus: ' + ", ".join(p["areas"]) + ".")


def card(p, th):
    c = THEMES[th]
    W, H, pad = 520, 226, 28
    parts = [
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" fill="{c["card"]}" stroke="{c["border"]}"/>',
        text(pad, 44, p["area"], 13, c["accent"], 600, spacing="1.8"),
    ]
    y = 80
    for line in wrap(p["title"], 23, W - 2 * pad, True)[:2]:
        parts.append(text(pad, y, line, 23, c["title"], 600))
        y += 30
    for line in wrap(p["desc"], 17, W - 2 * pad)[:2]:
        parts.append(text(pad, y + 2, line, 17, c["text"]))
        y += 25
    fy = H - 26
    parts.append(text(pad, fy, p["context"], 15, c["muted"]))
    parts.append(text(W - pad, fy, "View repository →", 15, c["title"], 500, "end"))
    return svg(W, H, "".join(parts), f'{p["title"]}: {p["desc"]} ({p["context"]})')


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.svg"):
        f.unlink()
    for th in THEMES:
        (OUT / f"header-{th}.svg").write_text(banner(th), encoding="utf-8")
        for p in PROJECTS:
            (OUT / f'card-{p["slug"]}-{th}.svg').write_text(card(p, th), encoding="utf-8")
    print("Wrote", len(list(OUT.glob("*.svg"))), "SVG files to", OUT)
