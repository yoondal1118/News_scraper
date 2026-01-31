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

/* 즐겨찾기 전용 버튼은 완전 투명하게 (보더/배경 제거) */
button[title="즐겨찾기 토글"],
button[title="즐겨찾기 해제"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.1rem 0.3rem !important;
}

/* 접근성: 텍스트 대비 확보 */
.high-contrast-text {
    color: #111827;
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
