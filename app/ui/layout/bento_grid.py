"""Bento Grid 레이아웃 모듈.

Bento Grid 기반 캘린더 레이아웃을 제공한다.
"""

import calendar
from datetime import date, datetime
from typing import Any, Callable


class BentoGrid:
    """Bento Grid 기반 캘린더 레이아웃."""

    def __init__(
        self,
        year: int,
        month: int,
        news_dates: list[str] | None = None,
        issue_dates: list[str] | None = None,
    ) -> None:
        """Bento Grid를 초기화한다.
        
        Args:
            year: 연도
            month: 월 (1-12)
            news_dates: 뉴스가 있는 날짜 리스트 (YYYY-MM-DD)
            issue_dates: 이슈가 있는 날짜 리스트 (YYYY-MM-DD)
        """
        self.year = year
        self.month = month
        self.news_dates = set(news_dates or [])
        self.issue_dates = set(issue_dates or [])
        self._calendar = calendar.Calendar(firstweekday=6)  # 일요일 시작

    def get_month_days(self) -> list[int]:
        """월의 일수를 반환한다.
        
        Returns:
            1부터 마지막 날까지의 리스트
        """
        _, num_days = calendar.monthrange(self.year, self.month)
        return list(range(1, num_days + 1))

    def get_weeks(self) -> list[list[int | None]]:
        """주 단위 구조를 반환한다.
        
        Returns:
            7일 단위로 구성된 주 리스트 (None은 빈 칸)
        """
        weeks = []
        month_days = self._calendar.monthdayscalendar(self.year, self.month)
        
        for week in month_days:
            week_data = []
            for day in week:
                week_data.append(day if day != 0 else None)
            weeks.append(week_data)
        
        return weeks

    def _format_date(self, day: int) -> str:
        """날짜를 YYYY-MM-DD 형식으로 변환한다."""
        return f"{self.year:04d}-{self.month:02d}-{day:02d}"

    def has_news(self, day: int) -> bool:
        """해당 날짜에 뉴스가 있는지 확인한다.
        
        Args:
            day: 일 (1-31)
            
        Returns:
            뉴스 유무
        """
        date_str = self._format_date(day)
        return date_str in self.news_dates

    def has_issue(self, day: int) -> bool:
        """해당 날짜에 이슈가 있는지 확인한다.
        
        Args:
            day: 일 (1-31)
            
        Returns:
            이슈 유무
        """
        date_str = self._format_date(day)
        return date_str in self.issue_dates

    def get_day_css_class(self, day: int) -> str:
        """날짜에 적용할 CSS 클래스를 반환한다.
        
        Args:
            day: 일 (1-31)
            
        Returns:
            CSS 클래스 문자열
        """
        classes = ["calendar-cell"]
        
        if self.has_news(day):
            classes.append("has-news")
        
        if self.has_issue(day):
            classes.append("has-issue")
        
        # 오늘인 경우
        today = date.today()
        if today.year == self.year and today.month == self.month and today.day == day:
            classes.append("today")
        
        return " ".join(classes)

    def get_next_month(self) -> tuple[int, int]:
        """다음 달의 연도와 월을 반환한다.
        
        Returns:
            (연도, 월) 튜플
        """
        if self.month == 12:
            return (self.year + 1, 1)
        return (self.year, self.month + 1)

    def get_prev_month(self) -> tuple[int, int]:
        """이전 달의 연도와 월을 반환한다.
        
        Returns:
            (연도, 월) 튜플
        """
        if self.month == 1:
            return (self.year - 1, 12)
        return (self.year, self.month - 1)

    def get_month_name(self) -> str:
        """월 이름을 반환한다 (한국어).
        
        Returns:
            월 이름
        """
        return f"{self.year}년 {self.month}월"

    def get_weekday_headers(self) -> list[str]:
        """요일 헤더를 반환한다.
        
        Returns:
            요일 리스트
        """
        return ["일", "월", "화", "수", "목", "금", "토"]


def render_bento_calendar(
    year: int,
    month: int,
    news_dates: list[str],
    issue_dates: list[str],
    on_day_click: Callable[[str], None] | None = None,
) -> None:
    """Bento Grid 스타일의 캘린더를 렌더링한다.
    
    Streamlit 컨텍스트에서 호출되어야 한다.
    
    Args:
        year: 연도
        month: 월
        news_dates: 뉴스가 있는 날짜 리스트
        issue_dates: 이슈가 있는 날짜 리스트
        on_day_click: 날짜 클릭 콜백
    """
    import streamlit as st
    from app.ui.components.emoji_helper import get_emoji
    
    grid = BentoGrid(year, month, news_dates, issue_dates)
    
    # 월 네비게이션
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button(f"{get_emoji('back')} 이전"):
            prev_year, prev_month = grid.get_prev_month()
            st.session_state["calendar_year"] = prev_year
            st.session_state["calendar_month"] = prev_month
            st.rerun()
    
    with col2:
        st.markdown(f"### {grid.get_month_name()}")
    
    with col3:
        if st.button(f"다음 {get_emoji('forward')}"):
            next_year, next_month = grid.get_next_month()
            st.session_state["calendar_year"] = next_year
            st.session_state["calendar_month"] = next_month
            st.rerun()
    
    # 요일 헤더
    headers = grid.get_weekday_headers()
    cols = st.columns(7)
    for i, header in enumerate(headers):
        with cols[i]:
            st.markdown(f"**{header}**")
    
    # 주별 날짜 그리드 (단일 버튼만 사용해서 테두리 중복 제거)
    weeks = grid.get_weeks()
    for week in weeks:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day is None:
                    st.write("")
                else:
                    has_news = grid.has_news(day)
                    has_issue = grid.has_issue(day)

                    badges = ""
                    if has_news:
                        badges += get_emoji("newspaper")
                    if has_issue:
                        badges += get_emoji("memo")

                    label = f"{day} {badges}" if badges else str(day)

                    if st.button(label, key=f"day_{year}_{month}_{day}"):
                        date_str = f"{year:04d}-{month:02d}-{day:02d}"
                        if on_day_click:
                            on_day_click(date_str)
                        else:
                            st.session_state["selected_date"] = date_str
