# 네이버 뉴스 스크래퍼 및 다이어리 앱

> Streamlit 기반 네이버 뉴스 수집 및 개인 다이어리 애플리케이션

## 주요 기능

- 📰 **뉴스 수집**: 네이버 6개 카테고리(정치/경제/사회/생활·문화/IT·과학/세계) 뉴스 수동 수집
- ⭐ **즐겨찾기**: 관심 있는 기사를 저장하고 관리
- 📅 **캘린더 관리**: Bento Grid 기반 캘린더에서 날짜별 이슈 CRUD
- 📝 **다이어리 작성**: 뉴스별 요약 및 의견 작성 (기사당 1개, 모달 팝업)
- 🗑️ **일괄 삭제**: 전체 기사 또는 카테고리별 삭제 (확인 모달)
- 🔗 **공유**: 작성한 내용을 클립보드로 복사

## 기술 스택

- **Language**: Python 3.11+
- **Web Framework**: Streamlit 1.34.0+
- **Web Scraping**: Playwright
- **Testing**: Pytest
- **UI Style**: Glassmorphism + Bento Grid (2026 트렌드)
- **Icons**: emoji 라이브러리

## 설치 및 실행

### 1. 환경 준비

```bash
# Python 3.12+ 확인
python --version

# 가상 환경 생성 및 활성화
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. Playwright 브라우저 설치

```bash
python -m playwright install chromium
```

### 4. 앱 실행

```bash
streamlit run app/main.py
```

브라우저에서 `http://localhost:8501`로 접속합니다.

## 사용 방법

### 상단 네비게이션

앱 상단에 3개의 네비게이션 버튼이 있습니다:
- **📰 뉴스 수집**: 뉴스 수집 및 목록 페이지
- **📅 캘린더**: 스마트 이슈 캘린더
- **⭐ 저장된 뉴스기사**: 즐겨찾기한 기사 및 다이어리

### 뉴스 수집

1. **뉴스 수집** 페이지에서 카테고리를 선택합니다.
2. **뉴스 수집** 버튼을 클릭합니다.
3. 수집된 뉴스가 블록 리스트로 표시됩니다.
4. 각 기사의 ☆ 버튼을 클릭하여 즐겨찾기에 추가합니다.

### 즐겨찾기 및 다이어리

1. **저장된 뉴스기사** 페이지에서 즐겨찾기한 기사를 확인합니다.
2. **다이어리** 버튼을 클릭하면 모달 팝업이 열립니다.
3. 요약과 의견을 작성하고 **저장** 버튼을 클릭합니다.

### 캘린더

1. **캘린더** 페이지에서 월/연도를 네비게이션합니다.
2. 뉴스가 있는 날짜에는 📰 배지가 표시됩니다.
3. 이슈가 있는 날짜에는 📝 배지가 표시됩니다.
4. 날짜를 클릭하여 이슈를 추가/수정/삭제합니다.

### 기사 삭제

1. **뉴스 수집** 페이지에서 **기사 삭제 옵션**을 펼칩니다.
2. **전체 삭제** 또는 **카테고리 삭제** 버튼을 클릭합니다.
3. 확인 모달에서 **확인**을 클릭하여 삭제합니다.

## 테스트 실행

```bash
pytest tests/ -v
```

## 프로젝트 구조

```
news_scraper/
├── app/
│   ├── main.py                # Streamlit 진입점 (상단 네비게이션)
│   ├── pages/
│   │   ├── home_page.py       # 뉴스 수집 페이지
│   │   ├── calendar_page_content.py  # 캘린더 페이지
│   │   └── favorites_page_content.py # 저장된 뉴스기사 페이지
│   ├── services/
│   │   ├── news_service.py    # 뉴스/즐겨찾기/삭제 서비스
│   │   ├── diary_service.py   # 다이어리 서비스
│   │   └── calendar_service.py# 캘린더 서비스
│   └── ui/
│       ├── components/        # UI 컴포넌트 (nav_bar.py 포함)
│       ├── layout/            # Bento Grid 레이아웃
│       └── theme/             # Glassmorphism 스타일
├── scraper/
│   └── naver_scraper.py       # Playwright 수집 로직
├── data/
│   ├── news_articles.json     # 뉴스 데이터 (is_favorite 필드 포함)
│   ├── diary_entries.json     # 다이어리 데이터
│   └── calendar_issues.json   # 캘린더 이슈 데이터
└── tests/
    ├── contract/              # 계약 테스트
    ├── integration/           # 통합 테스트
    └── unit/                  # 유닛 테스트
```

## 데이터 저장

모든 데이터는 `data/` 폴더에 JSON 형식으로 저장됩니다:

- `news_articles.json`: 수집된 뉴스 기사
- `diary_entries.json`: 다이어리 엔트리
- `calendar_issues.json`: 캘린더 이슈

## 라이선스

MIT License
