# Streamlit 멀티페이지 앱 페이지 모듈

def render_home_page():
    """뉴스 수집 페이지를 렌더링한다."""
    from app.pages.home_page import render_home
    render_home()


def render_calendar_page():
    """캘린더 페이지를 렌더링한다."""
    from app.pages import calendar_page_content
    calendar_page_content.render()


def render_favorites_page():
    """저장된 뉴스기사 페이지를 렌더링한다."""
    from app.pages import favorites_page_content
    favorites_page_content.render()
