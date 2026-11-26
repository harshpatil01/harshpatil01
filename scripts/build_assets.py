"""Build the header image used in the profile README.

Writes assets/banner-light.svg and assets/banner-dark.svg (GitHub picks one to
match the viewer's theme). Edit PROFILE below, then run:
    python scripts/build_assets.py
No third-party packages needed.
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

PROFILE = {
    "name": "Harsh Patil",
    "role": "Operations, Data & Automation",
    "areas": ["Ad Operations", "Supply Chain Analytics"],
    "line": "Power Platform  ·  Python  ·  SQL  ·  Power BI",
}

# Two neutral themes: navy ink on white, light ink on GitHub's dark background.
THEMES = {
    "light": {"bg": "#FFFFFF", "border": "#D0D7DE", "name": "#1B2A41",
              "role": "#3D4A5C", "muted": "#6E7781", "rule": "#1B2A41"},
    "dark": {"bg": "#0D1117", "border": "#30363D", "name": "#E6EDF3",
             "role": "#C9D1D9", "muted": "#8B949E", "rule": "#8B949E"},
}


def text(x, y, s, size, fill, weight=400, anchor="start", spacing=None):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}>{escape(s)}</text>')


def banner(c):
    W, H = 1200, 220
    p = PROFILE
    parts = [
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8" fill="{c["bg"]}" stroke="{c["border"]}"/>',
        text(64, 104, p["name"], 52, c["name"], 600, spacing="-0.5"),
        text(64, 146, p["role"], 24, c["role"], 400),
        f'<rect x="64" y="166" width="36" height="2" fill="{c["rule"]}"/>',
        # right column: focus areas and core tools, right-aligned
        text(W - 64, 92, "FOCUS", 13, c["muted"], 600, "end", spacing="2"),
    ]
    for i, area in enumerate(p["areas"]):
        parts.append(text(W - 64, 124 + i * 30, area, 22, c["role"], 400, "end"))
    parts.append(text(W - 64, 188, p["line"], 16, c["muted"], 400, "end"))
    title = f'{p["name"]}: {p["role"]}. ' + ", ".join(p["areas"]) + "."
    body = "".join(parts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>{body}</svg>\n')


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, colours in THEMES.items():
        (OUT / f"banner-{name}.svg").write_text(banner(colours), encoding="utf-8")
    print("Wrote banner-light.svg and banner-dark.svg to", OUT)
