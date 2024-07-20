import streamlit as st
from openai import OpenAI
import random

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

# secrets.toml에 저장된 API 키들을 리스트로 준비
api_keys = [
    st.secrets["api_key1"],
    st.secrets["api_key2"],
    st.secrets["api_key3"],
    st.secrets["api_key4"],
    st.secrets["api_key5"],
    st.secrets["api_key6"]
]

# 세션 상태에서 현재 API 키를 관리
if 'api_key' not in st.session_state:
    # API 키를 랜덤하게 선택하여 세션 상태에 저장
    st.session_state.api_key = random.choice(api_keys)

client = OpenAI(api_key=st.session_state.api_key)

# 페이지 레이아웃 설정

st.title("이미지 생성 보조 도구(1)")

    # 발표문 입력
presentation_text = st.text_area("발표문을(전체 혹은 일부) 입력하세요.", height=300)

# 이미지 스타일 선택
image_style = st.selectbox("이미지 스타일 선택", ["사실적", "미니멀 일러스트레이션", "만화적"])

# 이미지 생성 버튼
generate_button = st.button("이미지 생성")

if generate_button and presentation_text:
    # 선택한 스타일에 따라 프롬프트 수정
    style_prompt = {
        "사실적": "사실적인 스타일로",
        "미니멀 일러스트레이션": "미니멀 일러스트레이션 스타일로",
        "만화적": "만화적 스타일로"
    }

    prompt = f"{presentation_text} {style_prompt[image_style]}"

    try:
        # OpenAI API를 호출하여 이미지 생성
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        # 생성된 이미지 표시
        generated_image_url = image_response.data[0].url
        st.image(generated_image_url, caption="발표문 삽화")

        # 이미지 다운로드 버튼 생성
        st.markdown(f"[이미지 다운로드]({generated_image_url})", unsafe_allow_html=True)
    except Exception as e:
        st.error("이미지 생성 중 오류 발생: " + str(e))
