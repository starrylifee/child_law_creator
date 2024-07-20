import streamlit as st

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

# 홈 페이지의 타이틀 설정
st.title('🛠 자치활동 보조 인공지능도구 모음 홈페이지')

# 애플리케이션 소개
st.markdown("""
    ## 🌟 안녕하세요!
    이 애플리케이션은 학생 자치활동에 필요한 여러 가지 유용한 도구들로 구성되어 있습니다. 아래는 제작된 도구들의 리스트와 기능 설명입니다.
""")

# 컬럼으로 레이아웃 구성
col1, col2 = st.columns(2)

with col1:
    st.subheader('1. 우리주변 문제상황 찾기')
    st.write('이 도구를 사용하면 사진을 통해 우리 주변의 문제상황을 찾을 수 있습니다.')

with col2:
    st.subheader('2. 제안서 생성 보조도구')
    st.write('이 도구를 사용하면, 제안서를 쉽고 빠르게 작성할 수 있습니다.')

col3, col4 = st.columns(2)

with col3:
    st.subheader('3. 발표문 생성 보조도구')
    st.write('발표 준비에 도움이 필요하신가요? 이 도구가 도와드립니다.')

with col4:
    st.subheader('4. 안건 제안 보조 챗봇 & 보조도구')
    st.write('보조챗봇을 통해 법률안과 제안서에 대한 이해를 높일 수 있습니다. 챗봇과의 대화를 통해 아이디어를 만들어보세요.')

col5, col6 = st.columns(2)

with col5:
    st.subheader('5. 이미지 생성 보조도구')
    st.write('텍스트 설명을 바탕으로 이미지를 생성합니다.')
    st.markdown('**주의:** 이미지 생성요청이 한번에 몰릴 경우 이미지생성오류가 있을 수 있습니다.')

with col6:
    st.subheader('6. 경남교육청 업무안내')
    st.write('키워드나 업무를 입력하여, 관련 부서를 검색하거나 부서의 정보를 열람할 수 있습니다..')

# 추가적인 정보 제공
st.markdown("""
    ## 🚀 시작하기
    왼쪽의 탐색 바(> 클릭)를 사용하여 원하는 도구를 선택하고 사용해 보세요. 각 도구는 사용자의 입력에 따라 다양한 결과를 제공합니다.
""")

st.markdown("""
    ## 여러분의 자치 활동을 응원합니다!
""")

# 파일 다운로드 링크 추가
st.markdown("""
    ## 📥 파일 다운로드

    1. [인공지능을 이용한 학생자치 보조 프로그램 가이드북(학생용)](https://drive.google.com/file/d/1f5dQCAgaK7mphBjZ0yZZ0hfAhRNVifQO/view?usp=drive_link)
    2. [인공지능을 이용한 학생자치 보조 프로그램 가이드북(교사용)](https://drive.google.com/file/d/1RrnuQ8RY1foqR1-fgxng8JZsGDOxupZe/view?usp=drive_link)
    3. [인공지능을 활용한 학생자치 수업자료(사례집)](https://drive.google.com/file/d/1mejb3JY2uxzAbYcxDppx8EpKmny_6fJf/view?usp=drive_link)
""")

# 이미지 경로 절대 경로로 수정
st.image("file/knlogo2.jpg")