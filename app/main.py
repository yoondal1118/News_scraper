"""네이버 뉴스 스크래퍼 및 다이어리 앱.

Streamlit 메인 진입점.
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from app.ui.theme.styles import get_glassmorphism_css
from app.ui.components.emoji_helper import get_emoji
import app.pages as pages

# 페이지 설정 (사이바 숨김)
st.set_page_config(
    page_title="네이버 뉴스 다이어리",
    page_icon=get_emoji("newspaper"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Glassmorphism 스타일 및 사이드바 숨김 적용
st.markdown(get_glassmorphism_css(), unsafe_allow_html=True)
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }
    .css-1d391kg { display: none; }
    section[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# 세션 상태로 현재 페이지 및 로그인 유저 관리
if "user" not in st.session_state:
    # 쿼리 파라미터에서 유저 정보 복구 시도 (새로고침 대응)
    saved_user = st.query_params.get("user")
    st.session_state["user"] = saved_user if saved_user else None

if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "뉴스 수집"

# 로그인 상태 확인
if not st.session_state["user"]:
    from app.pages.login_page import render_login_page
    render_login_page()
    st.stop()
else:
    # 로그인 상태 유지 (쿼리 파라미터 업데이트)
    if st.query_params.get("user") != st.session_state["user"]:
        st.query_params["user"] = st.session_state["user"]

# --- 로그인된 경우의 화면 구성 ---

# 헤더 (로그아웃 버튼 우측 상단)
header_left, header_right = st.columns([8, 2])
with header_right:
    if st.button(f"{st.session_state['user']} (로그아웃)", use_container_width=True):
        st.session_state["user"] = None
        st.query_params.clear() # 쿼리 파라미터도 삭제
        st.rerun()

# 앱 타이틀
st.title(f"{get_emoji('newspaper')} 네이버 뉴스 다이어리")

# 상단 네비게이션 (Floating Island Style)
nav_cols = st.columns([1, 2, 2, 2, 1])
with nav_cols[1]:
    is_home = st.session_state["active_tab"] == "뉴스 수집"
    if st.button(f"{get_emoji('newspaper')} 뉴스 수집", use_container_width=True, type="primary" if is_home else "secondary"):
        st.session_state["active_tab"] = "뉴스 수집"
        st.rerun()
with nav_cols[2]:
    is_calendar = st.session_state["active_tab"] == "캘린더"
    if st.button(f"{get_emoji('calendar')} 캘린더", use_container_width=True, type="primary" if is_calendar else "secondary"):
        st.session_state["active_tab"] = "캘린더"
        st.rerun()
with nav_cols[3]:
    is_fav = st.session_state["active_tab"] == "저장된 뉴스기사"
    if st.button(f"{get_emoji('star')} 저장된 뉴스기사", use_container_width=True, type="primary" if is_fav else "secondary"):
        st.session_state["active_tab"] = "저장된 뉴스기사"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 현재 선택된 페이지만 렌더링
if st.session_state["active_tab"] == "뉴스 수집":
    pages.render_home_page()
elif st.session_state["active_tab"] == "캘린더":
    pages.render_calendar_page()
elif st.session_state["active_tab"] == "저장된 뉴스기사":
    pages.render_favorites_page()
else:
    st.info("페이지를 선택해주세요.")
