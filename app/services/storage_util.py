"""로컬 JSON 스토리지 유틸리티 모듈.

data/ 폴더의 JSON 파일을 읽고 쓰는 공통 기능을 제공한다.
"""

import json
from pathlib import Path
from typing import Any
from datetime import datetime


# 프로젝트 루트 기준 data 폴더 경로
DATA_DIR = Path(__file__).parent.parent.parent / "data"

# JSON 파일 경로
NEWS_ARTICLES_PATH = DATA_DIR / "news_articles.json"
DIARY_ENTRIES_PATH = DATA_DIR / "diary_entries.json"
CALENDAR_ISSUES_PATH = DATA_DIR / "calendar_issues.json"


def ensure_data_dir() -> None:
    """data 디렉토리가 존재하는지 확인하고 없으면 생성한다."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def read_json(file_path: Path) -> list[dict[str, Any]]:
    """JSON 파일을 읽어 리스트로 반환한다.
    
    Args:
        file_path: 읽을 JSON 파일 경로
        
    Returns:
        JSON 데이터 리스트 (파일이 없거나 비어있으면 빈 리스트)
    """
    ensure_data_dir()
    
    if not file_path.exists():
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def write_json(file_path: Path, data: list[dict[str, Any]]) -> bool:
    """데이터를 JSON 파일에 저장한다.
    
    Args:
        file_path: 저장할 JSON 파일 경로
        data: 저장할 데이터 리스트
        
    Returns:
        저장 성공 여부
    """
    ensure_data_dir()
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False


def generate_id(prefix: str = "") -> str:
    """고유 ID를 생성한다.
    
    Args:
        prefix: ID 접두사 (예: "news", "diary", "issue")
        
    Returns:
        타임스탬프 기반 고유 ID
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}_{timestamp}" if prefix else timestamp


def get_current_datetime() -> str:
    """현재 시각을 ISO 형식 문자열로 반환한다."""
    return datetime.now().isoformat()


def get_current_date() -> str:
    """현재 날짜를 YYYY-MM-DD 형식 문자열로 반환한다."""
    return datetime.now().strftime("%Y-%m-%d")


# 뉴스 기사 관련 함수
def load_news_articles() -> list[dict[str, Any]]:
    """뉴스 기사 목록을 로드한다."""
    return read_json(NEWS_ARTICLES_PATH)


def save_news_articles(articles: list[dict[str, Any]]) -> bool:
    """뉴스 기사 목록을 저장한다."""
    return write_json(NEWS_ARTICLES_PATH, articles)


# 다이어리 엔트리 관련 함수
def load_diary_entries() -> list[dict[str, Any]]:
    """다이어리 엔트리 목록을 로드한다."""
    return read_json(DIARY_ENTRIES_PATH)


def save_diary_entries(entries: list[dict[str, Any]]) -> bool:
    """다이어리 엔트리 목록을 저장한다."""
    return write_json(DIARY_ENTRIES_PATH, entries)


# 캘린더 이슈 관련 함수
def load_calendar_issues() -> list[dict[str, Any]]:
    """캘린더 이슈 목록을 로드한다."""
    return read_json(CALENDAR_ISSUES_PATH)


def save_calendar_issues(issues: list[dict[str, Any]]) -> bool:
    """캘린더 이슈 목록을 저장한다."""
    return write_json(CALENDAR_ISSUES_PATH, issues)


# ──────────────────────────────────────────────────────────────────
# 즐겨찾기 및 다이어리 연동 관련 함수 (002 기능)
# ──────────────────────────────────────────────────────────────────

def read_json_dict(file_path: Path) -> dict[str, Any]:
    """JSON 파일을 읽어 딕셔너리로 반환한다.
    
    Args:
        file_path: 읽을 JSON 파일 경로
        
    Returns:
        JSON 데이터 딕셔너리 (파일이 없거나 비어있으면 빈 딕셔너리)
    """
    ensure_data_dir()
    
    if not file_path.exists():
        return {}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, IOError):
        return {}


def write_json_dict(file_path: Path, data: dict[str, Any]) -> bool:
    """딕셔너리 데이터를 JSON 파일에 저장한다.
    
    Args:
        file_path: 저장할 JSON 파일 경로
        data: 저장할 딕셔너리 데이터
        
    Returns:
        저장 성공 여부
    """
    ensure_data_dir()
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False


def load_diary_entries_dict() -> dict[str, dict[str, Any]]:
    """다이어리 엔트리를 딕셔너리(key: article_id) 형태로 로드한다."""
    return read_json_dict(DIARY_ENTRIES_PATH)


def save_diary_entries_dict(entries: dict[str, dict[str, Any]]) -> bool:
    """다이어리 엔트리를 딕셔너리 형태로 저장한다."""
    return write_json_dict(DIARY_ENTRIES_PATH, entries)


def get_article_by_id(article_id: str) -> dict[str, Any] | None:
    """ID로 특정 뉴스 기사를 조회한다.
    
    Args:
        article_id: 조회할 기사 ID
        
    Returns:
        기사 딕셔너리 또는 None
    """
    articles = load_news_articles()
    for article in articles:
        if article.get("id") == article_id:
            return article
    return None


def delete_diary_entry_by_article_id(article_id: str) -> bool:
    """특정 기사 ID에 해당하는 다이어리 엔트리를 삭제한다.
    
    Args:
        article_id: 삭제할 기사 ID
        
    Returns:
        삭제 성공 여부
    """
    entries = load_diary_entries_dict()
    if article_id in entries:
        del entries[article_id]
        return save_diary_entries_dict(entries)
    return True  # 없어도 성공으로 간주

