"""Draw the front page for news-image-20261120.

A newspaper front page summing up the world's news of Friday 20 November
2026: the ICJ genocide ruling, the Shenzhen peace declaration, the Houthi
strike on Riyadh, the COP31 draft, and the Kyiv missile strikes, plus a
ticker of the day's other stories. Everything is drawn with Pillow
primitives; no network, no downloaded assets.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (31, 73, 125)
LIGHT_BLUE = (214, 230, 244)
GOLD = (201, 162, 39)
GREEN = (46, 125, 50)
ORANGE = (214, 105, 30)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def scales_of_justice(draw, x, y, s, ink):
    """Simple balanced scales: pole, beam, two pans, base."""
    cx, top = x + s // 2, y
    draw.line([cx, top, cx, top + int(s * 0.62)], fill=ink, width=5)
    draw.line([x + 8, top + int(s * 0.14), x + s - 8, top + int(s * 0.14)],
              fill=ink, width=5)
    draw.ellipse([cx - 7, top - 7, cx + 7, top + 7], fill=GOLD)
    for side in (-1, 1):
        px = cx + side * (s // 2 - 14)
        draw.line([px, top + int(s * 0.14), px, top + int(s * 0.42)],
                  fill=ink, width=3)
        draw.line([px - 26, top + int(s * 0.14), px, top + int(s * 0.14)],
                  fill=ink, width=3)
        draw.line([px + 26, top + int(s * 0.14), px, top + int(s * 0.14)],
                  fill=ink, width=3)
        draw.arc([px - 30, top + int(s * 0.40), px + 30, top + int(s * 0.56)],
                 start=0, end=180, fill=ink, width=4)
    draw.line([cx - 34, top + int(s * 0.62), cx + 34, top + int(s * 0.62)],
              fill=ink, width=5)
    draw.line([cx - 22, top + int(s * 0.70), cx + 22, top + int(s * 0.70)],
              fill=ink, width=5)


def flag_us(draw, x, y, w, h):
    for i in range(7):
        draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                       fill=RED if i % 2 == 0 else PAPER)
    draw.rectangle([x, y, x + int(w * 0.4), y + int(h * 0.55)], fill=BLUE)
    for r in range(3):
        for c in range(4):
            draw.ellipse([x + 6 + c * 12, y + 5 + r * 11,
                          x + 11 + c * 12, y + 10 + r * 11], fill=PAPER)


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=RED)
    draw.ellipse([x + 8, y + 6, x + 22, y + 20], fill=GOLD)
    for sx, sy in [(34, 8), (44, 16), (44, 28), (34, 34)]:
        draw.ellipse([x + sx, y + sy, x + sx + 7, y + sy + 7], fill=GOLD)


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h // 3], fill=PAPER)
    draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=BLUE)
    draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=RED)


def burst(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def story_card(draw, x, y, w, h, accent, kicker, headline, body, scene):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=(120, 120, 120), width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=accent)
    scene(draw, x + 12, y + 20, 118, h - 32)
    tx = x + 142
    draw.text((tx, y + 18), kicker, font=font(SANS_B, 19), fill=accent)
    lines = wrap(draw, headline, font(SANS_B, 27), w - 158)
    ly = y + 46
    for ln in lines[:2]:
        draw.text((tx, ly), ln, font=font(SANS_B, 27), fill=INK)
        ly += 32
    blines = wrap(draw, body, font(SANS, 20), w - 158)
    for ln in blines[:3]:
        draw.text((tx, ly + 4), ln, font=font(SANS, 20), fill=(60, 60, 60))
        ly += 25


def scene_flags(draw, x, y, w, h):
    flag_us(draw, x + 4, y + 18, 34, 24)
    flag_cn(draw, x + 42, y + 18, 34, 24)
    flag_ru(draw, x + 80, y + 18, 34, 24)
    draw.ellipse([x + 30, y + 62, x + 88, y + 120], fill=GOLD,
                 outline=INK, width=2)
    peace = "PEACE"
    pf = font(SANS_B, 15)
    draw.text((x + 59 - draw.textlength(peace, font=pf) / 2, y + 82), peace,
              font=pf, fill=INK)


def scene_tower(draw, x, y, w, h):
    draw.rectangle([x + 34, y + 30, x + 84, y + 132], fill=(70, 70, 78))
    draw.polygon([(x + 34, y + 30), (x + 84, y + 30), (x + 59, y + 6)],
                 fill=(70, 70, 78))
    for wy in range(40, 128, 16):
        for wx in (44, 64):
            draw.rectangle([x + wx, y + wy, x + wx + 8, y + wy + 8],
                           fill=GOLD)
    burst(draw, x + 59, y + 26, 26, ORANGE)
    burst(draw, x + 59, y + 26, 14, GOLD)
    draw.ellipse([x + 8, y + 6, x + 34, y + 26], fill=(150, 150, 150))
    draw.ellipse([x + 84, y + 12, x + 106, y + 30], fill=(150, 150, 150))


def scene_climate(draw, x, y, w, h):
    draw.ellipse([x + 24, y + 14, x + 94, y + 84], fill=GOLD)
    for i in range(8):
        import math
        a = math.pi * i / 4
        draw.line([x + 59 + 42 * math.cos(a), y + 49 + 42 * math.sin(a),
                   x + 59 + 52 * math.cos(a), y + 49 + 52 * math.sin(a)],
                  fill=ORANGE, width=4)
    draw.arc([x + 6, y + 74, x + 112, y + 140], start=180, end=360,
             fill=GREEN, width=6)
    draw.arc([x + 22, y + 86, x + 96, y + 142], start=180, end=360,
             fill=GREEN, width=6)
    draw.text((x + 34, y + 116), "CO2", font=font(SANS_B, 22), fill=RED)


def scene_missile(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(38, 44, 60))
    draw.line([x + 14, y + 96, x + 52, y + 40], fill=(200, 200, 200), width=10)
    draw.polygon([(x + 52, y + 40), (x + 66, y + 30), (x + 62, y + 52)],
                 fill=(200, 200, 200))
    burst(draw, x + 20, y + 104, 18, ORANGE)
    burst(draw, x + 20, y + 104, 9, GOLD)
    draw.ellipse([x + 82, y + 14, x + 88, y + 20], fill=PAPER)
    draw.ellipse([x + 96, y + 30, x + 100, y + 34], fill=PAPER)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.line([28, 20, W - 28, 20], fill=INK, width=4)
    draw_center(d, W // 2, 30, "THE WORLD IN ONE DAY",
                font(SERIF_B, 62))
    d.line([28, 108, W - 28, 108], fill=INK, width=2)
    d.line([28, 113, W - 28, 113], fill=INK, width=4)

    # Dateline band
    d.rectangle([28, 126, W - 28, 168], fill=RED)
    draw_center(d, W // 2, 132, "FRIDAY 20 NOVEMBER 2026",
                font(SANS_B, 30), fill=(255, 255, 255))
    draw_center(d, W // 2, 176, "Six stories that defined the day",
                font(SANS, 21), fill=(90, 90, 90))

    # Lead story: ICJ genocide ruling
    lx, ly, lw, lh = 28, 208, W - 56, 262
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=(255, 255, 255),
                outline=(120, 120, 120), width=2)
    d.rectangle([lx, ly, lx + lw, ly + 8], fill=BLUE)
    d.rectangle([lx + 14, ly + 22, lx + 300, ly + lh - 14], fill=LIGHT_BLUE)
    scales_of_justice(d, lx + 74, ly + 52, 170, INK)
    tx = lx + 330
    d.text((tx, ly + 20), "THE HAGUE  •  JUSTICE", font=font(SANS_B, 20),
           fill=RED)
    head = "MYANMAR GUILTY OF GENOCIDE"
    head_lines = wrap(d, head, font(SANS_B, 40), lw - 360)
    for i, ln in enumerate(head_lines):
        d.text((tx, ly + 48 + i * 46), ln, font=font(SANS_B, 40), fill=INK)
    body = ("The UN court rules Myanmar committed genocide against the "
            "Rohingya in 2017 — a historic first finding against a state. "
            "Refugees in Bangladesh cheer the verdict.")
    by = ly + 48 + len(head_lines) * 46 + 8
    for i, ln in enumerate(wrap(d, body, font(SANS, 22), lw - 360)):
        d.text((tx, by + i * 28), ln, font=font(SANS, 22), fill=(60, 60, 60))

    # Four-story grid
    gy, gh, gap = 486, 188, 14
    cw = (W - 56 - gap) // 2
    cards = [
        (28, gy, BLUE, "SHENZHEN  •  DIPLOMACY",
         "TRUMP, XI & PUTIN SIGN PEACE DECLARATION",
         "First trilateral summit ends with a joint peace statement; "
         "Ukraine tops the agenda.", scene_flags),
        (28 + cw + gap, gy, RED, "RIYADH  •  CONFLICT",
         "HOUTHI MISSILE HITS RIYADH'S TALLEST TOWER",
         "Strike damages the kingdom's tallest skyscraper; Riyadh vows "
         "a response.", scene_tower),
        (28, gy + gh + gap, GREEN, "ANTALYA  •  CLIMATE",
         "COP31 DRAFT DROPS FOSSIL FUELS",
         "Outcry as fossil-fuel wording is cut from the draft UN climate "
         "deal.", scene_climate),
        (28 + cw + gap, gy + gh + gap, (38, 44, 60), "KYIV  •  WAR",
         "KYIV HIT BY FOUR BALLISTIC MISSILES",
         "Ukraine war grinds on as peace talks stall and frontline "
         "strikes mount.", scene_missile),
    ]
    for x, y, accent, kicker, headline, body, scene in cards:
        story_card(d, x, y, cw, gh, accent, kicker, headline, body, scene)

    # Footer ticker
    fy = 892
    d.rectangle([28, fy, W - 28, fy + 100], fill=INK)
    ticker = ("ALSO TODAY:  S&P 500 falls 2.0% for a fifth straight loss  •  "
              "Tanker on fire after mine strike near the Strait of Hormuz  •  "
              "Drones halt flights at Genoa airport  •  India evacuates 80,000 "
              "as Cyclone Dana nears the coast")
    ty = fy + 10
    for ln in wrap(d, ticker, font(SANS, 19), W - 96):
        d.text((48, ty), ln, font=font(SANS, 19), fill=(255, 255, 255))
        ty += 25

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
