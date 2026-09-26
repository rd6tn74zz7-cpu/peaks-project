"""Карточка-анонс матча для Telegram-канала (1080x1350)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img


def pitch_lines(img):
    """Полупрозрачная разметка поля на фоне."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = (255, 255, 255, 28)
    m = 60
    d.rectangle([m, m, W - m, H - m], outline=c, width=5)
    d.line([(m, H // 2), (W - m, H // 2)], fill=c, width=5)
    d.ellipse([W // 2 - 170, H // 2 - 170, W // 2 + 170, H // 2 + 170], outline=c, width=5)
    d.rectangle([W // 2 - 260, m, W // 2 + 260, m + 190], outline=c, width=5)
    d.rectangle([W // 2 - 260, H - m - 190, W // 2 + 260, H - m], outline=c, width=5)
    return Image.alpha_composite(img.convert("RGBA"), layer)


def flag_england(w, h):
    f = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(f)
    t = h // 5
    d.rectangle([0, h // 2 - t // 2, w, h // 2 + t // 2], fill=(206, 17, 36))
    d.rectangle([w // 2 - t // 2, 0, w // 2 + t // 2, h], fill=(206, 17, 36))
    return f


def flag_spain(w, h):
    f = Image.new("RGB", (w, h), (170, 21, 27))
    ImageDraw.Draw(f).rectangle([0, h // 4, w, h * 3 // 4], fill=(241, 191, 0))
    return f


def paste_flag(img, flag, cx, cy):
    w, h = flag.size
    shadow = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([30, 36, w + 30, h + 36], 18, fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    img.alpha_composite(shadow, (cx - w // 2 - 30, cy - h // 2 - 30))
    mask = Image.new("L", flag.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=255)
    img.paste(flag, (cx - w // 2, cy - h // 2), mask)
    ImageDraw.Draw(img).rounded_rectangle(
        [cx - w // 2, cy - h // 2, cx + w // 2 - 1, cy + h // 2 - 1], 18, outline=(255, 255, 255), width=4)


def center(d, y, text, f, fill):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


def pill(d, y, text, f, bg, fg):
    tw = d.textlength(text, font=f)
    pad_x, h = 34, f.size + 30
    x0 = (W - tw) / 2 - pad_x
    d.rounded_rectangle([x0, y, x0 + tw + 2 * pad_x, y + h], h // 2, fill=bg)
    d.text((x0 + pad_x, y + 13), text, font=f, fill=fg)


img = pitch_lines(gradient(W, H, (8, 24, 58), (4, 70, 52)))
d = ImageDraw.Draw(img)

pill(d, 110, "ЛИГА НАЦИЙ УЕФА  •  1 ТУР", font(BOLD, 38), (255, 196, 0), (10, 20, 40))
center(d, 215, "ГЛАВНЫЙ МАТЧ ДНЯ", font(BOLD, 44), (255, 255, 255, 190))

fy = 520
paste_flag(img, flag_england(300, 200), 270, fy)
paste_flag(img, flag_spain(300, 200), W - 270, fy)
d = ImageDraw.Draw(img)
center(d, fy - 58, "VS", font(BOLD, 96), (255, 196, 0))

names = font(BOLD, 64)
for name, cx in (("АНГЛИЯ", 270), ("ИСПАНИЯ", W - 270)):
    d.text((cx - d.textlength(name, font=names) / 2, fy + 140), name, font=names, fill=(255, 255, 255))

d.line([(140, 860), (W - 140, 860)], fill=(255, 255, 255, 70), width=3)
center(d, 900, "СЕГОДНЯ, 26 СЕНТЯБРЯ", font(BOLD, 56), (255, 255, 255))
center(d, 985, "21:45 МСК", font(BOLD, 110), (255, 196, 0))
center(d, 1130, "Стадион «Уэмбли», Лондон", font(REG, 42), (255, 255, 255, 220))
center(d, 1190, "Испания — действующий чемпион мира", font(REG, 38), (255, 255, 255, 170))

img.convert("RGB").save("cards/england-spain-2026-09-26.png", optimize=True)
print("saved")
