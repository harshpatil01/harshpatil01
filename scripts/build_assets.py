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
    "sub": "Ad ops & applied AI  ·  M.Sc. SRH Hamburg  ·  Hamburg, Germany",
}

# Flow shown on the right of the banner: what I do, in four steps.
FLOW = ["Data", "Automate", "Analyse", "Report"]

STACK = [
    ("Automation", [("PA", "Power Automate", "#0066FF"),
                    ("PP", "Power Apps", "#742774"),
                    ("SP", "SharePoint", "#038387"),
                    ("365", "Microsoft 365", "#D83B01")]),
    ("Data", [("Py", "Python", "#3776AB"),
              ("SQL", "SQL", "#336791"),
              ("BI", "Power BI", "#C9A100"),
              ("XL", "Excel", "#217346")]),
    ("ML & other", [("ML", "pandas · scikit-learn", "#150458"),
                    ("St", "Streamlit", "#E0393E"),
                    ("SAP", "SAP S/4HANA", "#0070F2"),
                    ("C", "C", "#5C6BC0")]),
]

PROJECTS = [
    {
        "slug": "sentiment",
        "kicker": "NLP · APPLIED ML",
        "title": "Sentiment Analysis of Customer Reviews",
        "desc": "NLP on 568k Amazon reviews, six models compared, Streamlit app",
        "tech": "Python · TF-IDF · scikit-learn · XGBoost · Streamlit",
        "context": None,
    },
    {
        "slug": "customer-personality",
        "kicker": "SEGMENTATION",
        "title": "Customer Personality Analysis",
        "desc": "Customer segmentation with clustering for targeted marketing, Streamlit app",
        "tech": "Python · pandas · scikit-learn · Streamlit",
        "context": "Internship · Ai Variant",
    },
    {
        "slug": "insurance",
        "kicker": "REGRESSION",
        "title": "Insurance Premium Analysis",
        "desc": "Regression models to predict medical costs, interactive dashboard",
        "tech": "Python · pandas · scikit-learn · Streamlit",
        "context": "Internship · Ai Variant",
    },
    {
        "slug": "inventory-lp",
        "kicker": "OPTIMISATION",
        "title": "Optimal Inventory Control",
        "desc": "Linear programming for inventory decisions",
        "tech": "Python · linear programming",
        "context": "Coursework · SRH University",
    },
    {
        "slug": "smart-ats",
        "kicker": "LLM APP",
        "title": "Smart ATS",
        "desc": "LLM-based resume vs. job description checker built with Streamlit and the OpenAI API",
        "tech": "Python · OpenAI API · Streamlit",
        "context": None,
    },
]

# ---------------------------------------------------------------- themes

THEMES = {
    "light": {
        "bg1": "#F4F8FB", "bg2": "#FFFFFF", "card": "#FFFFFF", "border": "#D8DEE4",
        "text": "#1F2328", "muted": "#59636E", "accent": "#0E7490", "accent2": "#2563EB",
        "pill": "#E6F4F7", "pilltext": "#0E6177", "grid": "#E3EAF0", "node": "#FFFFFF",
    },
    "dark": {
        "bg1": "#0D1117", "bg2": "#111B27", "card": "#151B23", "border": "#30363D",
        "text": "#E6EDF3", "muted": "#9198A1", "accent": "#2DD4BF", "accent2": "#58A6FF",
        "pill": "#12302F", "pilltext": "#5EEAD4", "grid": "#1C2633", "node": "#161D27",
    },
}

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
    c = THEMES[th]
    parts = [
        '<defs>'
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{c["bg1"]}"/><stop offset="1" stop-color="{c["bg2"]}"/></linearGradient>'
        f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1.3" fill="{c["grid"]}"/></pattern>'
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>',
        f'<rect x="640" width="{W-640}" height="{H}" rx="16" fill="url(#dots)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{c["border"]}"/>',
        f'<rect x="64" y="72" width="44" height="5" rx="2.5" fill="{c["accent"]}"/>',
        t(64, 140, PROFILE["name"], 58, c["text"], 700, spacing="-1"),
        t(64, 186, PROFILE["role"], 28, c["accent"], 600),
        t(64, 226, PROFILE["tagline"], 19, c["text"], 500),
        t(64, 256, PROFILE["sub"], 16, c["muted"]),
    ]

    # Flow motif: 4 nodes along a gentle diagonal, connected by arrows.
    nodes = [(720, 96), (850, 150), (980, 96), (1080, 186)]
    nw, nh = 104, 44
    for (x1, y1), (x2, y2) in zip(nodes, nodes[1:]):
        sx, sy = x1 + nw, y1 + nh / 2
        ex, ey = x2, y2 + nh / 2
        mx = (sx + ex) / 2
        parts.append(f'<path d="M{sx} {sy} C{mx} {sy}, {mx} {ey}, {ex - 6} {ey}" fill="none" '
                     f'stroke="{c["accent2"]}" stroke-width="2" stroke-dasharray="5 5" opacity="0.8"/>')
        parts.append(f'<path d="M{ex - 8} {ey - 5} L{ex} {ey} L{ex - 8} {ey + 5}" fill="none" '
                     f'stroke="{c["accent2"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    for i, ((x, y), label) in enumerate(zip(nodes, FLOW)):
        x = min(x, W - nw - 16)
        parts.append(f'<rect x="{x}" y="{y}" width="{nw}" height="{nh}" rx="10" fill="{c["node"]}" '
                     f'stroke="{c["accent"] if i == len(FLOW) - 1 else c["border"]}" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{x + 18}" cy="{y + nh / 2}" r="5" fill="{c["accent"]}"/>')
        parts.append(t(x + 30, y + nh / 2 + 5, label, 15, c["text"], 600))
    # tiny bar chart under the "Report" node
    bx, by = 1080 - 0, 186 + nh + 14
    bx = min(bx, W - nw - 16)
    for j, hgt in enumerate([14, 22, 18, 30, 26]):
        parts.append(f'<rect x="{bx + 14 + j * 16}" y="{by + 32 - hgt}" width="10" height="{hgt}" rx="2" '
                     f'fill="{c["accent"]}" opacity="{0.45 + j * 0.11:.2f}"/>')
    return svg(W, H, "".join(parts), f'{PROFILE["name"]}: {PROFILE["role"]}')


# ---------------------------------------------------------------- stack

def stack(th):
    c = THEMES[th]
    W, H = 1200, 250
    colw, gap = 376, 36
    parts = []
    for ci, (group, tools) in enumerate(STACK):
        x0 = ci * (colw + gap)
        parts.append(f'<rect x="{x0 + 0.5}" y="0.5" width="{colw - 1}" height="{H - 1}" rx="14" '
                     f'fill="{c["card"]}" stroke="{c["border"]}"/>')
        parts.append(t(x0 + 24, 40, group.upper(), 14, c["accent"], 700, spacing="1.5"))
        for ti, (mono, name, color) in enumerate(tools):
            y = 60 + ti * 46
            parts.append(f'<rect x="{x0 + 24}" y="{y}" width="34" height="34" rx="8" fill="{color}"/>')
            fs = 13 if len(mono) <= 2 else 11
            parts.append(t(x0 + 41, y + 22, mono, fs, "#FFFFFF", 700, anchor="middle"))
            parts.append(t(x0 + 72, y + 23, name, 17, c["text"], 500))
    return svg(W, H, "".join(parts), "Tools: " + "; ".join(
        f'{g}: ' + ", ".join(n for _, n, _ in tl) for g, tl in STACK))


# ---------------------------------------------------------------- cards

def card(p, th):
    c = THEMES[th]
    W, H, pad = 600, 230, 28
    inner = W - 2 * pad
    parts = [
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{c["card"]}" stroke="{c["border"]}"/>',
        f'<rect x="0.5" y="0.5" width="6" height="{H - 1}" rx="3" fill="{c["accent"]}"/>',
        t(pad, 44, p["kicker"], 13, c["accent"], 700, spacing="1.5"),
    ]
    title_lines = wrap(p["title"], 25, inner, bold=True)[:2]
    y = 80
    for line in title_lines:
        parts.append(t(pad, y, line, 25, c["text"], 700))
        y += 32
    y += 2
    for line in wrap(p["desc"], 17, inner)[:2]:
        parts.append(t(pad, y, line, 17, c["muted"]))
        y += 25
    # footer: tech on the left, context pill on the right
    fy = H - 30
    parts.append(t(pad, fy, p["tech"], 14, c["muted"], 500))
    if p["context"]:
        pw = text_width(p["context"], 13, True) + 24
        px = W - pad - pw
        parts.append(f'<rect x="{px:.0f}" y="{fy - 50}" width="{pw:.0f}" height="26" rx="13" fill="{c["pill"]}"/>')
        parts.append(t(f"{px + pw / 2:.0f}", fy - 32, p["context"], 13, c["pilltext"], 700, anchor="middle"))
    parts.append(t(W - pad, 44, "View repo →", 14, c["accent2"], 600, anchor="end"))
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
