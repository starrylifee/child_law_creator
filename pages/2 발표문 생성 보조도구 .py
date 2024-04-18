import streamlit as st
from openai import OpenAI
from io import BytesIO

# OpenAI 클라이언트 객체 생성
client = OpenAI(api_key=st.secrets["api_key2"])

st.set_page_config(layout="wide")
    
st.title("발표문 생성기")

# 대상 선택
st.header("청중 선택")
audience = st.radio("청중을 선택하세요:", ('어린이', '청소년', '성인'))

# 발표 시간 선택
st.header("발표 시간 선택")
presentation_time = st.selectbox("발표할 시간을 선택하세요:", ['5분', '10분', '15분', '20분'])

# 제안서와 법률 입력 받기
st.header("제안서 및 법률")
proposal = st.text_area("제안서를 입력하세요 (50줄 내외):")
law = st.text_area("법률 내용을 입력하세요 (50줄 내외):")

st.divider()

@st.cache_data
def generate_speech(proposal, law, audience, presentation_time):
    # 발표 시간에 따른 max_tokens 추정
    time_to_tokens = {'5분': 600, '10분': 1200, '15분': 1800, '20분': 2400} # 추정값

    prompt = f'''
    청중({audience})을 위한 발표문을 생성해주세요. 발표문은 서론, 본론, 결론을 포함해야 하며, 각 부분은 명확하게 구분되어야 합니다. 발표문은 다음 제안서와 법률에 기반해야 합니다:

    제안서: {proposal}
    법률: {law}
    
    서론은 발표문의 주제를 소개하고, 청중의 관심을 끌어야 합니다. 본론은 제안서와 법률에 대한 상세한 분석과 논의를 제공해야 합니다. 결론은 발표문의 핵심 메시지를 요약하고, 청중에게 강한 인상을 남겨야 합니다.
    '''

    # chat_completions.create 메소드를 사용한 호출로 변경
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=time_to_tokens[presentation_time],
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content

# 발표문 생성 버튼
if st.button("발표문 생성하기"):
    speech = generate_speech(proposal, law, audience, presentation_time)
    st.subheader("생성된 발표문")
    st.write(speech)

    # 발표문을 TXT 파일로 변환
    txt_file = BytesIO(speech.encode('utf-8'))

    # 다운로드 링크 제공
    st.download_button(
        label="발표문 다운로드하기",
        data=txt_file,
        file_name="generated_speech.txt",
        mime="text/plain"
    )