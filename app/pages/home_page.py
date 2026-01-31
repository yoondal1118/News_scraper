"""뉴스 수집(홈) 페이지 모듈.

카테고리 선택, 뉴스 수집, 즐겨찾기/체크박스 기반 삭제 등의 기능을 제공한다.
"""

from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

from app.ui.components.emoji_helper import get_emoji
from app.ui.theme.styles import get_glassmorphism_css
from app.services.news_service import NewsService, delete_selected_articles, toggle_favorite


# 카테고리 상수
CATEGORIES: List[str] = [
    "정치",
    "경제",
    "사회",
    "생활/문화",
    "IT/과학",
    "세계",
]


def get_category_options() -> List[str]:
    """카테고리 선택 옵션을 반환한다."""

    return CATEGORIES.copy()


def get_category_emoji(category: str) -> str:
    """카테고리별 이모지를 반환한다."""

    mapping = {
        "정치": "🏛️",
        "경제": "💰",
        "사회": "🌐",
        "생활/문화": "🎨",
        "IT/과학": "💻",
        "세계": "🌍",
    }
    return mapping.get(category, "📰")


def format_news_for_display(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """뉴스 데이터를 화면 표시용 포맷으로 변환한다."""

    display_data: List[Dict[str, Any]] = []
    for article in articles:
        display_data.append(
            {
                "id": article.get("id", ""),
                "title": article.get("title", ""),
                "category": article.get("category", ""),
                "url": article.get("url", ""),
                "emoji": get_category_emoji(article.get("category", "")),
                "collected_at": article.get("collected_at", ""),
            }
        )
    return display_data


def group_by_category(articles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """기사를 카테고리별로 그룹화한다."""

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for article in articles:
        category = article.get("category", "기타")
        grouped.setdefault(category, []).append(article)
    return grouped


def get_empty_state_message() -> str:
    """뉴스가 없을 때 표시할 메시지를 반환한다."""

    empty_emoji = get_emoji("empty")
    return f"{empty_emoji} 수집된 뉴스가 없습니다. 카테고리를 선택하고 수집 버튼을 눌러주세요."


def get_loading_message() -> str:
    """로딩 중 메시지를 반환한다."""

    loading_emoji = get_emoji("loading")
    return f"{loading_emoji} 뉴스를 수집하고 있습니다..."


def get_error_message(error: str) -> str:
    """에러 메시지를 포맷한다."""

    error_emoji = get_emoji("error")
    return f"{error_emoji} 오류가 발생했습니다: {error}"


def get_success_message(count: int) -> str:
    """수집 성공 메시지를 반환한다."""

    success_emoji = get_emoji("success")
    return f"{success_emoji} {count}개의 뉴스가 수집되었습니다."


def render_home() -> None:
    """홈(뉴스 수집) 페이지를 렌더링한다."""

    # 스타일 적용
    st.markdown(get_glassmorphism_css(), unsafe_allow_html=True)

    st.subheader(f"{get_emoji('newspaper')} 뉴스 수집")

    # 페이지 설명
    st.markdown(
        f"""
        <div class=\"info-section\">
            네이버의 최신 뉴스를 카테고리별로 수집하고 관리할 수 있습니다.<br>
            중요한 기사는 별(⭐)로 저장하고, 필요 없는 기사는 체크박스로 선택해 한꺼번에 삭제하세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 상단 카테고리 선택 & 수집 버튼
    with st.container():
        col_select, col_btn = st.columns([3, 1])

        with col_select:
            selected_category = st.selectbox(
                "카테고리 선택",
                options=["전체"] + CATEGORIES,
                index=0,
                key="home_category_selector",
            )

            # 카테고리 변경 시 페이지 초기화
            if (
                "prev_category" not in st.session_state
                or st.session_state["prev_category"] != selected_category
            ):
                st.session_state["pagination_page"] = 1
                st.session_state["prev_category"] = selected_category

        with col_btn:
            st.write("")  # 수직 정렬용
            collect_trigger = st.button(
                f"{get_emoji('collect')} 뉴스 수집",
                use_container_width=True,
                type="primary",
            )

    service = NewsService()

    # 수집 실행
    if collect_trigger:
        categories_to_collect = (
            CATEGORIES if selected_category == "전체" else [selected_category]
        )
        with st.spinner(get_loading_message()):
            try:
                collected = service.collect_news(categories_to_collect)
                total = sum(len(v) for v in collected.values())
                st.toast(get_success_message(total))
                st.rerun()
            except Exception as e:  # pragma: no cover
                st.error(get_error_message(str(e)))

    # 기사 로드 및 필터링
    all_articles = service.load_articles()
    if selected_category != "전체":
        articles = [a for a in all_articles if a.get("category") == selected_category]
    else:
        articles = all_articles

    if not articles:
        st.info(get_empty_state_message())
        return

    # 대량 삭제 컨트롤
    st.write("---")
    col_sel1, col_sel2, _ = st.columns([2, 2, 6])

    with col_sel1:
        if st.button("전체선택", use_container_width=True, type="secondary"):
            for a in articles:
                st.session_state[f"select_{a['id']}"] = True
            st.rerun()

    with col_sel2:
        # 선택 삭제 버튼에서 아이콘 제거, 더 강조되도록 primary 처리
        if st.button(
            "선택 삭제",
            use_container_width=True,
            type="primary",
        ):
            selected_ids = [
                a["id"] for a in articles if st.session_state.get(f"select_{a['id']}")
            ]
            if selected_ids:
                st.session_state["confirm_delete_selected"] = selected_ids
            else:
                st.warning("삭제할 기사를 선택해주세요.")

    if st.session_state.get("confirm_delete_selected"):
        ids_to_del = st.session_state["confirm_delete_selected"]
        st.warning(f"⚠️ 선택한 {len(ids_to_del)}개의 기사를 삭제하시겠습니까?")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button("✅ 확인", key="confirm_bulk_yes"):
                result = delete_selected_articles(ids_to_del)
                st.toast(f"✅ {result['deleted_count']}개의 기사가 삭제되었습니다.")
                for aid in ids_to_del:
                    st.session_state.pop(f"select_{aid}", None)
                st.session_state["confirm_delete_selected"] = None
                st.rerun()
        with col_c2:
            if st.button("❌ 취소", key="confirm_bulk_no"):
                st.session_state["confirm_delete_selected"] = None
                st.rerun()

    # 페이지네이션 설정
    items_per_page = 10
    total_pages = (len(articles) - 1) // items_per_page + 1

    if "pagination_page" not in st.session_state or not isinstance(
        st.session_state["pagination_page"], int
    ):
        st.session_state["pagination_page"] = 1

    # 범위 보정
    if st.session_state["pagination_page"] < 1:
        st.session_state["pagination_page"] = 1
    if st.session_state["pagination_page"] > total_pages:
        st.session_state["pagination_page"] = total_pages

    start_idx = (st.session_state["pagination_page"] - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_articles = articles[start_idx:end_idx]

    # 목록 요약
    st.markdown(
        f"**총 {len(articles)}개 기사 중 {start_idx + 1}-{min(end_idx, len(articles))}개 표시**"
    )

    # 기사 리스트 (체크박스 → 제목 → 즐겨찾기)
    for idx, article in enumerate(current_articles):
        article_id = article.get("id", "")
        is_fav = article.get("is_favorite", False)
        emoji_cat = get_category_emoji(article.get("category", ""))
        star_icon = "⭐" if is_fav else "☆"

        title = article.get("title", "제목 없음")
        url = article.get("url", article.get("link", "#"))
        collected_at = (article.get("collected_at") or "")[:10]
        publisher = article.get("publisher")
        category = article.get("category", "")

        meta_parts: List[str] = []
        if collected_at:
            meta_parts.append(f"📅 {collected_at}")
        if publisher and publisher != "N/A":
            meta_parts.append(str(publisher))
        if category and category != "N/A":
            meta_parts.append(str(category))
        meta_text = " | ".join(meta_parts)

        col_check, col_title, col_star = st.columns([0.06, 0.86, 0.08])

        with col_check:
            st.checkbox("", key=f"select_{article_id}", label_visibility="collapsed")

        with col_title:
            title_html = f"<strong>[{emoji_cat} {category}] {title}</strong>"
            if meta_text:
                title_html += (
                    f"<br><span style='color:#888;font-size:0.85em;'>{meta_text}</span>"
                )
            st.markdown(
                f"<a href='{url}' target='_blank' style='text-decoration:none;color:inherit;'>{title_html}</a>",
                unsafe_allow_html=True,
            )

        with col_star:
            if st.button(
                star_icon,
                key=f"fav_{article_id}",
                help="즐겨찾기 토글",
                type="secondary",
            ):
                toggle_favorite(article_id)
                st.rerun()

        # 기사 간 구분선
        if idx < len(current_articles) - 1:
            st.markdown(
                "<hr style='border:none;border-top:1px solid #e5e7eb;margin:0.25rem 0;' />",
                unsafe_allow_html=True,
            )

    # 페이지네이션 버튼 (숫자만 표시, << >> 버튼 제거)
    if total_pages > 1:
        st.write("---")

        page_cols = st.columns(total_pages)
        for i in range(1, total_pages + 1):
            with page_cols[i - 1]:
                btn_type = (
                    "primary" if st.session_state["pagination_page"] == i else "secondary"
                )
                if st.button(str(i), key=f"page_{i}", type=btn_type):
                    st.session_state["pagination_page"] = i
                    st.rerun()


# main.py 에서 사용하기 위한 별칭
render_home_page = render_home
