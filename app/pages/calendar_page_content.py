"""캘린더 페이지 내용 모듈.

메인 앱에서 호출되는 캘린더 페이지 렌더링 함수를 제공한다.
"""

import streamlit as st
from datetime import date

from app.ui.theme.styles import get_glassmorphism_css
from app.ui.components.emoji_helper import get_emoji
from app.ui.layout.bento_grid import render_bento_calendar
from app.services.calendar_service import CalendarService
from app.services.news_service import NewsService, toggle_favorite


def render():
    """캘린더 페이지를 렌더링한다."""
    # 제목
    st.subheader(f"{get_emoji('calendar')} 스마트 이슈 캘린더")
    st.markdown(f"""
    <div class="info-section">
        날짜별로 수집된 뉴스와 개인적인 이슈를 한눈에 파악할 수 있는 스마트 캘린더입니다.<br>
        날짜를 클릭하여 해당 일의 주요 사건들을 복기하고 새로운 이슈를 기록해 보세요.
    </div>
    """, unsafe_allow_html=True)

    # 현재 연/월 상태
    if "calendar_year" not in st.session_state:
        st.session_state["calendar_year"] = date.today().year
    if "calendar_month" not in st.session_state:
        st.session_state["calendar_month"] = date.today().month

    # 헤더 및 수동 선택 영역
    col_y, col_m, col_info = st.columns([1, 1, 3])
    
    # 세션 상태 변화 감지를 위한 콜백 함수
    def update_year():
        st.session_state["calendar_year"] = st.session_state["cal_year_select"]
        
    def update_month():
        st.session_state["calendar_month"] = st.session_state["cal_month_select"]

    with col_y:
        year_options = [2024, 2025, 2026]
        current_year = st.session_state["calendar_year"]
        try:
            year_index = year_options.index(current_year)
        except ValueError:
            year_index = 2
            
        st.selectbox("년도", options=year_options, index=year_index, key="cal_year_select", on_change=update_year)

    with col_m:
        st.selectbox("월", options=list(range(1, 13)), index=st.session_state["calendar_month"] - 1, key="cal_month_select", on_change=update_month)

    with col_info:
        st.write("")
        st.markdown(f"<div style='margin-top:25px;'>현재 선택: <span class='neon-text'>{st.session_state['calendar_year']}년 {st.session_state['calendar_month']}월</span></div>", unsafe_allow_html=True)

    # 서비스 초기화
    calendar_service = CalendarService()
    news_service = NewsService()

    # 뉴스와 이슈가 있는 날짜 조회
    news_dates = news_service.get_dates_with_news()
    issue_dates = calendar_service.get_dates_with_issues()

    # 캘린더 렌더링
    st.markdown("---")

    def on_day_click(date_str: str):
        """날짜 클릭 핸들러."""
        st.session_state["selected_date"] = date_str

    render_bento_calendar(st.session_state["calendar_year"], st.session_state["calendar_month"], news_dates, issue_dates, on_day_click)

    # 선택된 날짜의 상세 정보
    st.markdown("---")

    if "selected_date" in st.session_state:
        selected_date = st.session_state["selected_date"]
        st.subheader(f"{get_emoji('date')} {selected_date}")
        
        col1, col2 = st.columns(2)
        
        # 해당 날짜의 뉴스 (Task 7)
        with col1:
            st.markdown(f"### {get_emoji('newspaper')} 뉴스")
            date_news = news_service.filter_by_date(selected_date)
            
            if date_news:
                # 카테고리별로 볼 수 있게 드롭박스 추가
                categories = ["전체", "정치", "경제", "사회", "생활/문화", "IT/과학", "세계"]
                selected_cat = st.selectbox("카테고리 필터", options=categories, key=f"cal_cat_{selected_date}")
                
                filtered_news = date_news
                if selected_cat != "전체":
                    filtered_news = [n for n in date_news if n.get("category") == selected_cat]
                
                if filtered_news:
                    for article in filtered_news:
                        article_id = article.get("id", "")
                        is_fav = article.get("is_favorite", False)
                        star_icon = "⭐" if is_fav else "☆"
                        
                        # 뉴스 수집 페이지와 동일한 UI 구성 (Request 6)
                        c_fav, c_link = st.columns([1, 9])
                        with c_fav:
                            if st.button(star_icon, key=f"cal_fav_{article_id}_{selected_date}"):
                                toggle_favorite(article_id)
                                st.rerun()
                        with c_link:
                            st.markdown(f"[{article['title']}]({article.get('url', article.get('link', '#'))})")
                else:
                    st.info(f"'{selected_cat}' 카테고리의 뉴스가 없습니다.")
            else:
                st.info("해당 날짜에 수집된 뉴스가 없습니다.")
        
        # 해당 날짜의 이슈 (Task 6 - 수정 기능 추가)
        with col2:
            st.markdown(f"### {get_emoji('memo')} 이슈")
            date_issues = calendar_service.get_issues_by_date(selected_date)
            
            # 이슈 추가 폼
            with st.expander(f"{get_emoji('add')} 새 이슈 추가", expanded=False):
                with st.form(key="calendar_add_issue_form"):
                    new_title = st.text_input("제목")
                    new_content = st.text_area("내용")
                    
                    if st.form_submit_button("저장"):
                        if new_title:
                            calendar_service.create_issue(
                                date=selected_date,
                                title=new_title,
                                content=new_content,
                            )
                            st.success("이슈가 추가되었습니다.")
                            st.rerun()
                        else:
                            st.warning("제목을 입력해주세요.")
            
            # 기존 이슈 표시
            if date_issues:
                for idx, issue in enumerate(date_issues):
                    created = issue.get("created_at", "")
                    created_str = created[:10] if isinstance(created, str) else ""
                    issue_id = issue.get("id", f"idx_{idx}")
                    with st.container():
                        st.markdown(
                            f"""
                            <div class="glass-card">
                                <strong>{issue.get('title', '')}</strong>
                                <p>{issue.get('content', '')}</p>
                                <small>생성: {created_str}</small>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                        col_edit, col_del = st.columns(2)
                        with col_edit:
                            # 각 이슈마다 고유 인덱스를 포함한 key로 중복 완전 방지
                            if st.button(f"{get_emoji('edit')} 수정", key=f"calendar_edit_issue_{selected_date}_{idx}"):
                                st.session_state["editing_issue"] = issue
                                st.rerun()

                        with col_del:
                            if st.button(f"{get_emoji('delete')} 삭제", key=f"calendar_del_issue_{selected_date}_{idx}"):
                                calendar_service.delete_issue(issue.get("id", ""))
                                st.success("이슈가 삭제되었습니다.")
                                st.rerun()

                if "editing_issue" in st.session_state and st.session_state["editing_issue"]:
                    # 수정 모달이 열려 있을 때도 상태를 유지하도록 컨테이너 외부에 배치 고려 가능하나 현재로도 작동함
                    # 단, Streamlit 특성상 다이얼로그 호출 후 리런되므로 순서 주의
                    _render_edit_issue_modal()
            else:
                st.info("해당 날짜에 등록된 이슈가 없습니다.")

    else:
        st.info(f"{get_emoji('info')} 캘린더에서 날짜를 클릭하면 해당 날짜의 뉴스와 이슈를 확인할 수 있습니다.")

    # 수정 모달을 모든 조건문 외부(최하단)에서 한 번 더 체크하여 안정성 확보 (Request 4 에러 방지)
    if "editing_issue" in st.session_state and st.session_state["editing_issue"] and "selected_date" not in st.session_state:
         # 날짜 선택이 안 된 상태에서 수정 모달이 남아있으면 정리
         st.session_state["editing_issue"] = None


@st.dialog("이슈 수정")
def _render_edit_issue_modal():
    """이슈 수정 모달을 렌더링한다."""
    issue = st.session_state.get("editing_issue")
    if not issue:
        st.session_state["editing_issue"] = None
        st.rerun()
        return

    calendar_service = CalendarService()
    new_title = st.text_input("제목", value=issue.get("title", ""))
    new_content = st.text_area("내용", value=issue.get("content", ""))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("수정 완료", use_container_width=True):
            calendar_service.update_issue(issue["id"], title=new_title, content=new_content)
            st.toast("이슈가 수정되었습니다.")
            st.session_state["editing_issue"] = None
            st.rerun()
    with col2:
        if st.button("취소", use_container_width=True):
            st.session_state["editing_issue"] = None
            st.rerun()
