#!/usr/bin/env python3
"""Generate og.png — 1200x630 link-preview card styled like an exported Swatch.
One-shot tool, not part of the site build. Run: python3 build-og.py"""
import os, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fontTools.ttLib import TTFont

# decompress the self-hosted woff2 fonts to ttf so PIL can render the real faces
_tmp = tempfile.mkdtemp()
def _ttf(src):
    f = TTFont(src); f.flavor = None
    out = os.path.join(_tmp, os.path.basename(src).replace(".woff2", ".ttf"))
    f.save(out); return out
CLASH7 = _ttf("vendor/fonts/clash-display-700.woff2")
CLASH5 = _ttf("vendor/fonts/clash-display-500.woff2")
MONO3  = _ttf("vendor/fonts/martian-mono-300-latin.woff2")
def F(p, s): return ImageFont.truetype(p, s)

W, H = 1200, 630
BG, FG, FG2 = "#14131A", "#F4F1EA", "#9A96A4"   # signature export dark + ink/muted
TILES = ["#E2664F", "#F0A18C", "#DAD3CB", "#C9A9A6", "#FBF4EF"]   # "Coral Concrete"
ACCENT = TILES[0]

img = Image.new("RGB", (W, H), BG)

# soft ambient glow top-right (echoes the site's three.js wash)
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
ar, ag, ab = (226, 102, 79)
for r, a in [(560, .22), (340, .16)]:
    gd.ellipse((W-180-r, -120-r, W-180+r, -120+r),
               fill=(0x14 + int(ar*a), 0x13 + int(ag*a), 0x1A + int(ab*a)))
glow = glow.filter(ImageFilter.GaussianBlur(150))
img = Image.blend(img, glow, 0.6)
draw = ImageDraw.Draw(img)

pad = 72
# meta row
draw.text((pad, pad-4), "tryswatch.com", font=F(MONO3, 25), fill=FG2)
rt = "COLOUR PALETTE STUDIO"
draw.text((W-pad-draw.textlength(rt, font=F(MONO3, 25)), pad-4), rt, font=F(MONO3, 25), fill=FG2)

# oversized wordmark "Swatch." with an accent period
tf = F(CLASH7, 160)
draw.text((pad-4, 128), "Swatch", font=tf, fill=FG)
draw.text((pad-4 + draw.textlength("Swatch", font=tf), 128), ".", font=tf, fill=ACCENT)

# tagline (two lines, kept clear of the tiles)
tg = F(CLASH5, 34)
draw.text((pad, 330), "A free colour palette generator.", font=tg, fill=FG)
draw.text((pad, 374), "Build with colour theory, export anywhere.", font=tg, fill=FG2)

# five hex tiles along the bottom
gap, tileH, bot = 14, 150, 54
tileW = (W - 2*pad - 4*gap) / 5
tileY = H - bot - tileH
mono = F(MONO3, 23)
for i, hx in enumerate(TILES):
    tx = pad + i*(tileW+gap)
    draw.rounded_rectangle((tx, tileY, tx+tileW, tileY+tileH), radius=16, fill=hx)
    r, g, b = int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16)
    tc = "#1A1814" if (r*299 + g*587 + b*114)/1000 > 150 else "#FBFAF6"
    draw.text((tx+18, tileY+tileH-34), hx[1:].upper(), font=mono, fill=tc)

img.save("og.png")
print("wrote og.png", img.size, os.path.getsize("og.png"), "bytes")
