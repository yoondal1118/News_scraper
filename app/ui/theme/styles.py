"""앱 전반에 사용하는 기본 스타일 모듈.

화이트/블랙 기반의 심플한 UI와 블루 포인트 색상을 정의한다.
"""

# 심플 라이트 테마 CSS (화이트/블랙 + 블루 포인트)
GLASSMORPHISM_CSS = """
<style>
html, body, [data-testid="stAppViewContainer"] {
    font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    background-color: #ffffff;
    color: #111827;
}

/* 상단 헤더 및 컨테이너 너비 제한 (반응형 대응) */
[data-testid="stAppViewBlockContainer"] {
    max-width: 800px;
    margin: 0 auto;
    padding-left: 1rem;
    padding-right: 1rem;
}

[data-testid="stAppViewContainer"] {
    padding-top: 1rem;
}

/* 기본 카드 */
.glass-card {
    background: #ffffff;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
}

.glass-card:hover {
    border-color: #2563eb;
}

/* 페이지 설명 영역 */
.info-section {
    background: #f9fafb;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 1.25rem;
    border-left: 4px solid #2563eb;
    font-size: 0.93rem;
}

/* 강조 텍스트 */
.neon-text {
    color: #2563eb;
    font-weight: 600;
}

/* 버튼 공통 스타일 (테두리 제거, hover 시만 살짝 강조)
    Streamlit의 기본 버튼 구조를 넓게 커버하기 위해 data-testid / kind / stButton 클래스를 모두 지정 */
button,
button[data-testid^="baseButton-"],
div.stButton > button {
    border-radius: 8px !important;
    border: none !important;
    box-shadow: none !important;
    background: #ffffff !important;
    color: #111827 !important;
    font-size: 0.9rem !important;
    padding: 0.35rem 0.8rem !important;
}

button:hover,
button[data-testid^="baseButton-"]:hover,
div.stButton > button:hover {
    border: none !important;
    box-shadow: 0 0 0 1px #2563eb inset !important;
    color: #2563eb !important;
}

button[data-testid="baseButton-primary"],
div.stButton > button[kind="primary"] {
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: none !important;
}

/* 캘린더 전용: 일자 버튼을 작은 네모 그리드처럼 보이게 */
.calendar-cell {
    font-size: 0.8rem;
    text-align: center;
}

/* 모바일 대응 반응형 캘린더 강제 가로 정렬 및 배열 최적화 */
@media screen and (max-width: 768px) {
    /* 사이드바 및 불필요한 공백 제거 */
    [data-testid="stAppViewContainer"] {
        padding-left: 0.1rem !important;
        padding-right: 0.1rem !important;
        padding-top: 0.5rem !important;
    }

    /* st.columns가 세로로 쌓이는 것을 강제로 막고 가로 7분할 유지 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
    }

    [data-testid="column"] {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        width: auto !important;
    }

    /* 달력 내부 버튼 텍스트 더욱 축소 및 줄바꿈 최적화 */
    div.stButton > button {
        font-size: 0.65rem !important;
        padding: 0 !important;
        min-height: 42px !important;
        max-height: 48px !important;
        line-height: 1.1 !important;
        white-space: pre-wrap !important;
    }
}

/* 캘린더 버튼 내 이모지 및 텍스트 마진 제거 */
div.stButton > button p {
    margin: 0 !important;
}
</style>
"""


def get_glassmorphism_css() -> str:
    """Glassmorphism CSS 스타일을 반환한다."""
    return GLASSMORPHISM_CSS


def get_category_colors() -> dict[str, str]:
    """카테고리별 색상 매핑을 반환한다."""
    return {
        "정치": "rgba(244, 67, 54, 0.3)",
        "경제": "rgba(76, 175, 80, 0.3)",
        "사회": "rgba(33, 150, 243, 0.3)",
        "생활/문화": "rgba(156, 39, 176, 0.3)",
        "IT/과학": "rgba(0, 188, 212, 0.3)",
        "세계": "rgba(255, 152, 0, 0.3)",
    }
