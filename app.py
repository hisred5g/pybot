from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
SYSTEM_PROMPT = "너는 파이썬 개발자야. 코딩에 관련된 질문에 5줄 이내로 대답하지."

st.title("파이썬 가이드 챗봇")

if "history" not in st.session_state:
    st.session_state["history"] = []

if st.button("대화 초기화") :
    st.session_state["history"] = []
    st.rerun()
    
user_input = st.text_input("메세지를 입력하세요:", key="user_input")

if st.button("답변 받기") :
    history_text = ""
    for m in st.session_state["history"]:
        role = "사용자" if m["role"] == "user" else "AI"
        history_text += f"{role}: {m['content']}\n"

    contents = (
        f"[시스템]\n{SYSTEM_PROMPT}\n\n"
        f"[대화]\n{history_text}사용자: {user_input}\nAI:"
    )

    try :
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.7, 
            ),
        )
        answer = getattr(resp, "text", "") or "(빈 응답)"
    except Exception as e:
        answer = f"오류발생 {e}"

    st.session_state["history"].append({"role": "user", "content": user_input})
    st.session_state["history"].append({"role": "assistant", "content": answer})

for m in st.session_state["history"] :
    if m["role"] == "user":
        st.markdown(f"<div style='text-align:right; background-color:#e0f7fa; padding:8px; border-radius:10px; margin-bottom:5px; display:inline-block'>{m['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:left; background-color:#f1f8e9; padding:8px; border-radius:10px; margin-bottom:5px; display:inline-block'>{m['content']}</div>", unsafe_allow_html=True)