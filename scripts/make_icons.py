#!/usr/bin/env python3
"""Generate Scribe's icon set: champagne gold waveform on charcoal.

App icon follows the macOS Big Sur grid (824px body inside a 1024 canvas,
~22.5% corner radius). Tray icons are flat monochrome silhouettes with
transparency, in light (for dark menu bars) and dark (for light menu bars).
"""
import os, math, subprocess, shutil
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, "src-tauri", "icons")
RES = os.path.join(ROOT, "src-tauri", "resources")

CHARCOAL_TOP = (46, 46, 51)
CHARCOAL_BOT = (24, 24, 27)
GOLD_TOP = (240, 214, 160)
GOLD_BOT = (198, 162, 100)

# 5 chunky bars: reads as "voice" at Dock size and survives the 16/32px
# Finder/Spotlight renders, where a finer 7-bar wave turns into a blob.
BARS = [0.35, 0.70, 1.00, 0.70, 0.35]


def vgradient(size, top, bottom):
    """Vertical linear gradient image."""
    w, h = size
    img = Image.new("RGB", (1, h))
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return img.resize((w, h), Image.NEAREST)


def squircle_mask(size, n=5.0, ss=4):
    """macOS-style squircle (superellipse |x|^n + |y|^n = 1), supersampled.

    A plain rounded rectangle uses circular corner arcs and reads subtly wrong
    next to native Dock icons; the continuous curvature is the whole point.
    """
    big = size * ss
    m = Image.new("L", (big, big), 0)
    d = ImageDraw.Draw(m)
    r = big / 2.0
    pts = []
    steps = 720
    for i in range(steps):
        theta = 2.0 * math.pi * i / steps
        ct, st = math.cos(theta), math.sin(theta)
        x = r * math.copysign(abs(ct) ** (2.0 / n), ct)
        y = r * math.copysign(abs(st) ** (2.0 / n), st)
        pts.append((r + x, r + y))
    d.polygon(pts, fill=255)
    return m.resize((size, size), Image.LANCZOS)


def waveform_mask(size, bars, bar_w, gap, max_h, cap=True):
    """L-mask of centered waveform bars with rounded caps."""
    w, h = size
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    total = len(bars) * bar_w + (len(bars) - 1) * gap
    x = (w - total) / 2
    for ratio in bars:
        bh = max_h * ratio
        y0 = (h - bh) / 2
        box = [x, y0, x + bar_w, y0 + bh]
        r = bar_w / 2 if cap else 0
        if r > 0:
            d.rounded_rectangle(box, radius=r, fill=255)
        else:
            d.rectangle(box, fill=255)
        x += bar_w + gap
    return m


def app_icon(px=1024):
    """Charcoal squircle body + gold waveform."""
    s = px / 1024
    canvas = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    body = int(824 * s)
    off = int(100 * s)

    mask = squircle_mask(body)
    canvas.paste(vgradient((body, body), CHARCOAL_TOP, CHARCOAL_BOT), (off, off), mask)

    bar_w, gap, max_h = 64 * s, 40 * s, 400 * s
    wm = waveform_mask((px, px), BARS, bar_w, gap, max_h)
    canvas.paste(vgradient((px, px), GOLD_TOP, GOLD_BOT), (0, 0), wm)
    return canvas


def tray_icon(state, color, px=64):
    """Flat monochrome state glyph with transparency."""
    img = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if state == "idle":
        wm = waveform_mask((px, px), [0.30, 0.62, 1.0, 0.62, 0.30], 6, 6, 44)
        solid = Image.new("RGBA", (px, px), color)
        img.paste(solid, (0, 0), wm)
    elif state == "recording":
        r = 15  # filled record dot — unmistakable at menu-bar size
        d.ellipse([px / 2 - r, px / 2 - r, px / 2 + r, px / 2 + r], fill=color)
    elif state == "transcribing":
        r, gap = 6, 20  # ellipsis = working
        for i in (-1, 0, 1):
            cx = px / 2 + i * gap
            d.ellipse([cx - r, px / 2 - r, cx + r, px / 2 + r], fill=color)
    return img


def main():
    master = app_icon(1024)
    os.makedirs(ICONS, exist_ok=True)

    # macOS .icns via iconutil
    iconset = os.path.join(ICONS, "icon.iconset")
    shutil.rmtree(iconset, ignore_errors=True)
    os.makedirs(iconset)
    for sz in (16, 32, 128, 256, 512):
        master.resize((sz, sz), Image.LANCZOS).save(f"{iconset}/icon_{sz}x{sz}.png")
        master.resize((sz * 2, sz * 2), Image.LANCZOS).save(f"{iconset}/icon_{sz}x{sz}@2x.png")
    subprocess.run(["iconutil", "-c", "icns", iconset, "-o", f"{ICONS}/icon.icns"], check=True)
    shutil.rmtree(iconset)

    # Tauri/Windows png set
    master.save(f"{ICONS}/icon.png")
    for name, sz in [("32x32", 32), ("64x64", 64), ("128x128", 128), ("128x128@2x", 256),
                     ("Square30x30Logo", 30), ("Square44x44Logo", 44), ("Square71x71Logo", 71),
                     ("Square89x89Logo", 89), ("Square107x107Logo", 107), ("Square142x142Logo", 142),
                     ("Square150x150Logo", 150), ("Square284x284Logo", 284),
                     ("Square310x310Logo", 310), ("StoreLogo", 50)]:
        master.resize((sz, sz), Image.LANCZOS).save(f"{ICONS}/{name}.png")
    master.resize((256, 256), Image.LANCZOS).save(
        f"{ICONS}/icon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (256, 256)])

    # Tray: light (white, for dark menu bars) + dark (near-black, for light menu bars)
    WHITE, DARK, GOLD = (255, 255, 255, 255), (28, 28, 30, 255), (229, 200, 143, 255)
    for state in ("idle", "recording", "transcribing"):
        tray_icon(state, WHITE).save(f"{RES}/tray_{state}.png")
        tray_icon(state, DARK).save(f"{RES}/tray_{state}_dark.png")
    # "Colored" set (Linux) keeps the brand gold
    tray_icon("idle", GOLD).save(f"{RES}/scribe.png")
    tray_icon("recording", GOLD).save(f"{RES}/recording.png")
    tray_icon("transcribing", GOLD).save(f"{RES}/transcribing.png")

    master.resize((512, 512), Image.LANCZOS).save("/tmp/scribe_preview.png")
    print("icons written")


if __name__ == "__main__":
    main()
