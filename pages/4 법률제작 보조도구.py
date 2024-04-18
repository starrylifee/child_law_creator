import streamlit as st
from openai import OpenAI
from io import BytesIO  # 파일 다운로드를 위해 필요

# OpenAI 클라이언트 객체 생성
client = OpenAI(api_key=st.secrets["api_key4"])

st.set_page_config(layout="wide")

st.title("법률안 작성 보조 도구")

# 사용자로부터 필요한 정보를 입력받습니다.
st.header("1. 문제 상황")
problem = st.text_area("무슨 문제가 있나요?")

st.header("2. 이상적인 모습")
ideal = st.text_area("문제가 해결된 이상적인 모습은 어떤 모습인가요?")

st.header("3. 해결 방안")
solution = st.text_area("문제를 해결할 방안은 무엇인가요?")

st.header("4. 국가의 노력")
government_action = st.text_area("문제를 해결하기 위해 국가가 노력해야 할 부분은 있나요?")

st.header("5. 벌칙")
penalties = st.text_area("규칙을 지키지 않을 경우 어떤 벌을 줄 수 있을까요?")

st.header("6. 추가 내용")
additional_content = st.text_area("법률에 추가하고 싶은 내용이 있나요?")

st.divider()

@st.cache_data  # st.experimental_memo 대신 st.cache_data 사용
def generate_law_document(problem, ideal, solution, government_action, penalties, additional_content):
    persona = f'''
    이 프롬프트는 사용자로부터 제공된 문제 상황, 이상적인 모습, 해결 방안, 국가의 노력, 벌칙, 추가 내용을 바탕으로, 대한민국 법률 형식에 맞는 법률안을 생성하는 데 도움을 주는 GPT 모델입니다. 이 법률안은 문제를 해결하고 이상적인 상태를 달성하기 위한 구체적인 방안을 제시해야 합니다. 사용자가 제공한 내용이 현실에 맞지 않거나 사실에 맞지 않는 경우 GPT가 수정해서 작성합니다. 법률안을 작성한 후 피드백을 반드시 작성합니다. 다음은 사용자가 제공한 내용입니다:
    문제 상황: {problem}
    이상적인 모습: {ideal}
    해결 방안: {solution}
    국가의 노력: {government_action}
    벌칙: {penalties}
    추가 내용: {additional_content}'''

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": "법률안을 작성해주세요."}
        ],
        max_tokens=3000,
        temperature=0.7
    )
    return response.choices[0].message.content

# 법률안 생성 버튼
if st.button("법률안 생성하기"):
    law_document = generate_law_document(problem, ideal, solution, government_action, penalties, additional_content)
    st.subheader("생성된 법률안")
    st.write(law_document)
    
    # 생성된 법률안을 TXT 파일로 변환
    txt_file = BytesIO(law_document.encode('utf-8'))
    
    # 다운로드 링크 제공
    st.download_button(
        label="법률안 다운로드하기",
        data=txt_file,
        file_name="generated_law_document.txt",
        mime="text/plain"
    )