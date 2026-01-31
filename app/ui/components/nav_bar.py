"""상단 중앙 네비게이션 바 컴포넌트.

슬라이딩 인디케이터를 포함한 세련된 상단 네비게이션을 제공한다.
"""

import streamlit as st
import emoji


def get_nav_css() -> str:
    """상단 네비게이션 바 CSS를 반환한다."""
    return """
    <style>
    /* 사이드바 숨기기 */
    [data-testid="stSidebar"] { display: none; }
    
    /* 네비게이션 컨테이너 */
    .nav-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 40px;
        padding: 16px 24px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 0 auto 24px auto;
        max-width: 600px;
        position: relative;
    }
    
    /* 네비게이션 아이템 */
    .nav-item {
        position: relative;
        padding: 8px 16px;
        color: #E0E0E0;
        text-decoration: none;
        font-size: 15px;
        font-weight: 500;
        cursor: pointer;
        transition: color 0.3s ease;
        white-space: nowrap;
    }
    
    .nav-item:hover {
        color: #00D4FF;
    }
    
    .nav-item.active {
        color: #00D4FF;
    }
    
    /* 슬라이딩 인디케이터 */
    .nav-item::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #00D4FF, #7B2FF7);
        border-radius: 2px;
        transition: width 0.3s ease;
    }
    
    .nav-item:hover::after,
    .nav-item.active::after {
        width: 80%;
    }
    
    /* 아이콘 스타일 */
    .nav-icon {
        margin-right: 6px;
    }
    </style>
    """


def render_nav_bar(current_page: str = "뉴스 수집") -> str | None:
    """상단 네비게이션 바를 렌더링한다.
    
    Args:
        current_page: 현재 활성화된 페이지명
        
    Returns:
        클릭된 페이지명 또는 None
    """
    # CSS 주입
    st.markdown(get_nav_css(), unsafe_allow_html=True)
    
    # 메뉴 아이템 정의 (아이콘 + 텍스트)
    menu_items = [
        {"icon": emoji.emojize(":newspaper:"), "label": "뉴스 수집", "page": "home"},
        {"icon": emoji.emojize(":calendar:"), "label": "캘린더", "page": "calendar"},
        {"icon": emoji.emojize(":star:"), "label": "저장된 뉴스기사", "page": "favorites"},
    ]
    
    # 네비게이션 HTML 생성
    nav_html = '<div class="nav-container">'
    for item in menu_items:
        active_class = "active" if item["label"] == current_page else ""
        nav_html += f'''
            <span class="nav-item {active_class}" data-page="{item['page']}">
                <span class="nav-icon">{item['icon']}</span>{item['label']}
            </span>
        '''
    nav_html += '</div>'
    
    st.markdown(nav_html, unsafe_allow_html=True)
    
    # Streamlit 버튼 기반 네비게이션 (실제 클릭 처리)
    cols = st.columns([1, 1, 1, 1, 1])
    
    clicked_page = None
    with cols[1]:
        if st.button(f"{emoji.emojize(':newspaper:')} 뉴스 수집", key="nav_home", use_container_width=True):
            clicked_page = "home"
    with cols[2]:
        if st.button(f"{emoji.emojize(':calendar:')} 캘린더", key="nav_calendar", use_container_width=True):
            clicked_page = "calendar"
    with cols[3]:
        if st.button(f"{emoji.emojize(':star:')} 저장된 뉴스기사", key="nav_favorites", use_container_width=True):
            clicked_page = "favorites"
    
    return clicked_page


def get_page_from_session() -> str:
    """세션에서 현재 페이지를 가져온다."""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    # 타입 검증: 문자열이 아니면 "home"으로 재설정
    if not isinstance(st.session_state.current_page, str) or st.session_state.current_page not in ("home", "calendar", "favorites"):
        st.session_state.current_page = "home"
    return st.session_state.current_page


def set_page_to_session(page: str) -> None:
    """세션에 현재 페이지를 설정한다."""
    st.session_state.current_page = page
