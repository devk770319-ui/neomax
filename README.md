# NeoMax 웹사이트

NeoMax가 개발·서비스하는 앱을 소개하는 정적 웹사이트입니다. GitHub Pages로 배포합니다.

- 저장소: https://github.com/devk770319-ui/neomax
- 주소: https://devk770319-ui.github.io/neomax/

## 구성

```
index.html                  홈 (출시 앱 · 개발 중 · 스튜디오 · 문의)
apps/<slug>/index.html      앱 상세 7개 (truckrush, harukan, golfrush, yobung, guimoon, challenger18, icare)
privacy/index.html          앱별 개인정보처리방침 모음
404.html
assets/css/style.css        전체 스타일
assets/js/main.js           메뉴 · 스크롤 등장 효과 · 스크린샷 갤러리 · 라이트박스
assets/img/icons|shots|art|brand
tools/apps_data.py          앱 문구 · 상태 · 색상 데이터  ← 내용 수정은 여기서
tools/build.py              HTML 생성기
tools/process_images.py     Play 스토어 원본 PNG → WebP 변환
tools/make_brand.py         og.png(공유 이미지), apple-touch-icon.png 생성
```

HTML은 직접 고치지 말고 `tools/apps_data.py` 또는 `tools/build.py`를 고친 뒤 다시 생성합니다.

```powershell
cd D:\05.site\04.neomax-site
python tools\build.py
git add -A; git commit -m "update"; git push
```

## 자주 하는 작업

- **앱이 출시됐을 때**: `tools/apps_data.py`에서 해당 앱의 `status`를 `'live'`로 바꾸고,
  `checks`, `notes_title`, `notes`, `updated`, `home_a`, `home_b`를 채운 뒤 빌드합니다.
- **스크린샷 교체**: Play 스토어 원본을 `<slug>_shotNN.png`로 받아 `tools/process_images.py`의 순서표를 고치고 실행합니다.
- **사용자 사이트 루트(https://devk770319-ui.github.io/)로 옮길 때**: `tools/build.py`의 `SITE_URL`, `BASE_PATH`만 바꿔 다시 빌드합니다.
  페이지 안의 링크는 모두 상대경로라 그대로 동작합니다. 루트 저장소의 `app-ads.txt`는 반드시 유지해야 합니다(AdMob 인증용).

## 메모

- 글꼴: Pretendard (jsDelivr CDN)
- Google Play 배지는 Google 공식 배지 이미지를 사용하고, 푸터에 상표 고지를 넣었습니다.
- 앱 소개 문구는 각 앱의 Google Play 등록정보(2026-10-08 기준)를 바탕으로 작성했습니다.
