    # 목록 표시
    st.markdown(f"**총 {len(articles)}개 기사 중 {start_idx+1}-{min(end_idx, len(articles))}개 표시**")
    
    # 기사 하나를 하나의 블럭처럼 보이도록 정리
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

        meta_parts = []
        if collected_at:
            meta_parts.append(f"📅 {collected_at}")
        if publisher and publisher != "N/A":
            meta_parts.append(publisher)
        if category and category != "N/A":
            meta_parts.append(category)
        meta_text = " | ".join(meta_parts)

        # [체크박스] -> [제목/메타] -> [즐겨찾기] 순서로 배치
        col_check, col_title, col_star = st.columns([0.06, 0.86, 0.08])

        with col_check:
            st.checkbox("", key=f"select_{article_id}", label_visibility="collapsed")

        with col_title:
            text = f"**[{emoji_cat} {category}] {title}**"
            if meta_text:
                text += f"<br><span style='color:#888;font-size:0.85em;'>{meta_text}</span>"
            st.markdown(
                f"<a href='{url}' target='_blank' style='text-decoration:none;color:inherit;'>{text}</a>",
                unsafe_allow_html=True,
            )

        with col_star:
            if st.button(star_icon, key=f"fav_{article_id}", help="즐겨찾기 토글", type="secondary"):
                from app.services.news_service import toggle_favorite
                toggle_favorite(article_id)
                st.rerun()

        # 기사 간 구분선
        if idx < len(current_articles) - 1:
            st.markdown("<hr style='border:none;border-top:1px solid #e5e7eb;margin:0.25rem 0;' />", unsafe_allow_html=True)
    Args:
        articles: 기사 리스트
        
    Returns:
        표시용 포맷 리스트
    """
    display_data = []
    for article in articles:
        display_data.append({
            "id": article.get("id", ""),
            "title": article.get("title", ""),
            "category": article.get("category", ""),
            "url": article.get("url", ""),
            "emoji": get_category_emoji(article.get("category", "")),
            "collected_at": article.get("collected_at", ""),
        })
    return display_data


def group_by_category(
    articles: list[dict[str, Any]]
) -> dict[str, list[dict[str, Any]]]:
    """기사를 카테고리별로 그룹화한다.
    
    Args:
        articles: 기사 리스트
        
    Returns:
        카테고리별 기사 딕셔너리
    """
    grouped: dict[str, list[dict[str, Any]]] = {}
    
    for article in articles:
        category = article.get("category", "기타")
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(article)
    
    return grouped


            st.markdown(f"**총 {len(articles)}개 기사 중 {start_idx + 1}-{min(end_idx, len(articles))}개 표시**")
    """뉴스가 없을 때 표시할 메시지를 반환한다.
    
    Returns:
        빈 상태 메시지
    """
    empty_emoji = get_emoji("empty")
    return f"{empty_emoji} 수집된 뉴스가 없습니다. 카테고리를 선택하고 수집 버튼을 눌러주세요."


def get_loading_message() -> str:
    """로딩 중 메시지를 반환한다.
    
    Returns:
        로딩 메시지
    """
    loading_emoji = get_emoji("loading")
    return f"{loading_emoji} 뉴스를 수집하고 있습니다..."


def get_error_message(error: str) -> str:
    """에러 메시지를 포맷한다.
    
    Args:
        error: 에러 내용
        
    Returns:
        포맷된 에러 메시지
    """
    error_emoji = get_emoji("error")
    return f"{error_emoji} 오류가 발생했습니다: {error}"


def get_success_message(count: int) -> str:
    """수집 성공 메시지를 반환한다.
    
    Args:
        count: 수집된 기사 수
        
    Returns:
        성공 메시지
    """
    success_emoji = get_emoji("success")
    return f"{success_emoji} {count}개의 뉴스가 수집되었습니다."


def render_home() -> None:
    """홈 페이지를 렌더링한다.
    
    Streamlit 컨텍스트에서 호출되어야 한다.
    """
    import streamlit as st
    from app.services.news_service import NewsService
    from app.ui.theme.styles import get_glassmorphism_css
    
    # 스타일 적용
    st.markdown(get_glassmorphism_css(), unsafe_allow_html=True)
    
    st.subheader(f"{get_emoji('newspaper')} 뉴스 수집")
    
    # 페이지 설명 추가
    st.markdown(f"""
    <div class="info-section">
        네이버의 최신 뉴스를 카테고리별로 실시간 수집하고 관리할 수 있습니다.<br>
        중요한 기사는 별점({get_emoji('star')})을 눌러 저장하고, 필요 없는 기사는 체크박스로 선택하여 한꺼번에 삭제하세요.
    </div>
    """, unsafe_allow_html=True)
    
    # 상단 드롭다운 및 수집 컨트롤
    with st.container():
        col_select, col_btn = st.columns([3, 1])
        with col_select:
            # 카테고리 선택 (드롭다운 방식)
            selected_category = st.selectbox(
                "카테고리 선택",
                options=["전체"] + CATEGORIES,
                index=0,
                key="home_category_selector"
            )
            
            # 카테고리 변경 시 페이지 초기화
            if "prev_category" not in st.session_state or st.session_state["prev_category"] != selected_category:
                st.session_state["pagination_page"] = 1
                st.session_state["prev_category"] = selected_category
        
        with col_btn:
            st.write(" ") # 수직 정렬용
            collect_trigger = st.button(
                f"{get_emoji('collect')} 뉴스 수집",
                use_container_width=True,
                type="primary"
            )
    
    # 뉴스 서비스
    service = NewsService()
    
    # 수집 실행
    if collect_trigger:
        categories_to_collect = CATEGORIES if selected_category == "전체" else [selected_category]
        with st.spinner(get_loading_message()):
            try:
                collected = service.collect_news(categories_to_collect)
                total = sum(len(articles) for articles in collected.values())
                st.toast(get_success_message(total))
                st.rerun()
            except Exception as e:
                st.error(get_error_message(str(e)))
    
    # 기사 목록 로드 및 필터링
    all_articles = service.load_articles()
    if selected_category != "전체":
        articles = [a for a in all_articles if a.get("category") == selected_category]
    else:
        articles = all_articles
    
    if not articles:
        st.info(get_empty_state_message())
        return

    # ─────────────────────────────────────────────────────
    # 대량 삭제 및 선택 관리 (Task 4)
    # ─────────────────────────────────────────────────────
    st.write("---")
    col_sel1, col_sel2, col_sel3 = st.columns([2, 2, 6])
    
    with col_sel1:
        # 요청: ":check 전체선택" → 단순 "전체선택" 텍스트로 변경
        if st.button("전체선택", use_container_width=True):
            for a in articles:
                st.session_state[f"select_{a['id']}"] = True
            st.rerun()
            
    with col_sel2:
        if st.button(f"{get_emoji('delete')} 선택 삭제", use_container_width=True, type="secondary"):
            selected_ids = [a["id"] for a in articles if st.session_state.get(f"select_{a['id']}")]
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
                from app.services.news_service import delete_selected_articles
                result = delete_selected_articles(ids_to_del)
                st.toast(f"✅ {result['deleted_count']}개의 기사가 삭제되었습니다.")
                # 세션 상태 정리
                for aid in ids_to_del:
                    if f"select_{aid}" in st.session_state:
                        del st.session_state[f"select_{aid}"]
                st.session_state["confirm_delete_selected"] = None
                st.rerun()
        with col_c2:
            if st.button("❌ 취소", key="confirm_bulk_no"):
                st.session_state["confirm_delete_selected"] = None
                st.rerun()

    # 페이지네이션 설정
    items_per_page = 10
    total_pages = (len(articles) - 1) // items_per_page + 1
    
    if "pagination_page" not in st.session_state or not isinstance(st.session_state["pagination_page"], int):
        st.session_state["pagination_page"] = 1
        
    # 페이지 범위 계산
    start_idx = (st.session_state["pagination_page"] - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_articles = articles[start_idx:end_idx]
    
    # 목록 표시
    st.markdown(f"**총 {len(articles)}개 기사 중 {start_idx+1}-{min(end_idx, len(articles))}개 표시**")
    
    # 기사 하나를 하나의 블럭처럼 보이도록 간단한 행 레이아웃으로 정리
    for article in current_articles:
        article_id = article.get("id", "")
        is_fav = article.get("is_favorite", False)
        emoji_cat = get_category_emoji(article.get("category", ""))
        star_icon = "⭐" if is_fav else "☆"

        title = article.get("title", "제목 없음")
        url = article.get("url", article.get("link", "#"))
        collected_at = (article.get("collected_at") or "")[:10]
        publisher = article.get("publisher")

        # [체크박스] [즐겨찾기] [제목/메타] 한 줄로 배치해 하나의 블럭처럼 보이게 구성
        row_c1, row_c2, row_c3 = st.columns([0.06, 0.06, 0.88])

        with row_c1:
            st.checkbox("", key=f"select_{article_id}", label_visibility="collapsed")

        with row_c2:
            if st.button(star_icon, key=f"fav_{article_id}", help="즐겨찾기 토글"):
                from app.services.news_service import toggle_favorite
                toggle_favorite(article_id)
                st.rerun()

        with row_c3:
            meta_parts = []
            if collected_at:
                meta_parts.append(f"📅 {collected_at}")
            if publisher and publisher != "N/A":
                meta_parts.append(publisher)
            meta_text = " | ".join(meta_parts) if meta_parts else ""

            st.markdown(
                f"**[{emoji_cat} {article.get('category', '')}]** "
                f"[ {title} ]({url})  "
                + (f"  \\n+                <span style='color:#888;font-size:0.85em;'>{meta_text}</span>" if meta_text else ""),
                unsafe_allow_html=True,
            )

    # 페이지네이션 버튼
    st.write("---")
    cols = st.columns(len(range(1, total_pages + 1)) + 2)
    with cols[0]:
        if st.button("<<", disabled=(st.session_state["pagination_page"] == 1)):
            st.session_state["pagination_page"] = 1
            st.rerun()
            
    for i in range(1, total_pages + 1):
        with cols[i]:
            btn_type = "primary" if st.session_state["pagination_page"] == i else "secondary"
            if st.button(str(i), key=f"page_{i}", type=btn_type):
                st.session_state["pagination_page"] = i
                st.rerun()
                
    with cols[-1]:
        if st.button(">>", disabled=(st.session_state["pagination_page"] == total_pages)):
            st.session_state["pagination_page"] = total_pages
            st.rerun()


# Alias for backwards compatibility and main.py import
render_home_page = render_home
