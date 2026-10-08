# -*- coding: utf-8 -*-
"""
NeoMax 웹사이트 이미지 가공 스크립트.

원본(Play 스토어에서 받은 PNG, 로컬 스토어 그래픽)을 사이트용 WebP로 줄인다.
  python tools/process_images.py <원본폴더> <로컬그래픽폴더>

원본 파일 이름 규칙: <slug>_icon.png, <slug>_shotNN.png
결과: assets/img/icons/<slug>.webp (256px), assets/img/shots/<slug>-NN.webp (가로 600px)
"""
import sys, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '_src', 'raw')
LOCAL = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, '_src', 'local')

ICON_DIR = os.path.join(ROOT, 'assets', 'img', 'icons')
SHOT_DIR = os.path.join(ROOT, 'assets', 'img', 'shots')
ART_DIR = os.path.join(ROOT, 'assets', 'img', 'art')
for d in (ICON_DIR, SHOT_DIR, ART_DIR):
    os.makedirs(d, exist_ok=True)

# 사이트에 쓰는 스크린샷 순서 (Play 등록 순서 기준 번호)
SHOTS = {
    'truckrush':    [1, 2, 3, 4, 5, 6, 7],
    'harukan':      [3, 1, 2, 4, 5, 6, 7, 8],
    'golfrush':     [1, 2, 3, 4, 5],
    'yobung':       [6, 3, 2, 4, 5],
    'guimoon':      [4, 2, 3, 1],
    'challenger18': [1, 7, 2, 3, 4, 5, 6],
}

def save_webp(im, path, quality=82):
    im.save(path, 'WEBP', quality=quality, method=6)
    return os.path.getsize(path) // 1024

total = 0
# 아이콘
for slug in SHOTS:
    src = os.path.join(RAW, f'{slug}_icon.png')
    if slug == 'guimoon' and os.path.exists(os.path.join(LOCAL, 'guimoon_icon_new.png')):
        src = os.path.join(LOCAL, 'guimoon_icon_new.png')  # 2026-10-08 새 아이콘
    im = Image.open(src).convert('RGB').resize((256, 256), Image.LANCZOS)
    total += save_webp(im, os.path.join(ICON_DIR, f'{slug}.webp'), 88)

# 스크린샷
for slug, order in SHOTS.items():
    for i, n in enumerate(order, 1):
        src = os.path.join(RAW, f'{slug}_shot{n:02d}.png')
        im = Image.open(src).convert('RGB')
        w = 600
        h = round(im.height * w / im.width)
        im = im.resize((w, h), Image.LANCZOS)
        total += save_webp(im, os.path.join(SHOT_DIR, f'{slug}-{i:02d}.webp'), 80)

# 상세 페이지 배경 아트 (스토어 그래픽 1024x500)
for name in ('guimoon_feature', 'challenger18_feature'):
    src = os.path.join(LOCAL, f'{name}.png')
    if os.path.exists(src):
        im = Image.open(src).convert('RGB')
        total += save_webp(im, os.path.join(ART_DIR, name.replace('_', '-') + '.webp'), 82)

print('done, total', total, 'KB')
