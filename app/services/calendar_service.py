"""캘린더 이슈 서비스 모듈.

날짜별 이슈의 CRUD 기능을 담당한다.
"""

from typing import Any

from app.services.storage_util import (
    load_calendar_issues,
    save_calendar_issues,
    generate_id,
    get_current_datetime,
)


class CalendarService:
    """캘린더 이슈 관리 서비스."""

    def __init__(self) -> None:
        """캘린더 서비스를 초기화한다."""
        self._issues: list[dict[str, Any]] | None = None

    def _load_issues(self) -> list[dict[str, Any]]:
        """이슈 목록을 로드한다."""
        if self._issues is None:
            self._issues = load_calendar_issues()
        return self._issues

    def _save_issues(self) -> bool:
        """이슈 목록을 저장한다."""
        if self._issues is not None:
            return save_calendar_issues(self._issues)
        return False

    def create_issue(
        self,
        date: str,
        title: str,
        content: str,
    ) -> dict[str, Any]:
        """새 이슈를 생성한다.
        
        Args:
            date: YYYY-MM-DD 형식의 날짜
            title: 이슈 제목
            content: 이슈 내용
            
        Returns:
            생성된 이슈 데이터
        """
        issues = self._load_issues()
        
        new_issue = {
            "id": generate_id("issue"),
            "date": date,
            "title": title,
            "content": content,
            "created_at": get_current_datetime(),
            "updated_at": get_current_datetime(),
        }
        
        issues.append(new_issue)
        self._issues = issues
        self._save_issues()
        
        return new_issue

    def get_issues_by_date(self, date: str) -> list[dict[str, Any]]:
        """특정 날짜의 이슈 목록을 조회한다.
        
        Args:
            date: YYYY-MM-DD 형식의 날짜
            
        Returns:
            해당 날짜의 이슈 리스트
        """
        issues = self._load_issues()
        return [issue for issue in issues if issue.get("date") == date]

    def get_issue_by_id(self, issue_id: str) -> dict[str, Any] | None:
        """ID로 이슈를 조회한다.
        
        Args:
            issue_id: 이슈 ID
            
        Returns:
            이슈 데이터 또는 None
        """
        issues = self._load_issues()
        for issue in issues:
            if issue.get("id") == issue_id:
                return issue
        return None

    def update_issue(
        self,
        issue_id: str,
        title: str | None = None,
        content: str | None = None,
    ) -> dict[str, Any] | None:
        """이슈를 수정한다.
        
        Args:
            issue_id: 수정할 이슈 ID
            title: 새 제목 (None이면 유지)
            content: 새 내용 (None이면 유지)
            
        Returns:
            수정된 이슈 데이터 또는 None
        """
        issues = self._load_issues()
        
        for issue in issues:
            if issue.get("id") == issue_id:
                if title is not None:
                    issue["title"] = title
                if content is not None:
                    issue["content"] = content
                issue["updated_at"] = get_current_datetime()
                
                self._issues = issues
                self._save_issues()
                return issue
        
        return None

    def delete_issue(self, issue_id: str) -> bool:
        """이슈를 삭제한다.
        
        Args:
            issue_id: 삭제할 이슈 ID
            
        Returns:
            삭제 성공 여부
        """
        issues = self._load_issues()
        original_len = len(issues)
        
        self._issues = [
            issue for issue in issues if issue.get("id") != issue_id
        ]
        
        if len(self._issues) < original_len:
            self._save_issues()
            return True
        
        return False

    def get_dates_with_issues(self) -> list[str]:
        """이슈가 있는 날짜 목록을 반환한다.
        
        Returns:
            YYYY-MM-DD 형식의 날짜 리스트 (정렬됨)
        """
        issues = self._load_issues()
        dates = set()
        
        for issue in issues:
            date = issue.get("date")
            if date:
                dates.add(date)
        
        return sorted(dates, reverse=True)

    def get_all_issues(self) -> list[dict[str, Any]]:
        """모든 이슈를 조회한다.
        
        Returns:
            전체 이슈 리스트
        """
        return self._load_issues()
