"""뉴스 서비스 모듈.

뉴스 데이터의 수집, 저장, 조회, 중복 제거를 담당한다.
"""

from datetime import datetime
from typing import Any

from app.services.storage_util import (
    load_news_articles,
    save_news_articles,
    generate_id,
    get_current_datetime,
    load_diary_entries_dict,
    save_diary_entries_dict,
)


class NewsService:
    """뉴스 데이터 관리 서비스."""

    def __init__(self) -> None:
        """뉴스 서비스를 초기화한다."""
        self._articles: list[dict[str, Any]] | None = None

    def load_articles(self) -> list[dict[str, Any]]:
        """저장된 뉴스 기사를 로드한다.
        
        Returns:
            기사 리스트
        """
        self._articles = load_news_articles()
        return self._articles

    def save_articles(self, articles: list[dict[str, Any]]) -> bool:
        """뉴스 기사를 저장한다.
        
        Args:
            articles: 저장할 기사 리스트
            
        Returns:
            저장 성공 여부
        """
        self._articles = articles
        return save_news_articles(articles)

    def remove_duplicates(
        self, articles: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """제목+카테고리 기준으로 중복 기사를 제거한다.
        
        Args:
            articles: 기사 리스트
            
        Returns:
            중복 제거된 기사 리스트
        """
        seen = set()
        unique_articles = []
        
        for article in articles:
            key = (article["title"], article["category"])
            if key not in seen:
                seen.add(key)
                unique_articles.append(article)
        
        return unique_articles

    def merge_articles(
        self,
        existing: list[dict[str, Any]],
        new_articles: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """기존 기사와 새 기사를 병합하고 중복을 제거한다.
        
        Args:
            existing: 기존 기사 리스트
            new_articles: 새로 수집된 기사 리스트
            
        Returns:
            병합 및 중복 제거된 기사 리스트
        """
        # 기존 기사의 key 집합 생성
        existing_keys = {
            (article["title"], article["category"]) for article in existing
        }
        
        # 새 기사 중 중복되지 않는 것만 추가
        merged = existing.copy()
        for article in new_articles:
            key = (article["title"], article["category"])
            if key not in existing_keys:
                merged.append(article)
                existing_keys.add(key)
        
        return merged

    def filter_by_category(
        self, category: str
    ) -> list[dict[str, Any]]:
        """특정 카테고리의 기사만 필터링한다.
        
        Args:
            category: 필터링할 카테고리
            
        Returns:
            해당 카테고리의 기사 리스트
        """
        articles = self._articles or self.load_articles()
        return [a for a in articles if a.get("category") == category]

    def filter_by_date(
        self, date_str: str
    ) -> list[dict[str, Any]]:
        """특정 날짜의 기사만 필터링한다.
        
        Args:
            date_str: YYYY-MM-DD 형식의 날짜
            
        Returns:
            해당 날짜의 기사 리스트
        """
        articles = self._articles or self.load_articles()
        return [
            a for a in articles 
            if a.get("collected_at", "").startswith(date_str)
        ]

    def get_dates_with_news(self) -> list[str]:
        """뉴스가 있는 날짜 목록을 반환한다.
        
        Returns:
            YYYY-MM-DD 형식의 날짜 리스트 (정렬됨)
        """
        articles = self._articles or self.load_articles()
        dates = set()
        
        for article in articles:
            collected_at = article.get("collected_at", "")
            if collected_at:
                # ISO 형식에서 날짜만 추출
                date_part = collected_at.split("T")[0]
                dates.add(date_part)
        
        return sorted(dates, reverse=True)

    def get_article_by_id(self, article_id: str) -> dict[str, Any] | None:
        """ID로 기사를 조회한다.
        
        Args:
            article_id: 기사 ID
            
        Returns:
            기사 데이터 또는 None
        """
        articles = self._articles or self.load_articles()
        for article in articles:
            if article.get("id") == article_id:
                return article
        return None

    def delete_article(self, article_id: str) -> bool:
        """ID로 기사를 삭제한다.
        
        Args:
            article_id: 기사 ID
            
        Returns:
            삭제 성공 여부
        """
        articles = self.load_articles()
        new_articles = [a for a in articles if a.get("id") != article_id]
        
        if len(articles) == len(new_articles):
            return False
            
        self.save_articles(new_articles)
        return True

    def collect_news(
        self, categories: list[str] | None = None
    ) -> dict[str, list[dict[str, Any]]]:
        """네이버 뉴스를 수집한다.
        
        Args:
            categories: 수집할 카테고리 리스트 (None이면 전체)
            
        Returns:
            카테고리별 수집된 기사
        """
        from scraper.naver_scraper import scrape_all_categories
        
        collected = scrape_all_categories(categories)
        
        # 기존 기사와 병합
        existing = self.load_articles()
        all_new_articles = []
        
        for category_articles in collected.values():
            all_new_articles.extend(category_articles)
        
        merged = self.merge_articles(existing, all_new_articles)
        self.save_articles(merged)
        
        return collected


# ──────────────────────────────────────────────────────────────────
# 즐겨찾기 관련 독립 함수 (002 기능)
# ──────────────────────────────────────────────────────────────────

def toggle_favorite(article_id: str) -> bool:
    """기사의 즐겨찾기 상태를 토글한다.
    
    Args:
        article_id: 토글할 기사 ID
        
    Returns:
        성공 여부 (기사가 존재하지 않으면 False)
    """
    articles = load_news_articles()
    
    for article in articles:
        if article.get("id") == article_id:
            current_status = article.get("is_favorite", False)
            article["is_favorite"] = not current_status
            return save_news_articles(articles)
    
    return False


def get_favorites() -> list[dict[str, Any]]:
    """즐겨찾기된 기사 목록을 반환한다.
    
    Returns:
        is_favorite가 True인 기사 리스트
    """
    articles = load_news_articles()
    return [a for a in articles if a.get("is_favorite", False) is True]


def get_favorite_status(article_id: str) -> bool:
    """특정 기사의 즐겨찾기 상태를 조회한다.
    
    Args:
        article_id: 조회할 기사 ID
        
    Returns:
        즐겨찾기 여부 (기사가 없거나 is_favorite가 없으면 False)
    """
    articles = load_news_articles()
    
    for article in articles:
        if article.get("id") == article_id:
            return article.get("is_favorite", False)
    
    return False


# ──────────────────────────────────────────────────────────────────
# 일괄 삭제 관련 독립 함수 (002 기능)
# ──────────────────────────────────────────────────────────────────

def delete_all_articles() -> dict[str, Any]:
    """모든 뉴스 기사와 관련 다이어리를 삭제한다.
    
    Returns:
        삭제 결과 {'success': bool, 'deleted_count': int}
    """
    articles = load_news_articles()
    deleted_count = len(articles)
    
    # 모든 기사 삭제
    save_news_articles([])
    
    # 모든 다이어리 삭제
    save_diary_entries_dict({})
    
    return {"success": True, "deleted_count": deleted_count}


def delete_articles_by_category(category: str) -> dict[str, Any]:
    """특정 카테고리의 기사와 관련 다이어리를 삭제한다.
    
    Args:
        category: 삭제할 카테고리
        
    Returns:
        삭제 결과 {'success': bool, 'deleted_count': int}
    """
    articles = load_news_articles()
    diary_entries = load_diary_entries_dict()
    
    # 삭제할 기사 ID 수집
    ids_to_delete = set()
    remaining_articles = []
    
    for article in articles:
        if article.get("category") == category:
            ids_to_delete.add(article.get("id"))
        else:
            remaining_articles.append(article)
    
    deleted_count = len(ids_to_delete)
    
    # 기사 저장
    save_news_articles(remaining_articles)
    
    # 관련 다이어리 삭제
    for article_id in ids_to_delete:
        if article_id in diary_entries:
            del diary_entries[article_id]
    
    save_diary_entries_dict(diary_entries)
    
    return {"success": True, "deleted_count": deleted_count}


def delete_selected_articles(article_ids: list[str]) -> dict[str, Any]:
    """선택된 뉴스 기사와 관련 다이어리를 삭제한다.
    
    Args:
        article_ids: 삭제할 기사 ID 리스트
        
    Returns:
        삭제 결과 {'success': bool, 'deleted_count': int}
    """
    articles = load_news_articles()
    diary_entries = load_diary_entries_dict()
    
    ids_to_delete = set(article_ids)
    remaining_articles = [a for a in articles if a.get("id") not in ids_to_delete]
    
    deleted_count = len(articles) - len(remaining_articles)
    
    # 기사 저장
    save_news_articles(remaining_articles)
    
    # 관련 다이어리 삭제
    for article_id in ids_to_delete:
        if article_id in diary_entries:
            del diary_entries[article_id]
    
    save_diary_entries_dict(diary_entries)
    
    return {"success": True, "deleted_count": deleted_count}
