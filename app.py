import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
LANGUAGES = {
    "영어": "English",
    "일본어": "Japanese",
    "베트남어": "Vietnamese",
}

st.set_page_config(page_title="번역기", page_icon="🌐")
st.title("🌐 간단 번역기")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error(".env 파일에 OPENAI_API_KEY가 설정되어 있지 않습니다.")
    st.stop()

client = OpenAI(api_key=api_key)

text = st.text_area("번역할 글을 입력하세요", height=200)
target = st.radio("번역할 언어", list(LANGUAGES), horizontal=True)

if st.button("번역하기", type="primary"):
    if not text.strip():
        st.warning("번역할 글을 입력해 주세요.")
    else:
        with st.spinner("번역 중..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                f"You are a professional translator. Translate the user's text "
                                f"into natural {LANGUAGES[target]}. Output only the translation."
                            ),
                        },
                        {"role": "user", "content": text},
                    ],
                )
                st.subheader(f"{target} 번역 결과")
                st.text_area("결과", response.choices[0].message.content, height=200)
            except Exception as e:
                st.error(f"번역 중 오류가 발생했습니다: {e}")
