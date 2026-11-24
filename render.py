#!/usr/bin/env python3
"""Render the news-image-20261123 front page (1024x1024 PNG) at build time.

Draws a newspaper front page summing up Monday 23 November 2026:
hero = Ukraine's sea-drone strike on the Russian corvette Merkury off
Benghazi, Libya (worded as Kyiv's claim, per the brief), six story cards,
and a one-liner ticker. Deterministic: fixed coordinates, no randomness,
no network, no external images. Run: python3 render.py -> entry.png
"""
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent

PAPER = (246, 241, 231)
INK = (26, 26, 26)
RED = (179, 38, 30)
NAVY = (22, 50, 79)
GREY = (120, 118, 110)
CARD_BG = (255, 255, 255)
CARD_LINE = (150, 148, 140)

F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
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


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def draw_hero_sea(d, x0, y0, w, h):
    """Night harbour: dusk sky, dark sea, warship, explosion, sea drone."""
    # sky gradient: dark navy -> dusk orange at the horizon
    top = (16, 34, 58)
    mid = (38, 70, 96)
    hor = (214, 110, 48)
    for yy in range(h):
        t = yy / max(h - 1, 1)
        if t < 0.55:
            k = t / 0.55
            c = tuple(int(top[i] + (mid[i] - top[i]) * k) for i in range(3))
        else:
            k = (t - 0.55) / 0.45
            c = tuple(int(mid[i] + (hor[i] - mid[i]) * k) for i in range(3))
        d.line([(x0, y0 + yy), (x0 + w - 1, y0 + yy)], fill=c)
    sea_y = y0 + int(h * 0.62)
    d.rectangle([x0, sea_y, x0 + w, y0 + h], fill=(10, 27, 46))
    # harbour cranes, left horizon
    d.line([(x0 + 60, sea_y), (x0 + 60, sea_y - 46)], fill=(8, 18, 32), width=5)
    d.line([(x0 + 60, sea_y - 46), (x0 + 118, sea_y - 38)], fill=(8, 18, 32), width=4)
    d.line([(x0 + 118, sea_y - 38), (x0 + 118, sea_y)], fill=(8, 18, 32), width=3)
    d.rectangle([x0 + 150, sea_y - 26, x0 + 210, sea_y], fill=(8, 18, 32))
    d.rectangle([x0 + 216, sea_y - 16, x0 + 258, sea_y], fill=(8, 18, 32))
    # sun glow low on the horizon, right
    d.ellipse([x0 + w - 190, sea_y - 34, x0 + w - 130, sea_y + 26], fill=(232, 150, 60))
    # warship silhouette (grey), right of centre, slightly listing
    hx, hy = x0 + 470, sea_y - 8
    hull = [(hx, hy), (hx + 330, hy), (hx + 360, hy + 22),
            (hx + 340, hy + 30), (hx + 20, hy + 30), (hx - 8, hy + 12)]
    d.polygon(hull, fill=(74, 84, 94))
    d.rectangle([hx + 60, hy - 34, hx + 180, hy], fill=(84, 94, 104))
    d.rectangle([hx + 190, hy - 26, hx + 250, hy], fill=(84, 94, 104))
    d.rectangle([hx + 96, hy - 58, hx + 128, hy - 34], fill=(94, 104, 114))
    # mast leaning after the blast: the ship is stricken, not intact
    d.line([(hx + 112, hy - 58), (hx + 130, hy - 82)], fill=(94, 104, 114), width=4)
    d.polygon([(hx + 300, hy - 6), (hx + 340, hy - 6), (hx + 330, hy - 16)],
              fill=(64, 74, 84))
    # portholes
    for px in range(hx + 30, hx + 330, 34):
        d.ellipse([px, hy + 8, px + 7, hy + 15], fill=(232, 190, 90))
    # scorch and deck flames at the impact point: the bow is blackened
    # and burning (Kyiv claims sunk; Libya says severely damaged)
    d.polygon([(hx + 268, hy + 2), (hx + 348, hy + 2), (hx + 340, hy + 28),
               (hx + 276, hy + 30)], fill=(18, 18, 20))
    for fx, fy, fh in [(hx + 282, hy, 16), (hx + 300, hy, 22), (hx + 320, hy, 14)]:
        d.polygon([(fx - 7, fy), (fx, fy - fh), (fx + 7, fy)],
                  fill=(245, 160, 40))
    # explosion at the bow: orange core, yellow heart, smoke
    ex, ey = hx + 330, hy - 26
    for r, c in [(46, (200, 70, 20)), (34, (240, 120, 30)), (20, (250, 200, 80))]:
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=c)
    d.polygon([(ex - 8, ey - 30), (ex + 6, ey - 62), (ex + 18, ey - 28),
               (ex + 34, ey - 52), (ex + 30, ey - 18), (ex + 8, ey - 6)],
              fill=(245, 160, 40))
    for sx, sy, sr in [(ex - 40, ey - 52, 15), (ex - 14, ey - 66, 18),
                       (ex + 16, ey - 54, 13), (ex + 42, ey - 46, 10)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 90, 92))
    # thick smoke column rising from mid-deck (kept inside the sea box)
    for sx, sy, sr in [(hx + 150, hy - 44, 13), (hx + 136, hy - 64, 16),
                       (hx + 150, hy - 84, 13)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(70, 70, 74))
    # sea drones, left, speeding in with bright white wakes. The strike
    # used 7 drones; two are shown, the lead one large so the weapon
    # itself is readable instead of a near-invisible sliver.
    dx, dy = x0 + 96, sea_y + 30
    d.line([(dx, dy), (dx - 72, dy - 5)], fill=(225, 230, 235), width=3)
    d.line([(dx, dy + 5), (dx - 88, dy + 12)], fill=(225, 230, 235), width=3)
    d.line([(dx, dy - 5), (dx - 60, dy - 14)], fill=(195, 202, 210), width=2)
    d.polygon([(dx, dy - 10), (dx + 96, dy), (dx, dy + 10), (dx + 14, dy)],
              fill=(22, 26, 32))
    d.rectangle([dx + 30, dy - 16, dx + 48, dy - 6], fill=(40, 46, 54))
    d.line([(dx + 39, dy - 16), (dx + 39, dy - 28)], fill=(40, 46, 54), width=3)
    # second drone trailing nearer the waterline
    dx2, dy2 = x0 + 40, sea_y + 10
    d.line([(dx2, dy2 + 3), (dx2 - 30, dy2 + 8)], fill=(200, 208, 215), width=2)
    d.polygon([(dx2, dy2 - 7), (dx2 + 54, dy2), (dx2, dy2 + 7), (dx2 + 9, dy2)],
              fill=(22, 26, 32))
    # wave strokes
    for wx in range(x0 + 20, x0 + w - 40, 90):
        d.arc([wx, sea_y + 52, wx + 56, sea_y + 66], 200, 340,
              fill=(70, 100, 130), width=2)
    for wx in range(x0 + 60, x0 + w - 40, 110):
        d.arc([wx, sea_y + 84, wx + 48, sea_y + 96], 200, 340,
              fill=(60, 88, 116), width=2)


def draw_chip(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(14, 107, 58))
    cx, cy = x0 + w // 2, y0 + h // 2
    for i in range(4):
        d.line([(cx - 52, cy - 26 + i * 17), (cx - 34, cy - 26 + i * 17)],
               fill=(212, 175, 55), width=3)
        d.line([(cx + 34, cy - 26 + i * 17), (cx + 52, cy - 26 + i * 17)],
               fill=(212, 175, 55), width=3)
    d.rectangle([cx - 34, cy - 30, cx + 34, cy + 30], fill=(20, 60, 35),
                outline=(212, 175, 55), width=3)
    d.text((cx - 13, cy - 13), "NV", font=font(F_SANS_B, 24), fill=(255, 255, 255))


def draw_bank(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 224, 208))
    cx = x0 + w // 2
    d.polygon([(cx - 70, y0 + 14), (cx + 70, y0 + 14), (cx, y0 + 34)],
              fill=(58, 58, 58))
    for i in range(4):
        px = cx - 54 + i * 36
        d.rectangle([px, y0 + 38, px + 12, y0 + h - 8], fill=(58, 58, 58))
    d.rectangle([cx - 70, y0 + h - 10, cx + 70, y0 + h - 6], fill=(58, 58, 58))
    d.line([(x0 + 26, y0 + h - 8), (x0 + w - 26, y0 + 6)], fill=(179, 38, 30),
           width=5)


def draw_factory(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(43, 43, 43))
    d.rectangle([x0 + 30, y0 + h - 34, x0 + w - 30, y0 + h - 6], fill=(17, 17, 17))
    d.rectangle([x0 + 46, y0 + 12, x0 + 66, y0 + h - 34], fill=(17, 17, 17))
    d.polygon([(x0 + 46, y0 + 12), (x0 + 56, y0 - 2), (x0 + 66, y0 + 12)],
              fill=(245, 160, 40))
    for fx, fy in [(x0 + 96, y0 + 22), (x0 + 120, y0 + 14), (x0 + 142, y0 + 24)]:
        d.polygon([(fx - 12, fy + 8), (fx, fy - 12), (fx + 12, fy + 8)],
                  fill=(240, 120, 30))
    for wx in range(x0 + 80, x0 + w - 50, 34):
        d.rectangle([wx, y0 + h - 22, wx + 14, y0 + h - 12], fill=(240, 200, 90))


def draw_globe(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(220, 233, 242))
    cx, cy, r = x0 + w // 2, y0 + h // 2, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 125, 50))
    d.ellipse([cx - r + 8, cy - r + 10, cx - r + 26, cy - r + 24], fill=(139, 195, 74))
    d.ellipse([cx + 2, cy + 6, cx + 22, cy + 20], fill=(139, 195, 74))
    d.line([(cx - r + 5, cy - r + 2), (cx + 2, cy - 2), (cx + 12, cy + 12),
            (cx + r - 8, cy + r - 10)], fill=(255, 255, 255), width=3)


def draw_truck(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(239, 230, 210))
    d.rectangle([x0 + 52, y0 + 18, x0 + 210, y0 + 44], fill=(138, 109, 59))
    d.rectangle([x0 + 214, y0 + 26, x0 + 252, y0 + 44], fill=(100, 78, 42))
    d.rectangle([x0 + 224, y0 + 30, x0 + 240, y0 + 38], fill=(220, 233, 242))
    for wx in (x0 + 84, x0 + 176, x0 + 232):
        d.ellipse([wx - 11, y0 + 42, wx + 11, y0 + 64 - 6 + 6], fill=(26, 26, 26))
        d.ellipse([wx - 4, y0 + 49, wx + 4, y0 + 57], fill=(150, 150, 150))
    for sx, sy, sr in [(x0 + 250, y0 + 12, 8), (x0 + 268, y0 + 6, 11)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 122))


def draw_court(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(228, 234, 240))
    cx = x0 + w // 2
    d.polygon([(cx - 76, y0 + 12), (cx + 76, y0 + 12), (cx, y0 + 32)],
              fill=(74, 90, 106))
    for i in range(4):
        px = cx - 58 + i * 38
        d.rectangle([px, y0 + 36, px + 12, y0 + h - 8], fill=(74, 90, 106))
    d.rectangle([cx - 76, y0 + h - 10, cx + 76, y0 + h - 6], fill=(74, 90, 106))


CARDS = [
    ("NVIDIA", "Huang back as Nvidia CEO",
     "Board reinstates Jensen Huang 11 days after his resignation; "
     "shares jump ~33% as the Nasdaq climbs 6%.", draw_chip),
    ("IRAN", "US sanctions Iran's shadow banks",
     "Treasury targets 20+ dozen exchange houses in 'Operation Economic "
     "Outcast'; Trump warns of strikes in the new year.", draw_bank),
    ("CIKANDE", "Cikande fire: 24 dead, ~30 missing",
     "Indonesia confirms the toll from the Sat 21 Nov candy-factory blaze; "
     "DNA identification will take weeks.", draw_factory),
    ("CLIMATE", "COP31: 'darkest moment' for climate talks",
     "After the Antalya collapse, 90+ nations back an electrification pledge; "
     "talks resume at COP32 in Ethiopia.", draw_globe),
    ("GAZA", "Gaza strike kills 3; Eisenkot condemns arson",
     "Israel's PM-elect calls West Bank attacks 'Jewish terrorism' after "
     "burned vehicles are found near Ramallah.", draw_truck),
    ("BANGLADESH", "Hasina will be jailed if she returns",
     "Bangladesh tells Reuters it will arrest the former PM on her return "
     "from India.", draw_court),
]

TICKER = ("US mulls training Syrian forces  •  SK hynix +20% on Huang's return  •  "
          "Oregon & Virginia sue SpaceX over AI safety  •  Thousands rally in Istanbul  •  "
          "Nigeria boat rescue race  •  Nepal PM visits Delhi; India pledges $1.63B  •  "
          "UN chief urges an AI safety framework  •  Merz warns Russia over 'dangerous provocations'")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.line([(16, 10), (1008, 10)], fill=INK, width=3)
    title = "THE WORLD IN ONE IMAGE"
    tf = font(F_SERIF_B, 56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 16), title, font=tf, fill=INK)
    d.line([(16, 84), (1008, 84)], fill=INK, width=1)
    date = "MONDAY  23  NOVEMBER  2026"
    df = font(F_SANS_B, 21)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 88), date, font=df, fill=RED)
    d.line([(16, 114), (1008, 114)], fill=INK, width=2)

    # ---- hero ----
    hx0, hy0, hw, hh = 16, 126, 992, 356
    d.rectangle([hx0, hy0, hx0 + hw, hy0 + hh], outline=INK, width=2)
    draw_hero_sea(d, hx0 + 2, hy0 + 2, hw - 4, 190)
    kicker = "KYIV CLAIMS  —  LIBYA SAYS SEVERELY DAMAGED"
    kf = font(F_SANS_B, 17)
    d.text((hx0 + 16, hy0 + 200), kicker, font=kf, fill=RED)
    head = ["UKRAINIAN DRONES SINK", "RUSSIAN WARSHIP IN LIBYA"]
    hf = font(F_SERIF_B, 42)
    y = hy0 + 220
    for ln in head:
        d.text((hx0 + 16, y), ln, font=hf, fill=INK)
        y += 46
    sub = ("Corvette Merkury hit by 7 sea drones at the Benghazi naval base; "
           "a helicopter aboard was destroyed and the cargo ship Angara also "
           "struck — 2,400 km from the front line.")
    sf = font(F_SANS, 18)
    text_block(d, hx0 + 16, y + 2, wrap(d, sub, sf, hw - 32), sf, INK, 21)

    # ---- grid of six cards ----
    gx, gy = 16, 496
    cw, ch, gap = 320, 188, 16
    for i, (tag, title, body, art) in enumerate(CARDS):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD_BG,
                    outline=CARD_LINE, width=1)
        art(d, cx + 1, cy + 1, cw - 2, 62)
        d.line([(cx, cy + 63), (cx + cw, cy + 63)], fill=CARD_LINE, width=1)
        tf2 = font(F_SANS_B, 12)
        d.text((cx + 10, cy + 70), tag, font=tf2, fill=RED)
        title_f = font(F_SANS_B, 19)
        ty = text_block(d, cx + 10, cy + 88,
                        wrap(d, title, title_f, cw - 20), title_f, INK, 21)
        body_f = font(F_SANS, 14)
        text_block(d, cx + 10, ty + 2,
                   wrap(d, body, body_f, cw - 20)[:3], body_f, (60, 60, 60), 17)

    # ---- ticker ----
    tx0, ty0, tw_, th = 16, 900, 992, 108
    d.rectangle([tx0, ty0, tx0 + tw_, ty0 + th], fill=NAVY)
    lab = "ALSO TODAY"
    lf = font(F_SANS_B, 17)
    d.text((tx0 + 14, ty0 + 10), lab, font=lf, fill=(240, 200, 90))
    tick_f = font(F_SANS, 16)
    text_block(d, tx0 + 14, ty0 + 34,
               wrap(d, TICKER, tick_f, tw_ - 28), tick_f, (235, 235, 235), 21)

    out = HERE / "entry.png"
    img.save(out, "PNG")
    data = out.read_bytes()
    print("wrote", out, len(data), "bytes",
          "md5", hashlib.md5(data).hexdigest())


if __name__ == "__main__":
    main()
