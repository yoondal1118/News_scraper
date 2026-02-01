"""저장된 뉴스기사 페이지 내용 모듈.

즐겨찾기한 뉴스 기사 목록과 다이어리 모달을 제공한다.
"""

import streamlit as st
from datetime import datetime

from app.ui.components.emoji_helper import get_emoji
from app.services.news_service import get_favorites, toggle_favorite
from app.services.diary_service import DiaryService
from app.services.storage_util import (
    load_diary_entries_dict,
    save_diary_entries_dict,
    get_current_datetime,
)


def render():
    """저장된 뉴스기사 페이지를 렌더링한다."""
    st.subheader(f"{get_emoji('star')} 저장된 뉴스기사")
    st.markdown(f"""
    <div class="info-section">
        관심 기사로 등록한 뉴스들을 모아보고, 나만의 다이어리를 작성할 수 있는 공간입니다.<br>
        기사 원문을 다시 읽거나, 기록된 생각을 수정하며 지식을 쌓아보세요.
    </div>
    """, unsafe_allow_html=True)
    
    # 즐겨찾기 목록 로드
    favorites = get_favorites()
    
    if not favorites:
        st.info(f"{get_emoji('info')} 저장된 뉴스기사가 없습니다. 뉴스 수집 페이지에서 기사를 즐겨찾기해 주세요.")
        return
    
    st.markdown(f"**총 {len(favorites)}개의 저장된 기사**")
    st.markdown("---")
    
    # 다이어리 엔트리 로드
    diary_entries = load_diary_entries_dict()
    
    # 기사 목록 표시
    for idx, article in enumerate(favorites):
        article_id = article.get("id", "")
        has_diary = article_id in diary_entries
        # 홈 페이지와 제목 형식을 맞추기 위해 제목 앞 메모 아이콘은 제거한다.
        url = article.get('url', article.get('link', '#'))

        title = article.get("title", "제목 없음")
        publisher = article.get("publisher")
        category = article.get("category", "")

        with st.container():
            # 하나의 블럭 안에 즐겨찾기, 제목, 링크, 다이어리 버튼을 모두 배치
            box = st.container()
            with box:
                header_main, header_star = st.columns([0.9, 0.1])

                with header_main:
                    # 메타 정보: 즐겨찾기 페이지에서는 카테고리는 제목에 포함되므로,
                    # 메타 라인에는 언론사 등만 표시한다.
                    meta_parts = []
                    if publisher and publisher != "N/A":
                        meta_parts.append(publisher)
                    meta_text = " | ".join(meta_parts)

                    # 제목 형식: [카테고리] 제목 (홈 페이지와 동일하게, 메모 아이콘 제거)
                    prefix = f"[{category}] " if category else ""
                    title_html = f"<strong>{prefix}{title}</strong>"
                    if meta_text:
                        title_html += f"<br><span style='color:#888;font-size:0.85em;'>{meta_text}</span>"

                    st.markdown(title_html, unsafe_allow_html=True)

                with header_star:
                    if st.button("⭐", key=f"fav_toggle_{article_id}", help="즐겨찾기 해제", type="secondary"):
                        toggle_favorite(article_id)
                        st.toast("즐겨찾기가 해제되었습니다.")
                        st.rerun()

                # 가운데 하단에 뉴스 바로가기 / 다이어리 버튼 배치
                spacer_l, center, spacer_r = st.columns([1, 2, 1])
                with center:
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        st.link_button(f"{get_emoji('link')} 뉴스 바로가기", url, use_container_width=True)
                    with btn_col2:
                        # 요청: 다이어리 버튼에서는 아이콘 제거
                        if st.button("다이어리", key=f"diary_btn_{idx}", use_container_width=True, type="primary"):
                            st.session_state["modal_article_id"] = article_id
                            st.session_state["modal_article"] = article
                            st.rerun()

        st.markdown("---")
    
    # 다이어리 모달
    if "modal_article_id" in st.session_state and st.session_state["modal_article_id"]:
        _render_diary_modal()


@st.dialog("다이어리 작성")
def _render_diary_modal():
    """다이어리 작성/조회 모달을 렌더링한다."""
    article_id = st.session_state.get("modal_article_id")
    article = st.session_state.get("modal_article", {})
    
    if not article_id:
        st.error("기사 정보를 찾을 수 없습니다.")
        return
    
    # 기사 요약 표시
    st.markdown(f"### {article.get('title', '제목 없음')}")
    
    # N/A 표시 제거 및 있는 정보만 노출 (Request 8)
    info_parts = []
    if article.get('publisher') and article.get('publisher') != "N/A":
        info_parts.append(f"**언론사**: {article['publisher']}")
    if article.get('category') and article.get('category') != "N/A":
        info_parts.append(f"**카테고리**: {article['category']}")
    if article.get('time') and article.get('time') != "N/A":
        info_parts.append(f"**시간**: {article['time']}")
    
    if info_parts:
        st.markdown(" | ".join(info_parts))
    
    if article.get('url') or article.get('link'):
        st.markdown(f"[{get_emoji('link')} 원문 보기]({article.get('url', article.get('link'))})")
    
    st.markdown("---")
    
    # 기존 다이어리 로드
    diary_entries = load_diary_entries_dict()
    existing_entry = diary_entries.get(article_id, {})
    existing_content = existing_entry.get("content", "")
    
    # 다이어리 입력
    st.markdown(f"### {get_emoji('memo')} 나의 다이어리")
    diary_content = st.text_area(
        "내용을 입력하세요",
        value=existing_content,
        height=200,
        key="favorites_diary_textarea",
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"{get_emoji('save')} 저장", use_container_width=True):
            if diary_content.strip():
                # 저장
                diary_entries[article_id] = {
                    "content": diary_content,
                    "created_at": existing_entry.get("created_at", get_current_datetime()),
                    "updated_at": get_current_datetime(),
                }
                save_diary_entries_dict(diary_entries)
                st.toast("다이어리가 저장되었습니다!")
                st.session_state["modal_article_id"] = None
                st.rerun()
            else:
                st.warning("내용을 입력해주세요.")
    
    with col2:
        if st.button("닫기", use_container_width=True):
            st.session_state["modal_article_id"] = None
            st.rerun()
