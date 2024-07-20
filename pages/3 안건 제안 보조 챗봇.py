from openai import OpenAI
import streamlit as st
import time
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


# 업데이트된 Assistant ID
assistant_id = "asst_vZTRHlvQaJKp9T8miz5g4RNU"

with st.sidebar:
    # 스레드 ID 관리
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = ""

    thread_btn = st.button("Thread 생성")

    if thread_btn:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id  # 스레드 ID를 session_state에 저장
        st.subheader(f"Created Thread ID: {st.session_state.thread_id}")
        st.info("스레드가 생성되었습니다.")
        st.info("스레드 ID를 기억하면 대화내용을 이어갈 수 있습니다.")
        st.divider()
        st.subheader("추천 질문")
        st.info("OOOO문제가 있어.")
        st.info("XXXX한 방향으로 해결하고 싶어.")
        st.info("법률안에는 어떤 내용이 들어가야해?")
        st.info("법률안으로 만들어줘.")

# 스레드 ID 입력란을 자동으로 업데이트
thread_id = st.text_input("Thread ID", value=st.session_state.thread_id)

st.title("안건 제안 보조 챗봇")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요, 저는 안건 제안 보조 챗봇입니다. 먼저 왼쪽의 'Thread 생성'버튼을 눌러주세요. 무엇을 도와드릴까요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    if not thread_id:
        st.error("Please add your thread_id to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)

    msg = thread_messages.data[0].content[0].text.value
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)