from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["api_key"])

# 'file' 폴더 안에 있는 여러 파일 경로
file_paths = [
    "file/19th child best law.pdf",
    "file/18th child best law.pdf",
    "file/17th child best law.pdf"
]

def file_upload(file_path):
    with open(file_path, "rb") as file:
        response = client.files.create(
            file=file,
            purpose="assistants"
        )
    return response.id

# 여러 파일을 업로드하고 각 파일 ID 저장
file_ids = [file_upload(file_path) for file_path in file_paths]

def assistant_creator(file_ids):
    my_assistant = client.beta.assistants.create(
        instructions="이 assistant는 어린이들과의 대화를 통해 법률안을 제작하는 과정에서 학생들로 하여금 스스로 생각하고 창의적인 답변을 할 수 있도록 유도합니다...",
        name="어린이 법률안 제작기",
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo-1106",
        file_ids=file_ids,  # 여러 파일 ID 사용
    )
    print(my_assistant)

    return my_assistant.id

# Assistant 생성 함수 호출하고 반환된 Assistant ID 저장
my_assistant_id = assistant_creator(file_ids)
