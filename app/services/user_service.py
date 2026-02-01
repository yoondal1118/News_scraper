"""사용자 관리 및 인증 서비스 모듈.

회원가입, 로그인, 비밀번호 찾기 및 사용자 데이터를 관리한다.
"""

import json
import os
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime
import streamlit as st

# 프로젝트 루트 기준 data 폴더 경로
DATA_DIR = Path(__file__).parent.parent.parent / "data"
USERS_FILE = DATA_DIR / "users.json"

def ensure_user_storage() -> None:
    """사용자 데이터 디렉토리와 파일을 생성한다."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

def hash_password(password: str) -> str:
    """비밀번호를 해싱한다."""
    return hashlib.sha256(password.encode()).hexdigest()

class UserService:
    """사용자 관리 서비스."""

    @staticmethod
    def _load_users() -> Dict[str, Any]:
        ensure_user_storage()
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    @staticmethod
    def _save_users(users: Dict[str, Any]) -> bool:
        ensure_user_storage()
        try:
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False

    @classmethod
    def register(cls, username: str, password: str, email: str) -> tuple[bool, str]:
        """회원가입을 처리한다."""
        users = cls._load_users()
        if username in users:
            return False, "이미 존재하는 아이디입니다."
        
        users[username] = {
            "password": hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "reset_code": None,
            "is_verified": False
        }
        
        if cls._save_users(users):
            # 사용자 전용 폴더 생성
            user_data_path = DATA_DIR / username
            user_data_path.mkdir(parents=True, exist_ok=True)
            return True, "회원가입 성공!"
        return False, "저장 중 오류가 발생했습니다."

    @classmethod
    def check_id_availability(cls, username: str) -> tuple[bool, str]:
        """아이디 중복 여부를 확인한다."""
        if not username:
            return False, "아이디를 입력해주세요."
        users = cls._load_users()
        if username in users:
            return False, "이미 사용 중인 아이디입니다."
        return True, "사용 가능한 아이디입니다."

    @classmethod
    def get_username_by_email(cls, email: str) -> Optional[str]:
        """이메일로 아이디를 조회한다."""
        users = cls._load_users()
        for uname, info in users.items():
            if info.get("email") == email:
                return uname
        return None

    @classmethod
    def login(cls, username: str, password: str) -> tuple[bool, str]:
        """로그인을 처리한다."""
        users = cls._load_users()
        user = users.get(username)
        if not user:
            return False, "존재하지 않는 아이디입니다."
        
        if user["password"] == hash_password(password):
            return True, "로그인 성공!"
        return False, "비밀번호가 일치하지 않습니다."

    @classmethod
    def get_user_email(cls, username: str) -> Optional[str]:
        """사용자의 이메일을 가져온다."""
        users = cls._load_users()
        user = users.get(username)
        return user["email"] if user else None

    @classmethod
    def set_reset_code(cls, username: str, code: str) -> bool:
        """비밀번호 재설정 코드를 저장한다."""
        users = cls._load_users()
        if username in users:
            users[username]["reset_code"] = code
            return cls._save_users(users)
        return False

    @classmethod
    def verify_and_reset_password(cls, username: str, code: str, new_password: str) -> tuple[bool, str]:
        """코드를 확인하고 비밀번호를 변경한다."""
        users = cls._load_users()
        user = users.get(username)
        if not user or user.get("reset_code") != code:
            return False, "인증 코드가 일치하지 않거나 사용자를 찾을 수 없습니다."
        
        user["password"] = hash_password(new_password)
        user["reset_code"] = None # 코드 사용 후 제거
        if cls._save_users(users):
            return True, "비밀번호가 성공적으로 변경되었습니다."
        return False, "저장 중 오류가 발생했습니다."

    @staticmethod
    def send_verification_email(to_email: str, code: str) -> tuple[bool, str]:
        """실제 SMTP를 사용하여 인증 코드를 발송한다."""
        try:
            # st.secrets 접근 방식 최적화 (Streamlit Cloud 대응)
            try:
                smtp_config = st.secrets["smtp"]
                server = smtp_config["server"]
                port = smtp_config["port"]
                user = smtp_config["user"]
                password = smtp_config["password"]
            except KeyError:
                return False, "SMTP 설정이 누락되었습니다. (Streamlit Cloud Secrets 설정을 확인하세요)"

            if not all([server, port, user, password]):
                return False, "SMTP 설정값이 비어있습니다."

            msg = MIMEMultipart()
            # RFC-5322 준수를 위해 헤더 인코딩 처리
            display_name = str(Header('네이버 뉴스 다이어리', 'utf-8'))
            msg['From'] = formataddr((display_name, user))
            msg['To'] = to_email
            msg['Subject'] = Header("[네이버 뉴스 다이어리] 이메일 인증 코드", 'utf-8')

            body = f"""
            안녕하세요, 네이버 뉴스 다이어리입니다.
            
            요청하신 이메일 인증 코드는 다음과 같습니다:
            
            [{code}]
            
            해당 코드를 인증창에 입력해 주세요.
            감사합니다.
            """
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP_SSL(server, port) as smtp:
                smtp.login(user, password)
                smtp.send_message(msg)

            return True, "이메일이 발송되었습니다."
        except Exception as e:
            return False, f"이메일 발송 실패: {str(e)}"
