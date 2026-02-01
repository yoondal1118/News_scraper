"""공유 버튼 컴포넌트 모듈.

다이어리 요약을 클립보드로 복사하는 기능을 제공한다.
"""

from typing import Any
import streamlit as st
from app.ui.components.emoji_helper import get_emoji


def format_for_clipboard(entry: dict[str, Any]) -> str:
    """다이어리 엔트리를 클립보드용 텍스트로 포맷한다.
    
    Args:
        entry: 다이어리 엔트리 데이터
        
    Returns:
        클립보드에 복사할 포맷된 텍스트
    """
    title = entry.get("article_title", "뉴스 기사")
    summary = entry.get("summary", "")
    opinion = entry.get("opinion", "")
    
    if not summary and not opinion:
        return f"📰 {title}\n\n(내용 없음)"
    
    parts = [f"📰 {title}"]
    
    if summary:
        parts.append(f"\n📝 요약:\n{summary}")
    
    if opinion:
        parts.append(f"\n💭 의견:\n{opinion}")
    
    parts.append(f"\n\n---\n네이버 뉴스 다이어리로 작성됨")
    
    return "\n".join(parts)


def get_clipboard_js(text: str) -> str:
    """클립보드 복사용 JavaScript 코드를 생성한다.
    
    Args:
        text: 복사할 텍스트
        
    Returns:
        JavaScript 코드 문자열
    """
    # 텍스트 이스케이프
    escaped_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    
    return f"""
    <script>
    function copyToClipboard() {{
        const text = `{escaped_text}`;
        if (navigator.clipboard && navigator.clipboard.writeText) {{
            navigator.clipboard.writeText(text).then(function() {{
                alert('클립보드에 복사되었습니다!');
            }}).catch(function(err) {{
                fallbackCopy(text);
            }});
        }} else {{
            fallbackCopy(text);
        }}
    }}
    
    function fallbackCopy(text) {{
        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.left = "-9999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {{
            document.execCommand('copy');
            alert('클립보드에 복사되었습니다!');
        }} catch (err) {{
            alert('복사에 실패했습니다. 직접 텍스트를 선택해 복사해주세요.');
        }}
        document.body.removeChild(textArea);
    }}
    </script>
    """


def copy_to_clipboard(text: str) -> None:
    """텍스트를 클립보드에 복사한다.
    
    Streamlit 컨텍스트에서 호출되어야 한다.
    
    Args:
        text: 복사할 텍스트
    """
    js_code = get_clipboard_js(text)
    
    # Streamlit에 JavaScript 삽입
    st.components.v1.html(
        f"""
        {js_code}
        <button onclick="copyToClipboard()" style="
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            padding: 8px 16px;
            cursor: pointer;
            font-size: 14px;
        ">
            {get_emoji('copy')} 클립보드에 복사
        </button>
        """,
        height=50,
    )


def render_share_button(entry: dict[str, Any]) -> None:
    """공유 버튼을 렌더링한다.
    
    Args:
        entry: 다이어리 엔트리 데이터
    """
    formatted_text = format_for_clipboard(entry)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button(f"{get_emoji('share')} 공유"):
            st.session_state["copy_text"] = formatted_text
            st.success(f"{get_emoji('success')} 아래 버튼으로 클립보드에 복사하세요!")
    
    if "copy_text" in st.session_state:
        copy_to_clipboard(st.session_state["copy_text"])
