#!/usr/bin/env python3
"""Builds the profile README's SVG assets in the website's "Stone Cards" style.

GitHub strips <style> and most HTML from READMEs, so every visual piece is an
SVG with its fonts embedded (images can't load web fonts). Edit the content
below and run:  python3 scripts/build.py
"""
import base64
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"
SITE = "https://angel.arrospide.dev/en"

# Tokens from AcademicPortfolio/src/config/themes.ts (light_linen / dark_linen)
THEMES = {
    "light": dict(bg="#f1efea", surface="#fbfaf7", fg="#111214", muted="#4b4f56",
                  border="#bfc3c9", accent="#ffba00", accent_text="#6b4800", on_accent="#111214"),
    "dark": dict(bg="#111214", surface="#1b1c1f", fg="#f1efea", muted="#bfc3c9",
                 border="#3a3d42", accent="#ffba00", accent_text="#ffba00", on_accent="#111214"),
}

FONTS = {
    "jost300": ("Jost", 300, "jost-latin-300-normal.woff2"),
    "jost400": ("Jost", 400, "jost-latin-400-normal.woff2"),
    "plex400": ("IBM Plex Sans", 400, "ibm-plex-sans-latin-400-normal.woff2"),
    "plex500": ("IBM Plex Sans", 500, "ibm-plex-sans-latin-500-normal.woff2"),
    "caveat600": ("Caveat", 600, "caveat-latin-600-normal.woff2"),
}

# Hand-drawn strokes, copied from src/components/ui/HandDrawn.astro
ARROW = ("0 0 60 26", ["M2 16C10 12.5 17 17.5 26 14.5 34 12 42 15.5 55 12.5",
                       "M44 4.5C47.5 7 52 9.5 56.5 12.2 52 15.5 48.5 18.5 46 22.5"])
CURLY = ("0 0 32 56", ["M11.5 1.5C12.6 5.5 13.5 11 13.9 14.8 10.5 17 4.2 20.5 3.1 25.6 2.1 30.6 5.6 33.6 9.6 31.6 13.3 29.7 15.6 22.5 14.6 16.2 17.8 18.6 22 23 23.7 29 25.2 34.6 25 42.5 21.5 52.5",
                       "M17.8 46.6C19 48.6 20.6 51 21.5 52.6 24 50.6 27.4 48.4 29.6 47.4"])
UNDERLINE = ("0 0 200 12", ["M3 8c37-5 77 2 117-3 30-3 60 2 77-1"])

BASE_CSS = """
.hd{fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round}
.hd path{stroke-dasharray:1;stroke-dashoffset:0}
@keyframes draw{from{stroke-dashoffset:1;opacity:0}1%{opacity:1}to{stroke-dashoffset:0;opacity:1}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
"""
REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important;opacity:1!important;stroke-dashoffset:0!important}}"


def font_face(*keys):
    out = []
    for k in keys:
        family, weight, file = FONTS[k]
        data = base64.b64encode((ROOT / "fonts" / file).read_bytes()).decode()
        out.append(f"@font-face{{font-family:'{family}';font-weight:{weight};"
                   f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return "".join(out)


def esc(s):
    return html.escape(s, quote=True)


def stroke(shape, x, y, w, h, color, width, cls="", stretch=False):
    vb, paths = shape
    par = ' preserveAspectRatio="none"' if stretch else ""
    ps = "".join(f'<path d="{d}" pathLength="1"/>' for d in paths)
    return (f'<svg class="hd {cls}" x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{vb}"{par} '
            f'overflow="visible" style="color:{color}" stroke-width="{width}">{ps}</svg>')


def svg(w, h, css, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
            f"<style>{css}{REDUCED}</style>{body}</svg>\n")


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"assets/{name}  {len(content.encode()) // 1024} KB")


# ---------------------------------------------------------------- banner
def banner():
    t = THEMES["light"]
    W, H, pad = 1200, 440, 56
    css = font_face("jost300", "plex400", "caveat600") + BASE_CSS + f"""
.name{{font-family:Jost;font-weight:300;font-size:104px;letter-spacing:-3px;fill:{t['on_accent']}}}
.name tspan{{animation:fade .35s ease-out both}}
.lead{{font-family:'IBM Plex Sans';font-size:27px;fill:{t['on_accent']};animation:fade .6s ease-out 1s both}}
.note{{font-family:Caveat;font-weight:600;font-size:32px;fill:{t['on_accent']};animation:fade .35s ease-out 2.5s both}}
.u path{{animation:draw .7s ease-out 1.5s both}}
.c path{{animation:draw .7s cubic-bezier(.4,0,.6,1) 2.5s both}}
.c path+path{{animation-duration:.25s;animation-delay:3.28s}}
.avatar{{animation:rise .6s ease-out .2s both}}
"""
    i = 0

    def letters(word):
        nonlocal i
        spans = []
        for ch in word:
            spans.append(f'<tspan style="animation-delay:{0.25 + i * 0.045:.3f}s">{esc(ch)}</tspan>')
            i += 1
        return "".join(spans)

    avatar = base64.b64encode((ROOT / "avatar.jpeg").read_bytes()).decode()
    A, ax, ay = 260, W - pad - 260, pad
    body = f"""
<rect width="{W}" height="{H}" rx="22" fill="{t['accent']}"/>
<text class="name" x="{pad - 4}" y="{pad + 92}">{letters("Ángel")}</text>
<text class="name" x="{pad - 4}" y="{pad + 196}">{letters("Arróspide-Marco")}</text>
<text class="lead" x="{pad}" y="{H - 104}">Computer engineer working on the security of AI systems</text>
<text class="lead" x="{pad}" y="{H - 64}">and ML applied to <tspan id="mark">cybersecurity</tspan>.</text>
{stroke(UNDERLINE, 280, H - 58, 172, 12, t['on_accent'], 2.6, "u", stretch=True)}
<clipPath id="r"><rect x="{ax}" y="{ay}" width="{A}" height="{A}" rx="22"/></clipPath>
<image class="avatar" href="data:image/jpeg;base64,{avatar}" x="{ax}" y="{ay}" width="{A}" height="{A}" clip-path="url(#r)" preserveAspectRatio="xMidYMid slice"/>
<text class="note" x="{W - pad - 150}" y="{H - 36}" transform="rotate(-4 {W - pad - 100} {H - 40})">this way</text>
{stroke(CURLY, W - pad - 36, H - 94, 34, 60, t['on_accent'], 2.4, "c")}
"""
    write("banner.svg", svg(W, H, css, body, "Ángel Arróspide-Marco — Computer engineer working on the security of AI systems and ML applied to cybersecurity."))


# ---------------------------------------------------------------- nav cards
NAV = [
    ("notes", "Notes", ["Talks, publications, projects,", "and reviews."]),
    ("now", "Now", ["What I'm currently working on,", "learning, and reading."]),
    ("manifesto", "Manifesto", ["What interests me and", "what I believe in."]),
    ("cv", "CV", ["Academic and professional", "history."]),
]


def nav_card(slug, title, lines, mode):
    t = THEMES[mode]
    W, H = 400, 132
    css = font_face("jost400", "plex400") + BASE_CSS + f"""
.t{{font-family:Jost;font-size:27px;fill:{t['fg']}}}
.s{{font-family:'IBM Plex Sans';font-size:16.5px;fill:{t['muted']}}}
.a path{{animation:draw .45s cubic-bezier(.4,0,.6,1) .3s both}}
.a path+path{{animation-duration:.22s;animation-delay:.8s}}
"""
    sub = "".join(f'<text class="s" x="26" y="{80 + n * 24}">{esc(l)}</text>' for n, l in enumerate(lines))
    body = f"""
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{t['surface']}" stroke="{t['border']}"/>
<text class="t" x="26" y="46">{esc(title)}</text>
{stroke(ARROW, W - 26 - 42, 26, 42, 18, t['accent_text'], 3, "a")}
{sub}
"""
    write(f"card-{slug}-{mode}.svg", svg(W, H, css, body, f"{title} — {' '.join(lines)}"))


# ---------------------------------------------------------------- pinned project
def project(mode):
    t = THEMES[mode]
    W, H = 816, 300
    tint = f"color-mix(in srgb,{t['accent']} 10%,{t['surface']})"
    edge = f"color-mix(in srgb,{t['accent']} 45%,{t['border']})"
    css = font_face("jost300", "jost400", "plex400", "plex500") + BASE_CSS + f"""
.card{{fill:{tint};stroke:{edge}}}
.tag{{font-family:'IBM Plex Sans';font-weight:500;font-size:13px;fill:{t['accent_text']};letter-spacing:.4px}}
.pill{{fill:none;stroke:{edge}}}
.t{{font-family:Jost;font-size:30px;fill:{t['fg']}}}
.d{{font-family:'IBM Plex Sans';font-size:16.5px;fill:{t['muted']}}}
.n{{font-family:Jost;font-weight:300;font-size:46px;letter-spacing:-1px;fill:{t['fg']};animation:fade .5s ease-out both}}
.l{{font-family:'IBM Plex Sans';font-size:14.5px;fill:{t['muted']}}}
.rule{{stroke:{edge}}}
.a path{{animation:draw .45s cubic-bezier(.4,0,.6,1) .4s both}}
.a path+path{{animation-duration:.22s;animation-delay:.9s}}
"""
    stats = [("98.6%", "precision"), ("95.0%", "recall"), ("3M+ pkt/s", "on a Raspberry Pi 4")]
    cols = "".join(
        f'<text class="n" x="{30 + k * 255}" y="232" style="animation-delay:{0.3 + k * 0.2}s">{esc(n)}</text>'
        f'<text class="l" x="{32 + k * 255}" y="262">{esc(l)}</text>'
        for k, (n, l) in enumerate(stats))
    body = f"""
<rect class="card" x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14"/>
<rect class="pill" x="30.5" y="26.5" width="232" height="26" rx="13"/>
<text class="tag" x="46" y="44">PINNED · BACHELOR'S THESIS</text>
<text class="t" x="30" y="96">Edge-Deployable Anomaly Detection for Industrial IoT</text>
{stroke(ARROW, W - 30 - 42, 78, 42, 18, t['accent_text'], 3, "a")}
<text class="d" x="30" y="128">An unsupervised NIDS for Industrial IoT traffic that catches zero-day attacks</text>
<text class="d" x="30" y="152">without attack labels — fast enough to score live traffic at the edge.</text>
<line class="rule" x1="30" y1="180" x2="{W - 30}" y2="180"/>
{cols}
"""
    write(f"project-nids-{mode}.svg", svg(W, H, css, body,
          "Edge-Deployable Anomaly Detection for Industrial IoT — 98.6% precision, 95.0% recall, 3M+ packets/s on a Raspberry Pi 4."))


# ---------------------------------------------------------------- section heading
def heading(slug, text, mode):
    t = THEMES[mode]
    W, H = 816, 56
    css = font_face("jost300") + BASE_CSS + f"""
.h{{font-family:Jost;font-weight:300;font-size:34px;letter-spacing:-.6px;fill:{t['fg']}}}
.u path{{animation:draw .6s ease-out .2s both}}
"""
    width = 15 * len(text) + 8
    body = f"""<text class="h" x="2" y="36">{esc(text)}</text>
{stroke(UNDERLINE, 0, 42, width, 10, t['accent_text'] if mode == 'light' else t['accent'], 2.4, "u", stretch=True)}"""
    write(f"h-{slug}-{mode}.svg", svg(W, H, css, body, text))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    banner()
    for mode in THEMES:
        for slug, title, lines in NAV:
            nav_card(slug, title, lines, mode)
        project(mode)
        heading("work", "Selected work", mode)
        heading("now", "Now", mode)
