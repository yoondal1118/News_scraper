"""네이버 뉴스 셀렉터 정의.

Playwright에서 사용할 CSS 셀렉터를 정의한다.
"""

# 네이버 뉴스 메인 셀렉터
MAIN_SELECTORS = {
    "article_list": "ul.sa_list li.sa_item",
    "article_title": "a.sa_text_title",
    "article_link": "a.sa_text_title",
    "article_summary": ".sa_text_lede",
    "article_press": ".sa_text_press",
}

# 카테고리별 추가 셀렉터 (필요시)
CATEGORY_SELECTORS = {
    "정치": {},
    "경제": {},
    "사회": {},
    "생활/문화": {},
    "IT/과학": {},
    "세계": {},
}


def get_selector(name: str) -> str:
    """셀렉터 이름으로 CSS 셀렉터를 반환한다."""
    return MAIN_SELECTORS.get(name, "")
