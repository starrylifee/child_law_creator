import streamlit as st
from openai import OpenAI

# OpenAI 객체 생성 및 API 키 제공
client = OpenAI(api_key=st.secrets["api_key5"])

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

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
