#!/usr/bin/env python3
"""Compose the news-image-01 front page (v2): 1024x1024 newspaper-style summary
of Friday 13 November 2026 world news. AI-generated editorial illustrations
(assets/*.webp); all text rendered crisply by PIL. Run: python3 compose.py [out.png]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

W = H = 1024
BG = (247, 243, 234)
INK = (22, 22, 22)
RED = (178, 34, 34)
GREY = (90, 86, 78)
RULE = (60, 58, 52)
BODY = (52, 50, 46)

A = "assets"

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold", s)
F_SERIF = lambda s: font("DejaVuSerif", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold", s)
F_SANS = lambda s: font("DejaVuSans", s)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit_anchor(path, w, h, anchor_y=0.5):
    """Resize to cover (w,h), cropping vertically at anchor_y (0=top, 1=bottom)."""
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    scale = max(w / iw, h / ih)
    nw, nh = round(iw * scale), round(ih * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - w) // 2
    y0 = int((nh - h) * anchor_y)
    return im.crop((x0, y0, x0 + w, y0 + h))

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 4], fill=INK)
d.text((W // 2, 52), "THE WORLD IN ONE DAY", font=F_SERIF_B(58), fill=INK, anchor="mm")
d.text((W // 2, 92), "FRIDAY, 13 NOVEMBER 2026", font=F_SANS_B(21), fill=RED, anchor="mm")
d.line([(24, 108), (W - 24, 108)], fill=RULE, width=3)
d.line([(24, 114), (W - 24, 114)], fill=RULE, width=1)

# ---- hero: Iran / Strait of Hormuz (126-440) ----
hy, hh = 126, 314
hero = fit_anchor(f"{A}/media-generation-hero-hormuz-0-b5b2e68b-f940-4c82-87c4-e005b1d059db.webp",
                  596, hh, anchor_y=0.7)
img.paste(hero, (24, hy))
d.rectangle([24, hy, 24 + 596, hy + hh], outline=RULE, width=2)
tx = 640
d.text((tx, hy + 4), "THE GULF  \u2022  WAR", font=F_SANS_B(20), fill=RED)
lines = wrap(d, "TANKERS HIT, RADAR DOWN AS IRAN WAR ESCALATES", F_SERIF_B(36), W - 24 - tx)
y = hy + 36
for ln in lines:
    d.text((tx, y), ln, font=F_SERIF_B(36), fill=INK)
    y += 44
y += 6
dek = ("Iran says it destroyed a US radar in Bahrain. An LNG "
       "tanker struck a mine in the Strait of Hormuz; four tankers were hit.")
for ln in wrap(d, dek, F_SERIF(18), W - 24 - tx):
    d.text((tx, y), ln, font=F_SERIF(18), fill=BODY)
    y += 24

# ---- row 2: Ukraine | Microsoft (456-744) ----
ry = 456
def panel(x, w, imgpath, kicker, headline, dek):
    im = fit_anchor(imgpath, w, 150, anchor_y=0.5)
    img.paste(im, (x, ry))
    d.rectangle([x, ry, x + w, ry + 150], outline=RULE, width=2)
    yy = ry + 160
    d.text((x, yy), kicker, font=F_SANS_B(17), fill=RED)
    yy += 26
    for ln in wrap(d, headline, F_SERIF_B(24), w):
        d.text((x, yy), ln, font=F_SERIF_B(24), fill=INK)
        yy += 30
    yy += 2
    for ln in wrap(d, dek, F_SERIF(16), w):
        d.text((x, yy), ln, font=F_SERIF(16), fill=BODY)
        yy += 22

panel(24, 478,
      f"{A}/media-generation-ukraine-talks-0-0a65d898-cc42-41ed-8788-ece138240c29.webp",
      "EUROPE  \u2022  DIPLOMACY",
      "EU WINS A SEAT AT UKRAINE PEACE TALKS",
      "Europe joins the next round; a record prisoner swap is planned.")
panel(522, 478,
      f"{A}/media-generation-microsoft-outage-0-3749c06b-e7f6-44d1-9396-62e7882a9cea.webp",
      "TECHNOLOGY  \u2022  OUTAGE",
      "MICROSOFT OUTAGE HITS OUTLOOK",
      "Teams and Copilot down too; Microsoft says it was no cyberattack.")
d.line([(24, 752), (W - 24, 752)], fill=RULE, width=1)

# ---- row 3 (768-964) ----
ry3 = 768
# Nvidia panel (left)
nx, nw = 24, 478
im = fit_anchor(f"{A}/media-generation-nvidia-chip-0-a2216600-aaa3-49c2-a2a0-a247f509961d.webp",
                nw, 96, anchor_y=0.5)
img.paste(im, (nx, ry3))
d.rectangle([nx, ry3, nx + nw, ry3 + 96], outline=RULE, width=2)
yy = ry3 + 104
d.text((nx, yy), "BUSINESS  \u2022  CHIPS", font=F_SANS_B(17), fill=RED)
yy += 26
for ln in wrap(d, "NVIDIA CHIEF HUANG RESIGNS, SUMMONED BY CONGRESS",
               F_SERIF_B(22), nw):
    d.text((nx, yy), ln, font=F_SERIF_B(22), fill=INK)
    yy += 27
d.text((nx, yy), "CFO Colette Kress is interim CEO.", font=F_SERIF(15), fill=BODY)

# Also today (right)
ax, aw = 522, 478
d.text((ax, ry3), "ALSO TODAY", font=F_SANS_B(19), fill=RED)
d.line([(ax, ry3 + 30), (ax + aw, ry3 + 30)], fill=RULE, width=2)
items = [
    ("Pope Leo XIV meets six abuse survivors in Peru as record crowds fill Lima.",
     "THE VATICAN"),
    ("Brooklyn collapse: final toll 8 dead, 18 injured.",
     "NEW YORK"),
    ("US seizes $1.2B from the Binance hack.",
     "WASHINGTON"),
]
yy = ry3 + 42
for txt, tag in items:
    d.ellipse([ax, yy + 5, ax + 9, yy + 14], fill=RED)
    for ln in wrap(d, txt, F_SERIF_B(16), aw - 20):
        d.text((ax + 18, yy), ln, font=F_SERIF_B(16), fill=INK)
        yy += 22
    d.text((ax + 18, yy), tag, font=F_SANS_B(13), fill=GREY)
    yy += 30

# ---- footer ----
d.line([(24, 972), (W - 24, 972)], fill=RULE, width=1)
d.text((W // 2, 992),
       "Sources: BBC \u00b7 AP \u00b7 Al Jazeera \u00b7 Reuters \u00b7 France 24 \u00b7 Just Security  \u2014  all stories reported 13 November 2026",
       font=F_SANS(13), fill=GREY, anchor="mm")
d.text((W // 2, 1012),
       "Editorial illustrations AI-generated  \u00b7  make.fun news-image-01",
       font=F_SANS(12), fill=GREY, anchor="mm")

out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes", img.size)
