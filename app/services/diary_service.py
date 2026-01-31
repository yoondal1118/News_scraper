"""다이어리 서비스 모듈.

기사별 다이어리 엔트리의 CRUD 기능을 담당한다.
명세: 기사당 다이어리 엔트리는 1개만 허용.
"""

from typing import Any

from app.services.storage_util import (
    load_diary_entries,
    save_diary_entries,
    generate_id,
    get_current_datetime,
)


class DiaryService:
    """다이어리 엔트리 관리 서비스."""

    def __init__(self) -> None:
        """다이어리 서비스를 초기화한다."""
        self._entries: list[dict[str, Any]] | None = None

    def _load_entries(self) -> list[dict[str, Any]]:
        """엔트리 목록을 로드한다."""
        if self._entries is None:
            self._entries = load_diary_entries()
        return self._entries

    def _save_entries(self) -> bool:
        """엔트리 목록을 저장한다."""
        if self._entries is not None:
            return save_diary_entries(self._entries)
        return False

    def create_entry(
        self,
        article_id: str,
        summary: str,
        opinion: str,
    ) -> dict[str, Any]:
        """새 다이어리 엔트리를 생성한다.
        
        기사당 1개 엔트리만 허용되므로, 기존 엔트리가 있으면 업데이트한다.
        
        Args:
            article_id: 연관 기사 ID
            summary: 요약 내용
            opinion: 의견 내용
            
        Returns:
            생성/업데이트된 엔트리 데이터
        """
        entries = self._load_entries()
        
        # 기존 엔트리 확인 (기사당 1개 제약)
        existing = self.get_entry_by_article_id(article_id)
        if existing:
            # 기존 엔트리 업데이트
            return self.update_entry(
                entry_id=existing["id"],
                summary=summary,
                opinion=opinion,
            )
        
        # 새 엔트리 생성
        new_entry = {
            "id": generate_id("diary"),
            "article_id": article_id,
            "summary": summary,
            "opinion": opinion,
            "created_at": get_current_datetime(),
            "updated_at": get_current_datetime(),
        }
        
        entries.append(new_entry)
        self._entries = entries
        self._save_entries()
        
        return new_entry

    def get_entry_by_article_id(self, article_id: str) -> dict[str, Any] | None:
        """기사 ID로 다이어리 엔트리를 조회한다.
        
        Args:
            article_id: 기사 ID
            
        Returns:
            엔트리 데이터 또는 None
        """
        entries = self._load_entries()
        for entry in entries:
            if entry.get("article_id") == article_id:
                return entry
        return None

    def get_entries_by_article(self, article_id: str) -> list[dict[str, Any]]:
        """기사 ID로 모든 엔트리를 조회한다.
        
        명세상 기사당 1개이므로 최대 1개 반환.
        
        Args:
            article_id: 기사 ID
            
        Returns:
            엔트리 리스트
        """
        entry = self.get_entry_by_article_id(article_id)
        return [entry] if entry else []

    def get_entry_by_id(self, entry_id: str) -> dict[str, Any] | None:
        """엔트리 ID로 조회한다.
        
        Args:
            entry_id: 엔트리 ID
            
        Returns:
            엔트리 데이터 또는 None
        """
        entries = self._load_entries()
        for entry in entries:
            if entry.get("id") == entry_id:
                return entry
        return None

    def update_entry(
        self,
        entry_id: str,
        summary: str | None = None,
        opinion: str | None = None,
    ) -> dict[str, Any] | None:
        """다이어리 엔트리를 수정한다.
        
        Args:
            entry_id: 수정할 엔트리 ID
            summary: 새 요약 (None이면 유지)
            opinion: 새 의견 (None이면 유지)
            
        Returns:
            수정된 엔트리 데이터 또는 None
        """
        entries = self._load_entries()
        
        for entry in entries:
            if entry.get("id") == entry_id:
                if summary is not None:
                    entry["summary"] = summary
                if opinion is not None:
                    entry["opinion"] = opinion
                entry["updated_at"] = get_current_datetime()
                
                self._entries = entries
                self._save_entries()
                return entry
        
        return None

    def delete_entry(self, entry_id: str) -> bool:
        """다이어리 엔트리를 삭제한다.
        
        Args:
            entry_id: 삭제할 엔트리 ID
            
        Returns:
            삭제 성공 여부
        """
        entries = self._load_entries()
        original_len = len(entries)
        
        self._entries = [
            entry for entry in entries if entry.get("id") != entry_id
        ]
        
        if len(self._entries) < original_len:
            self._save_entries()
            return True
        
        return False

    def get_all_entries(self) -> list[dict[str, Any]]:
        """모든 엔트리를 조회한다.
        
        Returns:
            전체 엔트리 리스트
        """
        return self._load_entries()
