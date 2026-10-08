# -*- coding: utf-8 -*-
"""
브랜드 이미지 생성: assets/img/brand/og.png (1200x630), apple-touch-icon.png (180x180)
  python tools/make_brand.py
Pretendard 폰트(사용자 폰트 폴더) 또는 맑은 고딕을 사용한다.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join(ROOT, 'assets', 'img', 'brand')
ICONS = os.path.join(ROOT, 'assets', 'img', 'icons')

USER_FONTS = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'Fonts')


def font(weight, size):
    cands = {
        'bold': [os.path.join(USER_FONTS, 'Pretendard-Bold.ttf'), r'C:\Windows\Fonts\malgunbd.ttf'],
        'semi': [os.path.join(USER_FONTS, 'Pretendard-SemiBold.ttf'), r'C:\Windows\Fonts\malgunbd.ttf'],
        'reg': [os.path.join(USER_FONTS, 'Pretendard-Regular.ttf'), r'C:\Windows\Fonts\malgun.ttf'],
    }[weight]
    for c in cands:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def grad_square(size, radius):
    """로고 마크: 대각선 그라데이션 라운드 사각형 + N"""
    s = size * 4
    stops = [(0, (154, 168, 255)), (.55, (196, 167, 255)), (1, (255, 174, 211))]
    g = Image.new('RGB', (s, s))
    px = g.load()
    for y in range(s):
        for x in range(s):
            t = (x + y) / (2 * (s - 1))
            for i in range(len(stops) - 1):
                if stops[i][0] <= t <= stops[i + 1][0]:
                    tt = (t - stops[i][0]) / (stops[i + 1][0] - stops[i][0])
                    px[x, y] = lerp(stops[i][1], stops[i + 1][1], tt)
                    break
    mask = Image.new('L', (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, s - 1, s - 1), radius * 4, fill=255)
    out = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    out.paste(g, (0, 0), mask)
    d = ImageDraw.Draw(out)
    k = s / 32
    pts = [(10.5 * k, 22 * k), (10.5 * k, 10 * k), (21.5 * k, 22 * k), (21.5 * k, 10 * k)]
    w = int(3.2 * k)
    d.line(pts, fill=(10, 11, 16), width=w, joint='curve')
    for p in (pts[0], pts[-1]):
        d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=(10, 11, 16))
    return out.resize((size, size), Image.LANCZOS)


def rounded(im, r):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    o = Image.new('RGBA', im.size, (0, 0, 0, 0))
    o.paste(im.convert('RGBA'), (0, 0), m)
    return o


def apple_touch():
    # iOS가 모서리를 자르므로 사각형 그대로(배경 포함) 만든다
    icon = grad_square(180, 0)
    icon.convert('RGB').save(os.path.join(BRAND, 'apple-touch-icon.png'))


def og():
    W, H = 1200, 630
    img = Image.new('RGB', (W, H), (6, 7, 10))
    glow = Image.new('RGB', (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((700, -260, 1400, 440), fill=(80, 64, 220))
    gd.ellipse((-260, 330, 380, 900), fill=(22, 82, 220))
    gd.ellipse((560, 420, 980, 820), fill=(200, 70, 140))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    img = Image.blend(img, glow, .55)
    # grid
    grid = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdd = ImageDraw.Draw(grid)
    for x in range(0, W, 60):
        gdd.line([(x, 0), (x, H)], fill=(255, 255, 255, 10))
    for y in range(0, H, 60):
        gdd.line([(0, y), (W, y)], fill=(255, 255, 255, 10))
    img = img.convert('RGBA')
    img.alpha_composite(grid)

    d = ImageDraw.Draw(img)
    mark = grad_square(64, 18)
    img.alpha_composite(mark, (80, 78))
    d.text((160, 84), 'NeoMax', font=font('bold', 46), fill=(244, 245, 248))

    d.text((80, 210), '손끝에서 시작되는', font=font('bold', 72), fill=(244, 245, 248))
    # gradient headline
    t2 = '작고 단단한 재미.'
    f2 = font('bold', 72)
    bbox = d.textbbox((0, 0), t2, font=f2)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1] + 20
    tm = Image.new('L', (tw + 10, th + 20), 0)
    ImageDraw.Draw(tm).text((0, 0), t2, font=f2, fill=255)
    gr = Image.new('RGB', tm.size)
    gp = gr.load()
    for x in range(tm.width):
        t = x / max(1, tm.width - 1)
        c = lerp((154, 168, 255), (196, 167, 255), t / .45) if t < .45 else lerp((196, 167, 255), (255, 174, 211), (t - .45) / .55)
        for y in range(tm.height):
            gp[x, y] = c
    img.paste(gr, (80, 300), tm)

    d.text((82, 412), '모바일 게임과 앱을 만드는 작은 스튜디오', font=font('reg', 28), fill=(170, 176, 190))

    # icons row
    slugs = ['truckrush', 'harukan', 'golfrush', 'yobung', 'guimoon', 'challenger18']
    x = 80
    for s in slugs:
        p = os.path.join(ICONS, f'{s}.webp')
        ic = Image.open(p).convert('RGB').resize((72, 72), Image.LANCZOS)
        img.alpha_composite(rounded(ic, 17), (x, 486))
        x += 88
    img.convert('RGB').save(os.path.join(BRAND, 'og.png'), optimize=True)


if __name__ == '__main__':
    apple_touch()
    og()
    print('brand images done')
