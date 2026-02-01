"""뉴스 카드 UI 컴포넌트.

뉴스 기사를 블록 형태로 표시하는 컴포넌트.
"""

from typing import Any, Callable
import streamlit as st
from app.ui.components.emoji_helper import get_category_emoji
from app.ui.theme.styles import get_category_colors


def render_news_card(article: dict[str, Any]) -> None:
    """뉴스 카드를 렌더링한다.
    
    Args:
        article: 뉴스 기사 데이터
    """
    category = article.get("category", "")
    title = article.get("title", "")
    url = article.get("url", "")
    article_id = article.get("id", "")
    emoji = get_category_emoji(category)
    colors = get_category_colors()
    bg_color = colors.get(category, "rgba(255, 255, 255, 0.1)")
    
    # 카드 HTML
    card_html = f"""
    <div class="news-block" style="background: {bg_color};">
        <span style="margin-right: 8px;">{emoji}</span>
        <span class="high-contrast-text">{title}</span>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def render_news_list(
    articles: list[dict[str, Any]],
    on_click_callback: Callable[[dict[str, Any]], None] | None = None,
) -> None:
    """뉴스 리스트를 렌더링한다.
    
    Args:
        articles: 뉴스 기사 리스트
        on_click_callback: 기사 클릭 시 콜백 함수
    """
    for article in articles:
        col1, col2 = st.columns([5, 1])
        
        with col1:
            render_news_card(article)
        
        with col2:
            if st.button("상세", key=f"card_{article.get('id', '')}"):
                if on_click_callback:
                    on_click_callback(article)
                else:
                    st.session_state["selected_article"] = article.get("id")


def render_category_section(
    category: str,
    articles: list[dict[str, Any]],
    expanded: bool = True,
) -> None:
    """카테고리 섹션을 렌더링한다.
    
    Args:
        category: 카테고리명
        articles: 해당 카테고리의 기사 리스트
        expanded: 확장 여부
    """
    emoji = get_category_emoji(category)
    
    with st.expander(f"{emoji} {category} ({len(articles)}개)", expanded=expanded):
        if not articles:
            st.info("해당 카테고리에 뉴스가 없습니다.")
        else:
            render_news_list(articles)
