"""네이버 뉴스 스크래퍼 모듈.

Playwright를 사용하여 네이버 뉴스 6개 카테고리의 기사를 수집한다.
subprocess를 사용하여 Windows Streamlit 호환성을 보장한다.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


class ScraperError(Exception):
    """스크래퍼 관련 예외."""
    pass


# 기사 스키마 정의
ARTICLE_SCHEMA = {
    "id": str,
    "title": str,
    "url": str,
    "category": str,
    "collected_at": str,
    "source": str,
}

# 6개 카테고리와 네이버 뉴스 URL 매핑
CATEGORIES = {
    "정치": "https://news.naver.com/section/100",
    "경제": "https://news.naver.com/section/101",
    "사회": "https://news.naver.com/section/102",
    "생활/문화": "https://news.naver.com/section/103",
    "IT/과학": "https://news.naver.com/section/105",
    "세계": "https://news.naver.com/section/104",
}

# 뉴스 기사 선택자
SELECTORS = {
    "article_list": "ul.sa_list li.sa_item",
    "article_title": "a.sa_text_title",
    "article_link": "a.sa_text_title",
}


def generate_article_id(category: str) -> str:
    """고유 기사 ID를 생성한다."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"news_{category}_{timestamp}"


def parse_articles(html_content: str, category: str) -> list[dict[str, Any]]:
    """HTML에서 기사 정보를 파싱한다.
    
    Args:
        html_content: 페이지 HTML 내용
        category: 뉴스 카테고리
        
    Returns:
        파싱된 기사 리스트 (빈 HTML이면 빈 리스트)
    """
    if not html_content or not html_content.strip():
        return []
    
    # 실제 파싱은 Playwright 페이지 객체에서 수행
    # 이 함수는 빈 HTML 체크를 위한 유틸리티
    return []


def scrape_category(category: str) -> list[dict[str, Any]]:
    """특정 카테고리의 뉴스를 수집한다.
    
    별도 Python 프로세스에서 Playwright를 실행하여 Windows 호환성을 보장한다.
    Streamlit Cloud 환경에서는 브라우저 자동 설치를 시도한다.
    
    Args:
        category: 수집할 카테고리 (정치, 경제, 사회, 생활/문화, IT/과학, 세계)
        
    Returns:
        수집된 기사 리스트
        
    Raises:
        ScraperError: 수집 실패 시
        ValueError: 잘못된 카테고리
    """
    if category not in CATEGORIES:
        raise ValueError(f"지원하지 않는 카테고리: {category}")

    # Streamlit Cloud 환경 등을 위한 브라우저 설치 확인 및 실행
    try:
        import playwright
        # 브라우저가 없는 경우 설치 시도
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)
    except ImportError:
        pass
    
    # 별도 프로세스에서 실행할 스크립트
    script = '''
import json
from datetime import datetime
from playwright.sync_api import sync_playwright

category = {category!r}
url = {url!r}
selectors = {selectors!r}

articles = []

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        
        article_elements = page.query_selector_all(selectors["article_list"])
        collected_at = datetime.now().isoformat()
        
        for i, element in enumerate(article_elements[:20]):
            try:
                title_element = element.query_selector(selectors["article_title"])
                if not title_element:
                    continue
                
                title = title_element.inner_text()
                link = title_element.get_attribute("href")
                
                if not title or not link:
                    continue
                
                if link.startswith("/"):
                    link = f"https://news.naver.com{{link}}"
                
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                article = {{
                    "id": f"news_{{category}}_{{timestamp}}_{{i}}",
                    "title": title.strip(),
                    "url": link,
                    "category": category,
                    "collected_at": collected_at,
                    "source": "naver",
                }}
                articles.append(article)
            except Exception:
                continue
        
        browser.close()
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
else:
    print(json.dumps({{"articles": articles}}))
'''.format(
        category=category,
        url=CATEGORIES[category],
        selectors=SELECTORS,
    )
    
    try:
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=60,
        )
        
        if result.returncode != 0:
            raise ScraperError(f"스크래퍼 프로세스 오류: {result.stderr}")
        
        output = result.stdout.strip()
        if not output:
            return []
        
        data = json.loads(output)
        
        if "error" in data:
            raise ScraperError(f"뉴스 수집 실패 ({category}): {data['error']}")
        
        return data.get("articles", [])
        
    except subprocess.TimeoutExpired:
        raise ScraperError(f"뉴스 수집 시간 초과 ({category})")
    except json.JSONDecodeError as e:
        raise ScraperError(f"응답 파싱 실패 ({category}): {e}")


def scrape_all_categories(
    categories: list[str] | None = None
) -> dict[str, list[dict[str, Any]]]:
    """여러 카테고리의 뉴스를 수집한다.
    
    Args:
        categories: 수집할 카테고리 리스트 (None이면 전체)
        
    Returns:
        카테고리별 기사 딕셔너리
    """
    if categories is None:
        categories = list(CATEGORIES.keys())
    
    result = {}
    for category in categories:
        try:
            articles = scrape_category(category)
            result[category] = articles
        except ScraperError as e:
            result[category] = []
            # 로깅 등 추가 처리 가능
    
    return result
