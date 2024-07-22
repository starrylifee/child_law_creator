import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
from PIL import Image
import io

hide_github_icon = """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK{ display: none; }
    #MainMenu{ visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
"""

st.markdown(hide_github_icon, unsafe_allow_html=True)

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 gemini_api_key1 값 가져오기
gemini_api_key1 = secrets["gemini_api_key1"]

# Gemini API 키 설정
genai.configure(api_key=gemini_api_key1)

# 핸드폰 사진 업로드 기능 추가
uploaded_file = st.file_uploader("핸드폰 사진 업로드")

# 이미지가 업로드되었는지 확인
if uploaded_file is not None:
    with st.spinner("이미지를 분석중입니다. 잠시만 기다려주세요..."):
        # 이미지 바이트 문자열로 변환
        img_bytes = uploaded_file.read()

        # bytes 타입의 이미지 데이터를 PIL.Image.Image 객체로 변환
        img = Image.open(io.BytesIO(img_bytes))

        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate content
        response = model.generate_content(["이 사진은 우리 주변 일상적인 사진입니다. 학생이 사진을 업로드 하면, 그 사진 속에서 발견할 수 있는 사회적 문제를 추출해 주세요. 위험, 어려움, 생태, 사회구조적문제 등 어떤 것이어도 좋습니다. 학생의 아이디어를 생성할 수 있도록 많은 이야기를 해주세요.", img])

        # Resolve the response
        response.resolve()

        # 결과 표시
        st.image(img) # 업로드된 사진 출력
        st.markdown(response.text)
else:
    st.markdown("핸드폰 사진을 업로드하세요.")
