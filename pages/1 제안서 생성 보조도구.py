import streamlit as st
from openai import OpenAI
from io import BytesIO  # 파일 다운로드를 위해 필요
import random

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
    
st.title("제안서 작성 보조")

# 문제 상황과 해결책을 입력받습니다.
st.header("문제 상황")
problem = st.text_area("문제 상황을 입력하세요:")

st.header("해결책")
solution = st.text_area("해결책을 입력하세요:")

st.divider()

@st.cache_data  # st.experimental_memo 대신 st.cache_data 사용
def generate_proposal(problem, solution):
    persona = f'''
    이 프롬프트는 사용자로부터 제공된 문제 상황과 해결 방안을 바탕으로, 체계적이고 전문적인 제안서를 생성하는 데 도움을 주는 GPT 모델입니다. 제안서는 '제안배경'과 '주요내용' 두 필수 카테고리를 포함해야 합니다. '제안배경' 아래에는 개조식으로 제안서를 제안한 배경을 주요 사건이나 통계등을 반드시 언급하며 간략하지만 명료하게 제시해야 합니다. '주요내용' 아래에는 개조식으로 제안 배경을 해결할 방법을 간단하고 명료하게 제시해야 합니다. 이 제안서는 시민이 공공기관에 제출할 내용으로 문제상황에 대한 해결방안을 공공기관에게 요청하는 내용을 담아야 합니다. 다음은 사용자가 제공한 문제 상황과 해결 방안입니다: 문제 상황: {problem} 해결 방안: {solution}'''

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": "제안서를 작성해주세요."}
        ],
        max_tokens=2000,
        temperature=0.7
    )
    return response.choices[0].message.content

# 제안서 생성 버튼
if st.button("제안서 생성하기"):
    proposal = generate_proposal(problem, solution)
    st.subheader("생성된 제안서")
    st.write(proposal)
    
    # 생성된 제안서를 TXT 파일로 변환
    txt_file = BytesIO(proposal.encode('utf-8'))
    
    # 다운로드 링크 제공
    st.download_button(
        label="제안서 다운로드하기",
        data=txt_file,
        file_name="generated_proposal.txt",
        mime="text/plain"
    )