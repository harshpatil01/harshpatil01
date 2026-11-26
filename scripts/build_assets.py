"""Build the SVG images used in the profile README.

Generates a light and a dark version of:
  - assets/banner-{light,dark}.svg   header banner
  - assets/stack-{light,dark}.svg    tools I use, grouped
  - assets/card-<slug>-{light,dark}.svg   one card per featured project

Edit the PROFILE / STACK / PROJECTS data below, then run:
    python scripts/build_assets.py
No third-party packages needed (Pillow is used only if installed, to measure
text more precisely; otherwise a rough width estimate is used).
"""

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

# ---------------------------------------------------------------- content

PROFILE = {
    "name": "Harsh Patil",
    "role": "Operations, Data & Automation",
    "tagline": "Power Platform · Python · SQL · Power BI",
    "sub": "Ad ops automation  ·  Supply chain analytics  ·  M.Sc. SCM  ·  Hamburg",
}

# The two tracks shown on the right of the banner.
TRACKS = [
    ("AD OPERATIONS", "Campaign workflow automation", "Power Automate · Power Apps · SharePoint"),
    ("SUPPLY CHAIN", "Operations & inventory analytics", "Python · linear programming · M.Sc. SCM"),
]

STACK = [
    ("Automation", [("PA", "Power Automate"),
                    ("PP", "Power Apps"),
                    ("SP", "SharePoint"),
                    ("365", "Microsoft 365")]),
    ("Data", [("Py", "Python"),
              ("SQL", "SQL"),
              ("BI", "Power BI"),
              ("XL", "Excel")]),
    ("ML & other", [("ML", "pandas · scikit-learn"),
                    ("St", "Streamlit"),
                    ("SAP", "SAP S/4HANA"),
                    ("C", "C")]),
]

PROJECTS = [
    {
        "slug": "inventory-lp",
        "kicker": "SUPPLY CHAIN",
        "title": "Optimal Inventory Control",
        "desc": "Linear programming for inventory decisions",
        "tech": "Python · linear programming",
        "context": "Coursework · SRH University",
    },
    {
        "slug": "customer-personality",
        "kicker": "SEGMENTATION",
        "title": "Customer Personality Analysis",
        "desc": "Customer segmentation with clustering for targeted marketing, Streamlit app",
        "tech": "Python · scikit-learn · Streamlit",
        "context": "Internship · Ai Variant",
    },
    {
        "slug": "sentiment",
        "kicker": "NLP · APPLIED ML",
        "title": "Sentiment Analysis of Customer Reviews",
        "desc": "NLP on 568k Amazon reviews, six models compared, Streamlit app",
        "tech": "Python · scikit-learn · XGBoost · Streamlit",
        "context": "Internship · Ai Variant",
    },
    {
        "slug": "insurance",
        "kicker": "REGRESSION",
        "title": "Insurance Premium Analysis",
        "desc": "Regression models to predict medical costs, interactive dashboard",
        "tech": "Python · scikit-learn · Streamlit",
        "context": "Internship · Ai Variant",
    },
    {
        "slug": "smart-ats",
        "kicker": "LLM APP",
        "title": "Smart ATS",
        "desc": "LLM-based resume vs. job description checker built with Streamlit and the OpenAI API",
        "tech": "Python · OpenAI API · Streamlit",
        "context": "Personal project",
    },
]

# ---------------------------------------------------------------- themes

# Restrained palette: navy + one muted brass accent, neutral greys.
NAVY, NAVY_DEEP = "#1B2A41", "#111A29"
THEMES = {
    "light": {
        "frame": "#D9DEE5", "card": "#FFFFFF", "border": "#D9DEE5",
        "text": "#1B2A41", "muted": "#4F5B6B", "accent": "#8A6A3B",
        "tile": NAVY, "tiletext": "#FFFFFF", "link": "#1B2A41",
    },
    "dark": {
        "frame": "#2A3442", "card": "#151C28", "border": "#2A3442",
        "text": "#E8ECF1", "muted": "#9AA5B4", "accent": "#D4B27A",
        "tile": "#22304A", "tiletext": "#D4B27A", "link": "#E8ECF1",
    },
}
BANNER = {"bg1": NAVY, "bg2": NAVY_DEEP, "name": "#FFFFFF", "role": "#D4B27A",
          "tag": "#D5DCE5", "sub": "#9AA7B8", "rule": "#D4B27A", "line": "#33445E"}

# ---------------------------------------------------------------- helpers

try:
    from PIL import ImageFont

    def _font(size, bold):
        for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
                     else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                     "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
        return None
except ImportError:  # pragma: no cover
    def _font(size, bold):
        return None


def text_width(s, size, bold=False):
    """Width of a string in px. DejaVu is wider than system UI fonts, so this
    errs on the safe side (text never overflows on GitHub)."""
    f = _font(size, bold)
    if f is not None:
        return f.getlength(s)
    return len(s) * size * (0.62 if bold else 0.56)


def wrap(s, size, max_w, bold=False):
    words, lines, line = s.split(), [], ""
    for w in words:
        trial = f"{line} {w}".strip()
        if text_width(trial, size, bold) <= max_w:
            line = trial
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def t(x, y, s, size, fill, weight=400, anchor="start", spacing=None):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}>{escape(s)}</text>')


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)}</title>{body}</svg>\n')


# ---------------------------------------------------------------- banner

def banner(th):
    W, H = 1200, 300
    c, b = THEMES[th], BANNER
    parts = [
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{b["bg1"]}"/><stop offset="1" stop-color="{b["bg2"]}"/>'
        '</linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{c["frame"]}"/>',
        f'<rect x="64" y="70" width="40" height="3" fill="{b["rule"]}"/>',
        t(64, 138, PROFILE["name"], 58, b["name"], 700, spacing="-0.5"),
        t(64, 182, PROFILE["role"], 26, b["role"], 500, spacing="0.3"),
        t(64, 224, PROFILE["tagline"], 20, b["tag"], 400),
        t(64, 258, PROFILE["sub"], 18, b["sub"], 400, spacing="0.2"),
    ]
    # right column: the two tracks, separated by a thin vertical rule
    x = 790
    parts.append(f'<line x1="{x - 36}" y1="64" x2="{x - 36}" y2="{H - 64}" stroke="{b["line"]}" stroke-width="1"/>')
    for i, (label, line1, line2) in enumerate(TRACKS):
        y = 92 + i * 96
        parts.append(t(x, y, label, 15, b["role"], 700, spacing="2"))
        parts.append(t(x, y + 32, line1, 22, b["name"], 500))
        parts.append(t(x, y + 60, line2, 17, b["sub"], 400))
    return svg(W, H, "".join(parts), f'{PROFILE["name"]}: {PROFILE["role"]}')


# ---------------------------------------------------------------- stack

def stack(th):
    c = THEMES[th]
    W, H = 1200, 296
    colw, gap = 376, 36
    parts = []
    for ci, (group, tools) in enumerate(STACK):
        x0 = ci * (colw + gap)
        parts.append(f'<rect x="{x0 + 0.5}" y="0.5" width="{colw - 1}" height="{H - 1}" rx="12" '
                     f'fill="{c["card"]}" stroke="{c["border"]}"/>')
        parts.append(f'<rect x="{x0 + 24}" y="26" width="28" height="2" fill="{c["accent"]}"/>')
        parts.append(t(x0 + 24, 50, group.upper(), 14, c["accent"], 700, spacing="2"))
        for ti, (mono, name) in enumerate(tools):
            y = 70 + ti * 54
            parts.append(f'<rect x="{x0 + 24}" y="{y}" width="40" height="40" rx="8" fill="{c["tile"]}"/>')
            fs = 15 if len(mono) <= 2 else 12
            parts.append(t(x0 + 44, y + 25, mono, fs, c["tiletext"], 700, anchor="middle"))
            parts.append(t(x0 + 80, y + 27, name, 20, c["text"], 500))
    return svg(W, H, "".join(parts), "Tools: " + "; ".join(
        f'{g}: ' + ", ".join(n for _, n in tl) for g, tl in STACK))


# ---------------------------------------------------------------- cards

def card(p, th):
    c = THEMES[th]
    W, H, pad = 520, 248, 28
    inner = W - 2 * pad
    parts = [
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c["card"]}" stroke="{c["border"]}"/>',
        f'<rect x="{pad}" y="24" width="28" height="2" fill="{c["accent"]}"/>',
        t(pad, 48, p["kicker"], 13, c["accent"], 700, spacing="1.8"),
    ]
    if p["context"]:  # context label, top right, outlined
        pw = text_width(p["context"], 13, False) + 24
        px = W - pad - pw
        parts.append(f'<rect x="{px:.0f}" y="30.5" width="{pw:.0f}" height="25" rx="12.5" fill="none" '
                     f'stroke="{c["accent"]}" stroke-opacity="0.6"/>')
        parts.append(t(f"{px + pw / 2:.0f}", 47, p["context"], 13, c["muted"], 500, anchor="middle"))
    y = 88
    for line in wrap(p["title"], 25, inner, bold=True)[:2]:
        parts.append(t(pad, y, line, 25, c["text"], 700))
        y += 32
    y += 2
    for line in wrap(p["desc"], 18, inner)[:2]:
        parts.append(t(pad, y, line, 18, c["muted"]))
        y += 26
    fy = H - 26  # footer: tech left, link right
    parts.append(f'<line x1="{pad}" y1="{fy - 26}" x2="{W - pad}" y2="{fy - 26}" stroke="{c["border"]}"/>')
    parts.append(t(pad, fy, p["tech"], 15, c["muted"], 400))
    parts.append(t(W - pad, fy, "View repo →", 15, c["link"], 600, anchor="end"))
    return svg(W, H, "".join(parts), f'{p["title"]}: {p["desc"]}')


def main():
    OUT.mkdir(exist_ok=True)
    for th in THEMES:
        (OUT / f"banner-{th}.svg").write_text(banner(th), encoding="utf-8")
        (OUT / f"stack-{th}.svg").write_text(stack(th), encoding="utf-8")
        for p in PROJECTS:
            (OUT / f'card-{p["slug"]}-{th}.svg').write_text(card(p, th), encoding="utf-8")
    print("Wrote", len(list(OUT.glob("*.svg"))), "SVG files to", OUT)


if __name__ == "__main__":
    main()
