"""뉴스 수집 페이지 진입점.

메인 앱에서 호출되는 홈 페이지 렌더링 함수를 제공한다.
"""


def render_home_page():
    """홈 페이지(뉴스 수집)를 렌더링한다."""
    from app.pages.home_page import render_home
    render_home()
