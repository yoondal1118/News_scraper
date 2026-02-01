"""이모지 헬퍼 모듈.

emoji 라이브러리를 사용하여 윈도우 기본 이모지 대신 일관된 이모지를 제공한다.
헌법 규칙: 윈도우 기본 이모지 이미지 사용 금지
"""

import emoji


def get_emoji(name: str) -> str:
    """이름으로 이모지를 반환한다.
    
    Args:
        name: 이모지 이름 (예: "newspaper", "calendar", "memo")
        
    Returns:
        해당 이모지 문자열
    """
    emoji_map = {
        # 뉴스 관련
        "newspaper": ":newspaper:",
        "news": ":rolled_up_newspaper:",
        "world": ":globe_showing_Americas:",
        
        # 카테고리
        "politics": ":classical_building:",
        "economy": ":chart_increasing:",
        "society": ":people_holding_hands:",
        "culture": ":performing_arts:",
        "it_science": ":robot:",
        "world_news": ":globe_with_meridians:",
        
        # 상태
        "success": ":check_mark_button:",
        "error": ":cross_mark:",
        "warning": ":warning:",
        "loading": ":hourglass_flowing_sand:",
        "empty": ":package:",
        
        # 액션
        "collect": ":inbox_tray:",
        "save": ":floppy_disk:",
        "share": ":link:",
        "copy": ":clipboard:",
        "edit": ":pencil:",
        "delete": ":wastebasket:",
        "add": ":plus:",
        
        # 캘린더
        "calendar": ":calendar:",
        "date": ":spiral_calendar:",
        "today": ":pushpin:",
        
        # 다이어리
        "diary": ":notebook:",
        "memo": ":memo:",
        "opinion": ":thought_balloon:",
        "summary": ":page_facing_up:",
        
        # UI
        "home": ":house:",
        "back": ":left_arrow:",
        "forward": ":right_arrow:",
        "refresh": ":counterclockwise_arrows_button:",
        "settings": ":gear:",
        "info": ":information:",
        "star": ":star:",
        "link": ":link:",
    }
    
    shortcode = emoji_map.get(name, f":{name}:")
    return emoji.emojize(shortcode, language="alias")


def get_category_emoji(category: str) -> str:
    """카테고리에 해당하는 이모지를 반환한다.
    
    Args:
        category: 뉴스 카테고리 (정치, 경제, 사회, 생활/문화, IT/과학, 세계)
        
    Returns:
        카테고리 이모지
    """
    category_emoji_map = {
        "정치": get_emoji("politics"),
        "경제": get_emoji("economy"),
        "사회": get_emoji("society"),
        "생활/문화": get_emoji("culture"),
        "IT/과학": get_emoji("it_science"),
        "세계": get_emoji("world_news"),
    }
    return category_emoji_map.get(category, get_emoji("newspaper"))


def get_status_emoji(status: str) -> str:
    """상태에 해당하는 이모지를 반환한다.
    
    Args:
        status: 상태 (success, error, loading, empty, warning)
        
    Returns:
        상태 이모지
    """
    return get_emoji(status)
