# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import random
import string
from app.services.user_service import UserService

def show_alert(message):
    """
    브라우저 alert 창을 띄웁니다.
    height=0, width=0으로 설정하여 레이아웃에 영향을 주지 않습니다.
    """
    # 메시지 내 따옴표 처리
    safe_message = str(message).replace('"', '\\"').replace("'", "\\'")
    components.html(f'<script>alert("{safe_message}");</script>', height=0, width=0)

def render_login_page():
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"
    
    # 알림 메시지 처리
    if "alert_msg" not in st.session_state:
        st.session_state["alert_msg"] = None
    
    if st.session_state["alert_msg"]:
        show_alert(st.session_state["alert_msg"])
        st.session_state["alert_msg"] = None

    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        mode = st.session_state["auth_mode"]
        if mode == "login":
            _render_login()
        elif mode == "register":
            _render_register()
        elif mode == "forgot_password":
            _render_forgot_password()

def _render_login():
    st.subheader("로그인")
    username = st.text_input("아이디", key="login_username")
    password = st.text_input("비밀번호", type="password", key="login_password")
    
    if st.button("로그인", use_container_width=True, type="primary"):
        if not username or not password:
            st.error("아이디와 비밀번호를 입력해주세요.")
            return
            
        success, message = UserService.login(username, password)
        if success:
            st.session_state["user"] = username
            st.session_state["active_tab"] = "뉴스 수집"
            st.toast(f"{username}님, 환영합니다!")
            st.rerun()
        else:
            st.error(message)
            
    col1, col2 = st.columns(2)
    with col1:
        if st.button("회원가입", use_container_width=True):
            st.session_state["auth_mode"] = "register"
            st.rerun()
    with col2:
        if st.button("비밀번호 찾기", use_container_width=True):
            st.session_state["auth_mode"] = "forgot_password"
            st.rerun()

def handle_check_id():
    username = st.session_state.get("reg_username", "")
    if not username:
        st.session_state["alert_msg"] = "아이디를 입력해주세요."
        return
    
    available, message = UserService.check_id_availability(username)
    st.session_state["reg_id_available"] = available
    st.session_state["alert_msg"] = message

def handle_send_code():
    email = st.session_state.get("reg_email", "")
    if not email or "@" not in email:
        st.session_state["alert_msg"] = "유효한 이메일을 입력해주세요."
        return
    
    code = "".join(random.choices(string.digits, k=6))
    success, message = UserService.send_verification_email(email, code)
    if success:
        st.session_state["reg_verification_code"] = code
        st.session_state["alert_msg"] = f"인증 코드가 발송되었습니다. ({email})"
    else:
        st.session_state["alert_msg"] = message

def handle_verify_code():
    input_code = st.session_state.get("reg_code_input", "")
    target_code = st.session_state.get("reg_verification_code", "")
    
    if input_code == target_code and target_code:
        st.session_state["reg_email_verified"] = True
        st.session_state["alert_msg"] = "이메일 인증이 완료되었습니다."
    else:
        st.session_state["alert_msg"] = "인증 코드가 일치하지 않습니다."

def _render_register():
    st.subheader("회원가입")
    
    if "reg_id_available" not in st.session_state:
        st.session_state["reg_id_available"] = False
    if "reg_email_verified" not in st.session_state:
        st.session_state["reg_email_verified"] = False

    # 아이디 입력 및 중복 확인
    i_col1, i_col2 = st.columns([3, 1])
    with i_col1:
        st.text_input("아이디", key="reg_username")
    with i_col2:
        st.markdown('<div style="padding-top:28px"></div>', unsafe_allow_html=True)
        st.button("중복확인", use_container_width=True, on_click=handle_check_id)
        
    # 이메일 입력 및 코드 발송
    e_col1, e_col2 = st.columns([3, 1])
    with e_col1:
        st.text_input("이메일", key="reg_email")
    with e_col2:
        st.markdown('<div style="padding-top:28px"></div>', unsafe_allow_html=True)
        st.button("코드발송", use_container_width=True, on_click=handle_send_code)
        
    # 이메일 인증 코드 입력
    if "reg_verification_code" in st.session_state and not st.session_state["reg_email_verified"]:
        c_col1, c_col2 = st.columns([3, 1])
        with c_col1:
            st.text_input("인증코드 입력", key="reg_code_input")
        with c_col2:
            st.markdown('<div style="padding-top:28px"></div>', unsafe_allow_html=True)
            st.button("확인", use_container_width=True, on_click=handle_verify_code)
    elif st.session_state["reg_email_verified"]:
        st.success("✅ 이메일 인증 완료")
        
    password = st.text_input("비밀번호", type="password", key="reg_password")
    password_conf = st.text_input("비밀번호 확인", type="password", key="reg_password_conf")
    
    if st.button("가입하기", use_container_width=True, type="primary"):
        if not st.session_state.get("reg_username"):
            st.session_state["alert_msg"] = "아이디를 입력해주세요."
        elif not st.session_state.get("reg_id_available"):
            st.session_state["alert_msg"] = "아이디 중복확인을 해주세요."
        elif not st.session_state.get("reg_email_verified"):
            st.session_state["alert_msg"] = "이메일 인증을 해주세요."
        elif not password or not password_conf:
            st.session_state["alert_msg"] = "비밀번호를 입력해주세요."
        elif password != password_conf:
            st.session_state["alert_msg"] = "비밀번호가 일치하지 않습니다."
        elif len(password) < 4:
            st.session_state["alert_msg"] = "비밀번호는 4자 이상이어야 합니다."
        else:
            success, message = UserService.register(
                st.session_state.reg_username, 
                password, 
                st.session_state.reg_email
            )
            if success:
                st.session_state["alert_msg"] = "회원가입이 완료되었습니다! 로그인해주세요."
                st.session_state["auth_mode"] = "login"
            else:
                st.session_state["alert_msg"] = message
        st.rerun()
                
    if st.button("로그인으로 돌아가기", use_container_width=True):
        st.session_state["auth_mode"] = "login"
        st.rerun()

def _render_forgot_password():
    st.subheader("비밀번호 찾기")
    
    if "reset_step" not in st.session_state:
        st.session_state["reset_step"] = 1
        
    if st.session_state["reset_step"] == 1:
        email = st.text_input("가입한 이메일 입력", key="forgot_email")
        if st.button("인증 코드 발송", use_container_width=True, type="primary"):
            username = UserService.get_username_by_email(email)
            if username:
                code = "".join(random.choices(string.digits, k=6))
                success, message = UserService.send_verification_email(email, code)
                if success:
                    UserService.set_reset_code(username, code)
                    st.session_state["reset_username"] = username
                    st.session_state["reset_step"] = 2
                    st.session_state["alert_msg"] = f"인증 코드를 발송했습니다. ({email})"
                    st.rerun()
                else:
                    st.session_state["alert_msg"] = message
                    st.rerun()
            else:
                st.session_state["alert_msg"] = "해당 이메일로 가입된 사용자를 찾을 수 없습니다."
                st.rerun()
                
    elif st.session_state["reset_step"] == 2:
        st.info(f"사용자 아이디: {st.session_state['reset_username']}")
        input_code = st.text_input("인증 코드 6자리 입력", key="reset_code_input")
        new_pw = st.text_input("새 비밀번호", type="password", key="reset_new_password")
        new_pw_conf = st.text_input("새 비밀번호 확인", type="password", key="reset_new_password_conf")
        
        if st.button("비밀번호 변경", use_container_width=True, type="primary"):
            if new_pw != new_pw_conf:
                st.session_state["alert_msg"] = "비밀번호가 일치하지 않습니다."
            elif len(new_pw) < 4:
                st.session_state["alert_msg"] = "비밀번호는 4자 이상이어야 합니다."
            else:
                success, message = UserService.verify_and_reset_password(
                    st.session_state["reset_username"], 
                    input_code, 
                    new_pw
                )
                if success:
                    st.session_state["alert_msg"] = "비밀번호가 성공적으로 변경되었습니다."
                    st.session_state["reset_step"] = 1
                    st.session_state["auth_mode"] = "login"
                    st.rerun()
                else:
                    st.session_state["alert_msg"] = message
                    st.rerun()
                    
    if st.button("로그인으로 돌아가기", use_container_width=True):
        st.session_state["auth_mode"] = "login"
        st.session_state["reset_step"] = 1
        st.rerun()

if __name__ == "__main__":
    render_login_page()
