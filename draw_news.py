"""Draw the news-image-20261123 poster (1024x1024) with Pillow.

Build-time helper only: it renders news.png at 2x and downscales with
LANCZOS. Deterministic: fixed seed, no network, no timestamps.
Run: python3 draw_news.py  ->  writes news.png next to this file.

All layout numbers are in FINAL pixels (1024x1024); u() scales them to
the 2x working canvas.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SS = 2                      # supersample factor


def u(n):
    return int(n * SS)


W = u(1024)
H = u(1024)

CHARCOAL = (26, 24, 21)
PANEL = (46, 42, 36)
PANEL_LINE = (96, 88, 76)
PAPER = (243, 233, 214)
INK = (34, 29, 24)
EMBER = (198, 57, 43)
EMBER_DARK = (138, 30, 20)
EMBER_GLOW = (232, 96, 40)
SAFETY = (245, 197, 24)
CREAM = (243, 233, 214)
WHITE = (250, 247, 240)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

rng = random.Random(20261123)


def font(path, size_final):
    return ImageFont.truetype(path, u(size_final))


def fit_font(draw, text, path, max_w_final, start_final, min_size=10):
    """Largest font size (<= start) whose text fits max_w_final."""
    size = start_final
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= u(max_w_final):
            return f
        size -= 2
    return font(path, min_size)


def wrap(draw, text, f, max_w_final):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=f) <= u(max_w_final):
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_center(draw, y_final, lines, f, fill, leading=1.15):
    y = u(y_final)
    for line in lines:
        w = draw.textlength(line, font=f)
        draw.text(((W - w) / 2, y), line, font=f, fill=fill)
        y += int(f.size * leading)
    return y // SS


def draw_strait(d, x, y, s):
    """Mini map of a strait: two landmasses, narrow channel, red arrow."""
    d.polygon([(x, y), (x + s * 0.42, y), (x + s * 0.30, y + s),
               (x, y + s)], fill=(110, 96, 70))
    d.polygon([(x + s * 0.62, y), (x + s, y), (x + s, y + s),
               (x + s * 0.52, y + s)], fill=(110, 96, 70))
    d.polygon([(x + s * 0.42, y), (x + s * 0.62, y), (x + s * 0.52, y + s),
               (x + s * 0.30, y + s)], fill=(64, 110, 140))
    d.line([(x + s * 0.46, y + s * 0.12), (x + s * 0.46, y + s * 0.88)],
           fill=EMBER, width=max(4, s // 16))
    d.polygon([(x + s * 0.46, y + s * 0.98), (x + s * 0.34, y + s * 0.78),
               (x + s * 0.58, y + s * 0.78)], fill=EMBER)


def draw_ship_fire(d, x, y, s):
    d.polygon([(x, y + s * 0.55), (x + s, y + s * 0.55), (x + s * 0.85, y + s * 0.85),
               (x + s * 0.15, y + s * 0.85)], fill=(90, 80, 66))
    d.rectangle([x + s * 0.30, y + s * 0.32, x + s * 0.45, y + s * 0.55], fill=(120, 108, 88))
    d.rectangle([x + s * 0.60, y + s * 0.38, x + s * 0.72, y + s * 0.55], fill=(120, 108, 88))
    for cx, cy, r, col in [(0.38, 0.28, 0.20, EMBER_GLOW), (0.52, 0.18, 0.24, EMBER),
                           (0.66, 0.30, 0.17, SAFETY), (0.45, 0.10, 0.12, EMBER_GLOW)]:
        d.ellipse([x + s * (cx - r), y + s * (cy - r), x + s * (cx + r), y + s * (cy + r)],
                  fill=col)


def draw_building_drone(d, x, y, s):
    d.rectangle([x + s * 0.10, y + s * 0.30, x + s * 0.62, y + s * 0.90], fill=(120, 108, 88))
    d.polygon([(x + s * 0.62, y + s * 0.30), (x + s * 0.90, y + s * 0.45),
               (x + s * 0.90, y + s * 0.90), (x + s * 0.62, y + s * 0.90)],
              fill=(96, 86, 70))
    d.polygon([(x + s * 0.10, y + s * 0.30), (x + s * 0.36, y + s * 0.12),
               (x + s * 0.62, y + s * 0.30)], fill=(70, 62, 50))
    for wy in (0.45, 0.62, 0.79):
        for wx in (0.22, 0.40):
            d.rectangle([x + s * wx, y + s * wy, x + s * (wx + 0.09), y + s * (wy + 0.09)],
                        fill=SAFETY)
    cx, cy = x + s * 0.82, y + s * 0.16
    d.ellipse([cx - s * 0.05, cy - s * 0.05, cx + s * 0.05, cy + s * 0.05], fill=CREAM)
    for dx in (-0.14, 0.14):
        d.ellipse([cx + s * dx - s * 0.06, cy - s * 0.06, cx + s * dx + s * 0.06, cy + s * 0.06],
                  outline=CREAM, width=max(3, s // 40))


def draw_factory(d, x, y, s):
    d.rectangle([x + s * 0.08, y + s * 0.55, x + s * 0.92, y + s * 0.90], fill=(120, 108, 88))
    d.polygon([(x + s * 0.08, y + s * 0.55), (x + s * 0.30, y + s * 0.38),
               (x + s * 0.55, y + s * 0.55)], fill=(96, 86, 70))
    for cx in (0.22, 0.48, 0.74):
        d.rectangle([x + s * cx, y + s * 0.18, x + s * (cx + 0.09), y + s * 0.60],
                    fill=(90, 80, 66))
    for cx, cy, r in [(0.26, 0.10, 0.10), (0.52, 0.06, 0.12), (0.78, 0.12, 0.09)]:
        d.ellipse([x + s * (cx - r), y + s * (cy - r), x + s * (cx + r), y + s * (cy + r)],
                  fill=(150, 142, 130))


def draw_chair_chip(d, x, y, s):
    d.rectangle([x + s * 0.18, y + s * 0.55, x + s * 0.55, y + s * 0.62], fill=(120, 108, 88))
    d.rectangle([x + s * 0.18, y + s * 0.15, x + s * 0.26, y + s * 0.58], fill=(120, 108, 88))
    d.line([(x + s * 0.22, y + s * 0.62), (x + s * 0.22, y + s * 0.90)], fill=(120, 108, 88),
           width=max(4, s // 20))
    d.line([(x + s * 0.52, y + s * 0.62), (x + s * 0.52, y + s * 0.90)], fill=(120, 108, 88),
           width=max(4, s // 20))
    d.rectangle([x + s * 0.62, y + s * 0.55, x + s * 0.95, y + s * 0.88], fill=EMBER)
    d.rectangle([x + s * 0.70, y + s * 0.63, x + s * 0.87, y + s * 0.80], fill=CHARCOAL)
    d.text((x + s * 0.72, y + s * 0.64), "AI", font=font(BOLD, max(10, s // 6 // SS)),
           fill=SAFETY)


def draw_scoreboard(d, x, y, s):
    d.rectangle([x, y + s * 0.15, x + s, y + s * 0.85], fill=(20, 20, 18),
                outline=SAFETY, width=max(3, s // 30))
    d.text((x + s * 0.08, y + s * 0.28), "720/9d", font=font(BOLD, max(12, s // 4 // SS)),
           fill=SAFETY)
    d.text((x + s * 0.08, y + s * 0.62), "IND v NZ", font=font(BOLD, max(10, s // 9 // SS)),
           fill=CREAM)


def build():
    img = Image.new("RGB", (W, H), CHARCOAL)
    d = ImageDraw.Draw(img, "RGBA")
    margin = u(24)

    # ---- header: date -------------------------------------------------
    date_f = fit_font(d, "MONDAY 23 NOVEMBER 2026", BOLD, 1024 - 48, 62)
    y = text_center(d, 22, ["MONDAY 23 NOVEMBER 2026"], date_f, SAFETY)
    sub_f = font(BOLD, 18)
    y = text_center(d, y + 8, ["THE DAY IN SIX STORIES"], sub_f, CREAM)
    rule_y = u(y + 14)
    d.rectangle([margin, rule_y, W - margin, rule_y + u(3)], fill=EMBER)

    # ---- burning draft document ---------------------------------------
    doc_w, doc_h = u(620), u(250)
    doc = Image.new("RGBA", (doc_w, doc_h), (0, 0, 0, 0))
    glow = Image.new("RGBA", (doc_w, doc_h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([doc_w * 0.55, -doc_h * 0.25, doc_w * 1.15, doc_h * 0.75],
               fill=(232, 96, 40, 60))
    doc = Image.alpha_composite(doc, glow)
    dd = ImageDraw.Draw(doc)
    dd.rectangle([0, 0, doc_w, doc_h], fill=PAPER + (255,))
    dd.rectangle([0, 0, doc_w, doc_h], outline=(190, 172, 140, 255), width=u(2))
    char = [(doc_w * 0.72, doc_h), (doc_w * 0.80, doc_h * 0.86),
            (doc_w * 0.88, doc_h * 0.94), (doc_w * 0.94, doc_h * 0.82),
            (doc_w, doc_h * 0.90), (doc_w, doc_h)]
    dd.polygon(char, fill=(24, 18, 14, 255))
    for _ in range(26):
        t = rng.random()
        ex = doc_w * (0.72 + 0.28 * t)
        ey = doc_h * (0.86 + 0.10 * rng.random())
        r = u(2 + 3 * rng.random())
        col = rng.choice([EMBER_GLOW, EMBER, SAFETY])
        dd.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col + (255,))
    # (smoke wisps removed: they read as a smudge on the sheet's top edge)
    kick_f = font(BOLD, 20)
    dd.text((u(28), u(20)), "DRAFT  —  COP31 FINAL TEXT", font=kick_f, fill=(120, 90, 60))
    dd.line([(u(28), u(20) + kick_f.size + u(8)),
             (doc_w - u(28), u(20) + kick_f.size + u(8))],
            fill=(190, 172, 140), width=u(2))
    struck_f = fit_font(dd, "FOSSIL FUELS", BOLD, 620 - 56, 64)
    ty = u(20) + kick_f.size + u(18)
    dd.text((u(28), ty), "FOSSIL FUELS", font=struck_f, fill=INK)
    tw = dd.textlength("FOSSIL FUELS", font=struck_f)
    sy = ty + struck_f.size * 0.52
    dd.line([(u(28) - u(4), sy - u(3)), (u(28) + tw + u(4), sy + u(5))],
            fill=EMBER, width=u(7))
    dd.line([(u(28) - u(4), sy + u(5)), (u(28) + tw + u(4), sy - u(3))],
            fill=EMBER, width=u(5))
    note_y = (ty + struck_f.size + u(14)) // SS
    dd.text((u(28), u(note_y)), "phase-out language removed from the text",
            font=font(REG, 19), fill=(80, 66, 50))
    dd.text((u(28), u(note_y + 26)), "EU: no deal without it",
            font=font(BOLD, 19), fill=EMBER_DARK)

    doc_rot = doc.rotate(-2, expand=True, resample=Image.BICUBIC)
    doc_x = (W - doc_rot.width) // 2
    doc_y = rule_y + u(16)
    img.paste(doc_rot, (doc_x, doc_y), doc_rot)

    # ---- headline ------------------------------------------------------
    hy = doc_y // SS + doc_rot.height // SS + 14
    h1_f = fit_font(d, "COP31 TALKS", BOLD, 1024 - 48, 66)
    hy = text_center(d, hy, ["COP31 TALKS"], h1_f, CREAM, leading=1.0)
    h2_f = fit_font(d, "COLLAPSE", BOLD, 1024 - 48, 66)
    hy = text_center(d, hy, ["COLLAPSE"], h2_f, EMBER_GLOW, leading=1.0)
    sub2_f = fit_font(d, "EU rejects final draft without fossil-fuel phase-out.",
                      BOLD, 1024 - 48, 24)
    hy = text_center(d, hy + 8, ["EU rejects final draft without fossil-fuel phase-out."],
                     sub2_f, SAFETY)

    # ---- bottom strip: six stories -------------------------------------
    tiles = [
        ("HORMUZ", "Iran–US war spreads to Saudi Arabia and Bahrain", draw_strait),
        ("BALTIC", "Russian cargo ship still burning off Finland", draw_ship_fire),
        ("KYIV", "14 missing after drone hits a Kyiv building", draw_building_drone),
        ("INDONESIA", "Candy-factory fire: 3 dead, 50 missing", draw_factory),
        ("SOUTH KOREA", "Education minister quits over AI-cheating scandal", draw_chair_chip),
        ("INDIA", "India 720/9d — record Test total v New Zealand", draw_scoreboard),
    ]
    strip_y = hy + 16
    strip_h = 1024 - strip_y - 20
    rows, cols = 2, 3
    gap = 12
    tile_w = (1024 - 48 - (cols - 1) * gap) // cols
    tile_h = (strip_h - (rows - 1) * gap) // rows
    icon_s = u(76)
    for i, (kick, label, icon_fn) in enumerate(tiles):
        r, c = divmod(i, cols)
        x = u(24 + c * (tile_w + gap))
        y = u(strip_y + r * (tile_h + gap))
        tw_, th_ = u(tile_w), u(tile_h)
        d.rounded_rectangle([x, y, x + tw_, y + th_], radius=u(9),
                            fill=PANEL, outline=PANEL_LINE, width=u(1))
        ix = x + u(14)
        iy = y + u(12)
        icon_fn(d, ix, iy, icon_s)
        kf = fit_font(d, kick, BOLD, tile_w - 14 - 76 - 10 - 14, 22)
        d.text((ix + icon_s + u(10), y + u(16)), kick, font=kf, fill=SAFETY)
        lf = font(REG, 21)
        lines = wrap(d, label, lf, tile_w - 28)
        ly = iy + icon_s + u(12)
        for line in lines[:3]:
            d.text((x + u(14), ly), line, font=lf, fill=CREAM)
            ly += int(lf.size * 1.22)

    out = img.resize((1024, 1024), Image.LANCZOS)
    path = os.path.join(HERE, "news.png")
    out.save(path, format="PNG", optimize=True)
    print(f"wrote {path} {os.path.getsize(path)} bytes")


if __name__ == "__main__":
    build()
