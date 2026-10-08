# -*- coding: utf-8 -*-
"""
NeoMax 웹사이트 정적 페이지 생성기.

  python tools/build.py

생성물: index.html, apps/<slug>/index.html, privacy/index.html, 404.html
앱 문구·상태는 tools/apps_data.py 에서 고친다.
사이트 주소가 바뀌면(예: 사용자 사이트 루트로 이전) SITE_URL, BASE_PATH 만 고쳐서 다시 실행한다.
"""
import os, sys, json
from html import escape
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apps_data import APPS, SUPPORT_EMAIL, PLAY_DEV_URL, PLAY_URL, STATUS_LABEL  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = 'https://devk770319-ui.github.io/neomax'   # 끝에 / 없음
BASE_PATH = '/neomax/'                                 # 404 페이지용
VER = '20261009'
YEAR = '2026'
POLICIES_URL = 'https://devk770319-ui.github.io/neomax-policies/'

APP = {a['slug']: a for a in APPS}
LIVE = [a for a in APPS if a['status'] == 'live']
UPCOMING = [a for a in APPS if a['status'] != 'live']

# ---------------------------------------------------------------- icons (lucide 스타일, ISC)
ICONS = {
    'arrow': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    'arrow-left': '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
    'chev-left': '<path d="m15 18-6-6 6-6"/>',
    'chev-right': '<path d="m9 18 6-6-6-6"/>',
    'external': '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'check-circle': '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    'mail': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    'copy': '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    'bell': '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    'x': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    'hand': '<path d="M18 11V6a2 2 0 0 0-4 0v5"/><path d="M14 10V4a2 2 0 0 0-4 0v6"/><path d="M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>',
    'weight': '<circle cx="12" cy="5" r="3"/><path d="M6.5 8a2 2 0 0 0-1.905 1.46L2.1 18.5A2 2 0 0 0 4 21h16a2 2 0 0 0 1.925-2.54L19.4 9.5A2 2 0 0 0 17.48 8Z"/>',
    'layers': '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    'timer': '<line x1="10" x2="14" y1="2" y2="2"/><line x1="12" x2="15" y1="14" y2="11"/><circle cx="12" cy="14" r="8"/>',
    'star': '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>',
    'gift': '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/>',
    'shield': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    'pen': '<path d="M12 20h9"/><path d="M16.376 3.622a1 1 0 0 1 3.002 3.002L7.368 18.635a2 2 0 0 1-.855.506l-2.872.838a.5.5 0 0 1-.62-.62l.838-2.872a2 2 0 0 1 .506-.854z"/>',
    'lock': '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    'chart': '<path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="m19 9-5 5-4-4-3 3"/>',
    'calendar': '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/>',
    'rotate': '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>',
    'flag': '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" x2="4" y1="22" y2="15"/>',
    'wind': '<path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    'target': '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    'trophy': '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
    'zap': '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    'sparkles': '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/>',
    'map': '<path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/>',
    'droplet': '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    'book': '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/>',
    'wifioff': '<path d="M12 20h.01"/><path d="M8.5 16.429a5 5 0 0 1 7 0"/><path d="M5 12.859a10 10 0 0 1 5.17-2.69"/><path d="M19 12.859a10 10 0 0 0-2.007-1.523"/><path d="M2 8.82a15 15 0 0 1 4.177-2.643"/><path d="M22 8.82a15 15 0 0 0-11.288-3.764"/><path d="m2 2 20 20"/>',
    'receipt': '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 17.5v-11"/>',
    'file': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m9 15 2 2 4-4"/>',
    'clipboard': '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>',
    'swords': '<polyline points="14.5 17.5 3 6 3 3 6 3 17.5 14.5"/><line x1="13" x2="19" y1="19" y2="13"/><line x1="16" x2="20" y1="16" y2="20"/><line x1="19" x2="21" y1="21" y2="19"/><polyline points="14.5 6.5 18 3 21 3 21 6 17.5 9.5"/><line x1="5" x2="9" y1="14" y2="18"/><line x1="7" x2="4" y1="17" y2="20"/><line x1="3" x2="5" y1="19" y2="21"/>',
    'ghost': '<path d="M9 10h.01"/><path d="M15 10h.01"/><path d="M12 2a8 8 0 0 0-8 8v12l3-3 2.5 2.5L12 19l2.5 2.5L17 19l3 3V10a8 8 0 0 0-8-8z"/>',
    'scroll': '<path d="M15 12h-5"/><path d="M15 8h-5"/><path d="M19 17V5a2 2 0 0 0-2-2H4"/><path d="M8 21h12a2 2 0 0 0 2-2v-1a1 1 0 0 0-1-1H11a1 1 0 0 0-1 1v1a2 2 0 1 1-4 0V5a2 2 0 1 0-4 0v2a1 1 0 0 0 1 1h3"/>',
    'mountain': '<path d="m8 3 4 8 5-5 5 15H2L8 3z"/>',
    'smartphone': '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
    'heart': '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    'info': '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
}


def icon(name, cls=''):
    c = f' class="{cls}"' if cls else ''
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def rgba(hexcolor, a):
    h = hexcolor.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r}, {g}, {b}, {a})'


def app_vars(a, s1=.30, s2=.20):
    return (f'--g1:{rgba(a["c1"], s1)};--g2:{rgba(a["c2"], s2)};--tint:{a["tint"]};'
            f'--g3:{rgba(a["tint"], .10)};--g4:{rgba(a["tint"], .22)}')


# ---------------------------------------------------------------- images
_size_cache = {}


def img_size(rel):
    if rel not in _size_cache:
        p = os.path.join(ROOT, rel.replace('/', os.sep))
        with Image.open(p) as im:
            _size_cache[rel] = im.size
    return _size_cache[rel]


def icon_src(a, rp):
    ext = a.get('icon_ext', 'webp')
    return f'{rp}assets/img/icons/{a["slug"]}.{ext}'


def app_icon(a, rp, cls='app-icon', size=256, lazy=True):
    ld = ' loading="lazy"' if lazy else ''
    return (f'<img class="{cls}" src="{icon_src(a, rp)}" alt="{escape(a["name"])} 아이콘" '
            f'width="{size}" height="{size}"{ld} decoding="async">')


def shot_rel(a, n):
    return f'assets/img/shots/{a["slug"]}-{n:02d}.webp'


def phone(a, n, rp, cls='', lazy=True, alt=None):
    rel = shot_rel(a, n)
    w, h = img_size(rel)
    ld = ' loading="lazy"' if lazy else ''
    alt = alt or f'{a["name"]} 스크린샷 {n}'
    c = f'phone {cls}'.strip()
    return (f'<div class="{c}"><img src="{rp}{rel}" alt="{escape(alt)}" width="{w}" height="{h}"'
            f'{ld} decoding="async"></div>')


def status_tag(a):
    return f'<span class="tag status {a["status"]}">{STATUS_LABEL[a["status"]]}</span>'


def play_badge(a, rp):
    url = PLAY_URL.format(pkg=a['pkg'])
    return (f'<a class="play-badge" href="{url}" target="_blank" rel="noopener" '
            f'aria-label="Google Play에서 {escape(a["name"])} 다운로드">'
            f'<img src="{rp}assets/img/brand/google-play-badge-ko.png" alt="Google Play에서 다운로드" width="646" height="192"></a>')


def notify_mail(a):
    from urllib.parse import quote
    subj = quote(f'[{a["name"]}] 출시 알림 신청')
    body = quote(f'{a["name"]} 출시 소식을 받고 싶어요.\n')
    return f'mailto:{SUPPORT_EMAIL}?subject={subj}&body={body}'


# ---------------------------------------------------------------- layout
def head(title, desc, rp, path='', og_img='assets/img/brand/og.png', extra=''):
    url = f'{SITE_URL}/{path}'
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="theme-color" content="#06070a">
<link rel="canonical" href="{url}">
<link rel="icon" href="{rp}assets/img/brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rp}assets/img/brand/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="NeoMax">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/{og_img}">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="{rp}assets/css/style.css?v={VER}">
<script>document.documentElement.classList.add('js')</script>
{extra}</head>
'''


def header(rp):
    home = rp or './'
    return f'''<header class="site-header">
  <div class="container nav">
    <a class="brand" href="{home}" aria-label="NeoMax 홈">
      <img src="{rp}assets/img/brand/favicon.svg" alt="" width="30" height="30">NeoMax
    </a>
    <nav class="nav-links" aria-label="주요 메뉴">
      <a href="{rp}#apps">앱</a>
      <a href="{rp}#upcoming">개발 중</a>
      <a href="{rp}#studio">스튜디오</a>
      <a href="{rp}#contact">문의</a>
    </nav>
    <div class="nav-right">
      <a class="btn btn-ghost btn-sm" href="{PLAY_DEV_URL}" target="_blank" rel="noopener">Google Play {icon('external')}</a>
      <button class="menu-btn" type="button" aria-label="메뉴 열기" aria-expanded="false"><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-menu">
  <a href="{rp}#apps">앱</a>
  <a href="{rp}#upcoming">개발 중</a>
  <a href="{rp}#studio">스튜디오</a>
  <a href="{rp}#contact">문의</a>
  <a class="btn btn-primary" href="{PLAY_DEV_URL}" target="_blank" rel="noopener">Google Play에서 보기 {icon('external')}</a>
</div>
'''


def footer(rp):
    live = '\n'.join(f'<li><a href="{rp}apps/{a["slug"]}/">{a["name"]}</a></li>' for a in LIVE)
    up = '\n'.join(f'<li><a href="{rp}apps/{a["slug"]}/">{a["name"]}</a></li>' for a in UPCOMING)
    home = rp or './'
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{home}"><img src="{rp}assets/img/brand/favicon.svg" alt="" width="30" height="30">NeoMax</a>
        <p class="about">한 손으로 가볍게 즐기는 모바일 게임과, 매일을 조용히 돕는 앱을 만드는 작은 스튜디오입니다.</p>
      </div>
      <div>
        <h4>출시된 앱</h4>
        <ul>{live}</ul>
      </div>
      <div>
        <h4>개발 중</h4>
        <ul>{up}</ul>
      </div>
      <div>
        <h4>지원</h4>
        <ul>
          <li><a href="mailto:{SUPPORT_EMAIL}">문의하기</a></li>
          <li><a href="{rp}privacy/">개인정보처리방침</a></li>
          <li><a href="{PLAY_DEV_URL}" target="_blank" rel="noopener">Google Play 개발자 페이지</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>{YEAR}</span> NeoMax. All rights reserved.</span>
      <span>Google Play 및 Google Play 로고는 Google LLC의 상표입니다.</span>
    </div>
  </div>
</footer>
<script src="{rp}assets/js/main.js?v={VER}" defer></script>
</body>
</html>
'''


def write(rel, html):
    p = os.path.join(ROOT, rel.replace('/', os.sep))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('wrote', rel, len(html) // 1024, 'KB')


# ---------------------------------------------------------------- home
def build_home():
    rp = ''
    ld = {
        '@context': 'https://schema.org', '@type': 'Organization', 'name': 'NeoMax',
        'url': SITE_URL + '/', 'email': SUPPORT_EMAIL,
        'logo': SITE_URL + '/assets/img/brand/apple-touch-icon.png',
        'sameAs': [PLAY_DEV_URL],
    }
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    out = [head('NeoMax — 손끝에서 시작되는 작고 단단한 재미',
                'NeoMax는 한 손으로 가볍게 즐기는 모바일 게임과 매일을 조용히 돕는 앱을 만드는 작은 스튜디오입니다. 트럭러시, 하루칸, 골프러쉬를 Google Play에서 만나보세요.',
                rp, '', extra=extra)]
    out.append('<body>\n' + header(rp))

    tr, hk, gr = APP['truckrush'], APP['harukan'], APP['golfrush']
    gm, yb, ch, ic = APP['guimoon'], APP['yobung'], APP['challenger18'], APP['icare']

    # HERO
    out.append(f'''<main>
<section class="hero" id="top">
  <div class="hero-bg" aria-hidden="true"><div class="grid"></div><div class="glow g1"></div><div class="glow g2"></div><div class="glow g3"></div></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <span class="pill reveal"><span class="dot"></span>지금 Google Play에서 {len(LIVE)}개 앱 서비스 중</span>
      <h1 class="reveal" data-d="1">손끝에서 시작되는<br><span class="grad-text">작고 단단한 재미.</span></h1>
      <p class="lead reveal" data-d="2">NeoMax는 한 손으로 가볍게 즐기는 모바일 게임과, 매일을 조용히 돕는 앱을 만드는 작은 스튜디오입니다. 기획부터 아트, 개발, 운영까지 직접 다듬습니다.</p>
      <div class="hero-actions reveal" data-d="3">
        <a class="btn btn-primary" href="#apps">앱 둘러보기 {icon('arrow', 'arrow')}</a>
        <a class="btn btn-ghost" href="#upcoming">개발 중인 프로젝트</a>
      </div>
      <div class="hero-stats reveal" data-d="4">
        <div class="stat"><b>{len(APPS)}</b><span>프로젝트</span></div>
        <div class="stat"><b>{len(LIVE)}</b><span>Google Play 출시</span></div>
        <div class="stat"><b>{len(UPCOMING)}</b><span>개발 · 테스트 중</span></div>
      </div>
    </div>
    <div class="hero-visual reveal" data-d="2" data-parallax aria-hidden="true">
      <div class="layer l-left">{phone(tr, 1, rp, lazy=False)}</div>
      <div class="layer l-right">{phone(hk, 1, rp, lazy=False)}</div>
      <div class="layer l-center">{phone(gr, 1, rp, lazy=False)}</div>
      <img class="float-icon f1" src="{icon_src(gm, rp)}" alt="" width="68" height="68">
      <img class="float-icon f2" src="{icon_src(yb, rp)}" alt="" width="60" height="60">
      <img class="float-icon f3" src="{icon_src(ch, rp)}" alt="" width="54" height="54">
      <img class="float-icon f4" src="{icon_src(ic, rp)}" alt="" width="52" height="52">
    </div>
  </div>
</section>
''')

    # MARQUEE
    items = ''.join(
        f'<div class="marquee-item">{app_icon(a, rp, size=42)}<div>{a["name"]}<small>{a["en"]} · {a["genre"]}</small></div></div>'
        for a in APPS)
    out.append(f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{items}{items}</div></div>\n')

    # LIVE APPS
    out.append(f'''
<section class="section" id="apps">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Available now</span>
      <h2 class="title">지금 바로<br>만나보세요.</h2>
      <p>Google Play에서 서비스 중인 NeoMax의 앱입니다. 모두 무료로 시작할 수 있어요.</p>
    </div>
''')
    for i, a in enumerate(LIVE):
        rev = ' reverse' if i % 2 else ''
        checks = ''.join(f'<li>{icon("check-circle")}<span>{escape(c)}</span></li>' for c in a['checks'])
        tags = ''.join(f'<span class="tag">{t}</span>' for t in a['tags'][:2])
        out.append(f'''    <article class="showcase{rev} reveal" style="{app_vars(a)}">
      <div class="showcase-copy">
        <div class="app-id">
          {app_icon(a, rp, size=76)}
          <div><h3>{a["name"]}</h3><div class="sub">{a["en"]} {tags}</div></div>
        </div>
        <h4 class="tagline">{a["tagline"]}</h4>
        <p class="desc">{escape(a["lead"])}</p>
        <ul class="checks">{checks}</ul>
        <div class="cta-row">
          {play_badge(a, rp)}
          <a class="link-more" href="apps/{a["slug"]}/">자세히 보기 {icon('arrow')}</a>
        </div>
      </div>
      <div class="showcase-visual" aria-hidden="true">
        {phone(a, a["home_b"], rp, "pb")}
        {phone(a, a["home_a"], rp, "pa")}
      </div>
    </article>
''')
    out.append('  </div>\n</section>\n')

    # UPCOMING
    out.append(f'''
<section class="section" id="upcoming" style="padding-top:0">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">In development</span>
      <h2 class="title">곧 만나게 될<br>다음 이야기.</h2>
      <p>테스트와 다듬기를 거치고 있는 프로젝트입니다. 출시되면 이곳에서 가장 먼저 알려 드릴게요.</p>
    </div>
    <div class="upcoming-grid">
''')
    for i, a in enumerate(UPCOMING):
        if a['shots']:
            c1, c2, c3 = a['card']
            visual = (f'<div class="u-visual" aria-hidden="true">{phone(a, c2, rp, "ph2")}'
                      f'{phone(a, c3, rp, "ph3")}{phone(a, c1, rp, "ph1")}</div>')
        else:
            chips = [('calendar', '치료 일정'), ('receipt', '영수증 보관'), ('file', '보험 청구'), ('users', '가족 공유')]
            ch_html = ''.join(f'<span class="chip c{k + 1}">{icon(n)}{t}</span>' for k, (n, t) in enumerate(chips))
            visual = (f'<div class="u-visual icare-visual" aria-hidden="true"><span class="ring r3"></span>'
                      f'<span class="ring r2"></span><span class="ring r1"></span>'
                      f'{app_icon(a, rp, "app-icon big-icon", 118)}{ch_html}</div>')
        out.append(f'''      <article class="u-card reveal" data-d="{i % 2 + 1}" style="{app_vars(a, .34, .22)}">
        {visual}
        <div class="u-body">
          <div class="u-top">
            {app_icon(a, rp, size=58)}
            <div><h3>{a["name"]}</h3><div class="en">{a["en"]} · {a["genre"]}</div></div>
            {status_tag(a)}
          </div>
          <p>{escape(a["short"])}</p>
          <div class="u-foot"><span>Android · Google Play</span><span class="go">자세히 보기 {icon('arrow')}</span></div>
        </div>
        <a class="stretched" href="apps/{a["slug"]}/" aria-label="{escape(a["name"])} 자세히 보기"></a>
      </article>
''')
    out.append('    </div>\n  </div>\n</section>\n')

    # STUDIO
    principles = [
        ('hand', '배우는 데 3초', '쓸어 올리기, 밀기, 당겼다 놓기. 손가락 하나로 시작하고, 깊이는 플레이하면서 발견하도록 만듭니다.'),
        ('shield', '가입 없이, 기록은 내 기기에', '회원가입과 로그인 없이 바로 시작합니다. 일기와 진행 기록은 기본적으로 기기 안에만 남습니다.'),
        ('sparkles', '광고는 고를 수 있게', '보상형 광고는 직접 누를 때만 나옵니다. 플레이와 기록의 흐름을 끊는 광고는 최소한으로 둡니다.'),
        ('layers', '작게 만들고, 오래 다듬기', '테스트와 피드백을 거쳐 조금씩 자주 업데이트합니다. 출시는 끝이 아니라 시작이라고 생각합니다.'),
    ]
    cards = ''.join(f'''<div class="p-card reveal" data-d="{k + 1}"><div class="ico">{icon(n)}</div><h3>{t}</h3><p>{b}</p></div>'''
                    for k, (n, t, b) in enumerate(principles))
    out.append(f'''
<section class="section" id="studio" style="padding-top:0">
  <div class="container">
    <div class="section-head reveal" style="max-width:none">
      <span class="eyebrow">Studio</span>
    </div>
    <p class="statement reveal"><em>작지만 허투루 만들지 않습니다.</em> 짧게 즐기고 오래 남는 게임, 매일 손이 가는 앱. NeoMax는 <em>쉬운 조작과 깊은 손맛</em>, 그리고 <em>사용자의 시간과 정보를 아끼는 설계</em>를 가장 중요하게 생각합니다.</p>
    <div class="principles">{cards}</div>
  </div>
</section>
''')

    # CONTACT
    out.append(f'''
<section class="section" id="contact" style="padding-top:0">
  <div class="container">
    <div class="contact-panel reveal">
      <div>
        <span class="eyebrow">Contact</span>
        <h2 class="title">이야기를<br>들려주세요.</h2>
        <p class="lead">버그 제보, 기능 제안, 제휴 문의 모두 환영합니다. 보내 주신 의견은 빠짐없이 읽고 다음 업데이트에 참고합니다.</p>
      </div>
      <div class="contact-box">
        <small>이메일</small>
        <a class="mail" href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>
        <div class="row">
          <a class="btn btn-primary" href="mailto:{SUPPORT_EMAIL}">{icon('mail')} 메일 보내기</a>
          <button class="btn btn-ghost" type="button" data-copy="{SUPPORT_EMAIL}">{icon('copy')} <span class="copy-label">주소 복사</span></button>
        </div>
        <div class="contact-links">
          <a href="privacy/">개인정보처리방침 {icon('arrow')}</a>
          <a href="{PLAY_DEV_URL}" target="_blank" rel="noopener">Google Play 개발자 페이지 {icon('external')}</a>
        </div>
      </div>
    </div>
  </div>
</section>
</main>
''')
    out.append(footer(rp))
    write('index.html', ''.join(out))


# ---------------------------------------------------------------- app page
STEP_LABEL = {'done': '완료', 'now': '진행 중', 'next': '예정'}


def build_app(a):
    rp = '../../'
    live = a['status'] == 'live'
    title = f'{a["name"]} ({a["en"]}) — NeoMax'
    desc = a['short'] + ('' if a['short'].endswith('.') else '.') + ' ' + a['lead']
    ld = {
        '@context': 'https://schema.org', '@type': 'SoftwareApplication',
        'name': a['name'], 'alternateName': a['en'], 'operatingSystem': 'ANDROID',
        'applicationCategory': 'LifestyleApplication' if a['slug'] in ('harukan', 'icare') else 'GameApplication',
        'description': a['short'],
        'author': {'@type': 'Organization', 'name': 'NeoMax'},
    }
    if live:
        ld['offers'] = {'@type': 'Offer', 'price': '0', 'priceCurrency': 'KRW'}
        ld['installUrl'] = PLAY_URL.format(pkg=a['pkg'])
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    out = [head(title, desc[:150], rp, f'apps/{a["slug"]}/', extra=extra)]
    out.append(f'<body style="{app_vars(a)}">\n' + header(rp))

    tags = ''.join(f'<span class="tag">{t}</span>' for t in a['tags'])
    if live:
        cta = (f'{play_badge(a, rp)}<a class="btn btn-ghost" href="#features">주요 기능 보기</a>')
    else:
        cta = (f'<a class="btn btn-primary" href="{notify_mail(a)}">{icon("bell")} 출시 소식 받기</a>'
               f'<a class="btn btn-ghost" href="{rp}#upcoming">다른 프로젝트 보기</a>')
    meta = ''.join(f'<div><small>{k}</small><b>{v}</b></div>' for k, v in a['meta'])

    if a['shots']:
        b = 2 if a['shots'] >= 2 else 1
        visual = (f'<div class="app-hero-visual reveal" data-d="2" aria-hidden="true">'
                  f'{phone(a, b, rp, "pb", lazy=False)}{phone(a, 1, rp, "pa", lazy=False)}</div>')
    else:
        chips = [('calendar', '치료 일정'), ('receipt', '영수증 보관'), ('file', '보험 청구'), ('users', '가족 공유')]
        ch_html = ''.join(f'<span class="chip c{k + 1}">{icon(n)}{t}</span>' for k, (n, t) in enumerate(chips))
        visual = (f'<div class="app-hero-visual icare-visual reveal" data-d="2" aria-hidden="true">'
                  f'<span class="ring r3"></span><span class="ring r2"></span><span class="ring r1"></span>'
                  f'{app_icon(a, rp, "app-icon big-icon", 118, lazy=False)}{ch_html}</div>')

    art = ''
    if a.get('art'):
        art = f'<div class="app-hero-art" style="background-image:url({rp}assets/img/art/{a["art"]})"></div>'

    out.append(f'''<main>
<section class="app-hero">
  <div class="app-hero-bg" aria-hidden="true"></div>{art}
  <div class="container">
    <nav class="breadcrumb" aria-label="위치"><a href="{rp}">NeoMax</a>{icon('chev-right')}<a href="{rp}{'#apps' if live else '#upcoming'}">{'앱' if live else '개발 중'}</a>{icon('chev-right')}<span>{a["name"]}</span></nav>
    <div class="app-hero-grid">
      <div>
        <div class="reveal">{app_icon(a, rp, size=116, lazy=False)}</div>
        <h1 class="reveal" data-d="1">{a["name"]}</h1>
        <p class="en reveal" data-d="1">{a["en"]} · {a["genre"]}</p>
        <div class="tags reveal" data-d="2">{status_tag(a)}{tags}</div>
        <p class="lead reveal" data-d="2">{escape(a["lead"])}</p>
        <div class="cta-row reveal" data-d="3">{cta}</div>
        <div class="meta-strip reveal" data-d="4">{meta}</div>
      </div>
      {visual}
    </div>
  </div>
</section>
''')

    # gallery
    if a['shots']:
        shots = ''.join(f'<button class="shot" type="button" aria-label="스크린샷 {n} 크게 보기">{phone(a, n, rp)}</button>'
                        for n in range(1, a['shots'] + 1))
        mid_cta = ''
        if live:
            mid_cta = (f'<a class="btn btn-ghost btn-sm" href="{PLAY_URL.format(pkg=a["pkg"])}" target="_blank" rel="noopener">'
                       f'Google Play에서 받기 {icon("external")}</a>')
        out.append(f'''
<section class="section" style="padding-top:40px">
  <div class="container">
    <div class="head-row reveal" style="margin-bottom:40px">
      <div class="section-head">
        <span class="eyebrow">Screenshots</span>
        <h2 class="title">{a["tagline"]}</h2>
      </div>
      <div class="gallery-nav" data-gallery-target="gal">{mid_cta}
        <button class="icon-btn" type="button" data-dir="prev" aria-label="이전">{icon('chev-left')}</button>
        <button class="icon-btn" type="button" data-dir="next" aria-label="다음">{icon('chev-right')}</button>
      </div>
    </div>
    <div class="gallery-wrap reveal" id="gal" data-gallery><div class="gallery">{shots}</div></div>
  </div>
</section>
''')

    # features
    feats = ''.join(f'<div class="f-card reveal" data-d="{k % 3 + 1}"><div class="ico">{icon(n)}</div><h3>{escape(t)}</h3><p>{escape(b)}</p></div>'
                    for k, (n, t, b) in enumerate(a['features']))
    out.append(f'''
<section class="section" id="features" style="padding-top:{'0' if a['shots'] else '40px'}">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Features</span>
      <h2 class="title">{'이런 점이 다릅니다.' if live else '이렇게 만들고 있어요.'}</h2>
    </div>
    <div class="features">{feats}</div>
  </div>
</section>
''')

    # notes / steps + info
    left = []
    if a.get('steps'):
        steps = ''.join(f'<li class="{s}"><span class="mark">{icon("check") if s == "done" else ""}</span><b>{t}</b><small>{STEP_LABEL[s]}</small></li>'
                        for t, s in a['steps'])
        left.append(f'''<div class="panel reveal"><h3>개발 현황</h3><ol class="steps">{steps}</ol>
          <p class="panel-foot">출시 일정이 정해지면 이 페이지와 Google Play에서 알려 드립니다.</p></div>''')
    if a.get('notes'):
        notes = ''.join(f'<li>{icon("info")}<span>{escape(n)}</span></li>' for n in a['notes'])
        left.append(f'<div class="panel reveal"><h3>{a["notes_title"]}</h3><ul class="note-list">{notes}</ul></div>')

    rows = [('개발사', 'NeoMax'), ('카테고리', a['genre'])]
    if live:
        rows.append(('최근 업데이트', a['updated']))
    else:
        rows.append(('진행 상태', STATUS_LABEL[a['status']]))
    rows += [('지원 기기', 'Android'),
             ('개인정보처리방침', f'<a href="{a["privacy"]}" target="_blank" rel="noopener">보기</a>'),
             ('문의', f'<a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>')]
    info = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    out.append(f'''
<section class="section" style="padding-top:0">
  <div class="container info-grid">
    <div class="stack">{''.join(left)}</div>
    <div class="panel reveal" data-d="1"><h3>앱 정보</h3><dl class="info-table">{info}</dl></div>
  </div>
</section>
''')

    # CTA band
    if live:
        band = (f'<div class="cta-band reveal"><div class="left">{app_icon(a, rp, size=84)}<div>'
                f'<h2>지금 {a["name"]}을(를) 시작해 보세요.</h2><p>Google Play에서 무료로 받을 수 있어요.</p></div></div>'
                f'{play_badge(a, rp)}</div>')
    else:
        band = (f'<div class="cta-band reveal"><div class="left">{app_icon(a, rp, size=84)}<div>'
                f'<h2>{a["name"]} 출시 소식을 받아 보세요.</h2><p>메일을 남겨 주시면 출시 소식을 알려 드릴게요.</p></div></div>'
                f'<a class="btn btn-primary" href="{notify_mail(a)}">{icon("bell")} 출시 알림 신청</a></div>')
    out.append(f'<section class="section" style="padding-top:0"><div class="container">{band}</div></section>\n')

    # other apps
    others = ''.join(f'<a class="o-card" href="{rp}apps/{o["slug"]}/">{app_icon(o, rp, size=68)}<b>{o["name"]}</b>{status_tag(o)}</a>'
                     for o in APPS if o['slug'] != a['slug'])
    out.append(f'''
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="section-head reveal" style="margin-bottom:36px">
      <span class="eyebrow">More from NeoMax</span>
      <h2 class="title" style="font-size:clamp(28px,3vw,40px)">NeoMax의 다른 앱</h2>
    </div>
    <div class="others reveal">{others}</div>
  </div>
</section>
</main>
''')
    if a['shots']:
        out.append(f'''<div class="lightbox" role="dialog" aria-modal="true" aria-label="스크린샷 보기">
  <button class="icon-btn lb-close" type="button" aria-label="닫기">{icon('x')}</button>
  <button class="icon-btn lb-prev" type="button" aria-label="이전">{icon('chev-left')}</button>
  <img src="" alt="">
  <button class="icon-btn lb-next" type="button" aria-label="다음">{icon('chev-right')}</button>
  <span class="lb-count"></span>
</div>
''')
    out.append(footer(rp))
    write(f'apps/{a["slug"]}/index.html', ''.join(out))


# ---------------------------------------------------------------- privacy index
def build_privacy():
    rp = '../'
    out = [head('개인정보처리방침 — NeoMax', 'NeoMax 앱별 개인정보처리방침 모음입니다.', rp, 'privacy/')]
    out.append('<body>\n' + header(rp))
    rows = ''.join(f'''<a class="pv-row reveal" href="{a["privacy"]}" target="_blank" rel="noopener">
      {app_icon(a, rp, size=52)}<div><b>{a["name"]}</b><small>{a["en"]} · {a["pkg"]}</small></div>{status_tag(a)}<span class="go">{icon('external')}</span></a>'''
                   for a in APPS)
    out.append(f'''<main>
<section class="app-hero" style="padding-bottom:40px">
  <div class="app-hero-bg" aria-hidden="true" style="--g1:rgba(124,136,255,.22);--g2:rgba(255,150,200,.12)"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="위치"><a href="{rp}">NeoMax</a>{icon('chev-right')}<span>개인정보처리방침</span></nav>
    <h1 class="reveal" style="font-size:clamp(38px,5vw,60px)">개인정보처리방침</h1>
    <p class="lead reveal" data-d="1" style="color:var(--text-2);margin-top:20px;max-width:640px;font-size:18px">NeoMax의 각 앱은 서비스에 꼭 필요한 정보만 다룹니다. 앱마다 처리하는 정보가 다르므로 아래에서 해당 앱의 방침을 확인해 주세요.</p>
  </div>
</section>
<section class="section" style="padding-top:20px">
  <div class="container"><div class="pv-list">{rows}</div>
  <p class="pv-foot reveal">개인정보 관련 문의: <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p></div>
</section>
</main>
''')
    out.append(footer(rp))
    write('privacy/index.html', ''.join(out))


# ---------------------------------------------------------------- 404
def build_404():
    rp = BASE_PATH
    out = [head('페이지를 찾을 수 없어요 — NeoMax', '요청하신 페이지를 찾을 수 없습니다.', rp, '404.html')]
    out.append('<body>\n' + header(rp))
    out.append(f'''<main class="notfound">
  <div>
    <div class="code grad-text">404</div>
    <p>찾으시는 페이지가 없거나 주소가 바뀌었어요.</p>
    <a class="btn btn-primary" href="{rp}">홈으로 가기 {icon('arrow', 'arrow')}</a>
  </div>
</main>
''')
    out.append(footer(rp))
    write('404.html', ''.join(out))


if __name__ == '__main__':
    build_home()
    for a in APPS:
        build_app(a)
    build_privacy()
    build_404()
    print('ok')
