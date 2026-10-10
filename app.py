import streamlit as st

# 1. 초기 세션 상태 설정 (오답 및 풀이 상태 기록)
if 'wrong_answers' not in st.session_state:
    st.session_state.wrong_answers = []
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "전체 문제"

# 예시 한자 데이터 (총 150개 가정)
all_questions = [
    {"id": i, "question": f"한자 문제 {i+1}", "answer": "정답"}
    for i in range(150)
]

st.title("한자 학습 앱")

# 2. 모드 선택 (일반 풀기 vs 틀린 문제만 다시 풀기)
mode = st.radio("학습 모드를 선택하세요", ["일반 문제 풀기", "틀린 문제만 다시 풀기"])

if mode == "일반 문제 풀기":
    # 3. 50개씩 끊어서 선택하기
    chunk_size = 50
    total_questions = len(all_questions)
    
    # 50개 단위 범위 옵션 생성 (예: 1~50, 51~100, 101~150)
    options = [
        f"{i + 1}번 ~ {min(i + chunk_size, total_questions)}번"
        for i in range(0, total_questions, chunk_size)
    ]
    
    selected_range = st.selectbox("문제 범위를 선택하세요 (50개 단위)", options)
    
    # 선택한 범위의 인덱스 계산
    selected_idx = options.index(selected_range)
    start_idx = selected_idx * chunk_size
    end_idx = min(start_idx + chunk_size, total_questions)
    
    current_questions = all_questions[start_idx:end_idx]
    st.write(f"현재 선택된 문제 수: {len(current_questions)}개")

else:
    # 4. 틀린 문제만 다시 풀기 모드
    if not st.session_state.wrong_answers:
        st.info("🎉 틀린 문제가 없습니다!")
        current_questions = []
    else:
        current_questions = st.session_state.wrong_answers
        st.warning(f"복습할 틀린 문제 수: {len(current_questions)}개")

# 5. 문제 풀기 화면 (간단 예시)
if current_questions:
    st.divider()
    for q in current_questions:
        st.subheader(q["question"])
        user_ans = st.text_input(f"정답을 입력하세요 (문제 ID: {q['id']})", key=f"q_{q['id']}")
        
        if st.button(f"정답 확인 (문제 {q['id']})", key=f"btn_{q['id']}"):
            if user_ans == q["answer"]:
                st.success("정답입니다!")
                # 맞췄으면 오답 목록에서 제거
                if q in st.session_state.wrong_answers:
                    st.session_state.wrong_answers.remove(q)
            else:
                st.error("틀렸습니다!")
                # 틀렸으면 오답 목록에 추가
                if q not in st.session_state.wrong_answers:
                    st.session_state.wrong_answers.append(q)
