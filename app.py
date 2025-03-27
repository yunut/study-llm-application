import streamlit as st
from dotenv import load_dotenv
from llm import get_ai_response

load_dotenv()

st.set_page_config(
    page_title="소득세 챗봇",
    page_icon=":robot:",
)

st.title(":shark: 소득세 챗봇 :shark:")
st.caption("소득세 관련 질문에 답해드립니다.")

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_question := st.chat_input(placeholder="소득세 관련 질문을 입력하세요"):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})
        
    with st.spinner("답변을 생각하고 있어요..."):
        response = get_ai_response(user_question)
        print(response)
        with st.chat_message("ai"):
            ai_message = st.write_stream(response)
            st.session_state.messages.append({"role": "ai", "content": ai_message}) 