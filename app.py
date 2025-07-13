# app.py
import streamlit as st

# 페이지 제목
st.title("인간공학적 위험성평가 도구")

# 기본 내용
st.write("이 앱이 보이면 Streamlit이 정상 작동합니다!")

# 간단한 입력 테스트
name = st.text_input("이름을 입력하세요:")
if name:
    st.write(f"안녕하세요, {name}님!")

# 버튼 테스트
if st.button("클릭하세요"):
    st.balloons()
    st.success("버튼이 작동합니다!")
