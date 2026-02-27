import streamlit as st
import pandas as pd
from src.data_loader import load_questions
from src.clustering import DifficultyClustering
from src.user_model import UserModel
from src.question_selector import select_question
from src.evaluation import check_answer

st.set_page_config(page_title="Adaptive Quiz Master")

st.title("🎯 Adaptive Learning Quiz")

# Session State Setup
if "user_model" not in st.session_state:
    st.session_state.user_model = UserModel()

if "questions" not in st.session_state:
    df = load_questions()
    cluster = DifficultyClustering()
    df = cluster.fit(df)
    st.session_state.questions = df

if "current_question" not in st.session_state:
    difficulty = st.session_state.user_model.current_difficulty
    st.session_state.current_question = select_question(
        st.session_state.questions, difficulty
    )

question = st.session_state.current_question

# Display Question
st.subheader(f"Difficulty Level: {st.session_state.user_model.current_difficulty}")
st.write(question["question"])

options = {
    "A": question["option_a"],
    "B": question["option_b"],
    "C": question["option_c"],
    "D": question["option_d"],
}

selected = st.radio("Choose an option:", list(options.keys()), format_func=lambda x: options[x])

if st.button("Submit"):
    correct = check_answer(selected, question["answer"])

    st.session_state.user_model.update(correct)

    if correct:
        st.success("Correct!")
    else:
        st.error(f"Wrong! Correct answer: {question['answer']}")

    new_difficulty = st.session_state.user_model.adjust_difficulty()

    st.session_state.current_question = select_question(
        st.session_state.questions, new_difficulty
    )

# Dashboard
st.sidebar.header("📊 Progress")

accuracy = st.session_state.user_model.accuracy()
st.sidebar.metric("Accuracy", f"{accuracy:.2f}")
st.sidebar.metric("Total Questions", st.session_state.user_model.total_questions)
st.sidebar.metric("Correct Answers", st.session_state.user_model.correct_answers)