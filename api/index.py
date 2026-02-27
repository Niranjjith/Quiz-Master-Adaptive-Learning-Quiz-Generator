from flask import Flask, render_template, request, redirect, url_for, session, flash
from src.data_loader import load_questions
from src.clustering import DifficultyClustering
from src.user_model import UserModel
from src.question_selector import select_question
from src.evaluation import check_answer


app = Flask(__name__, template_folder="../templates")
app.secret_key = "change-me-in-production"


df = load_questions()
cluster = DifficultyClustering()
questions_df = cluster.fit(df)


def get_user_model():
    data = session.get("user_model")
    user = UserModel()
    if data:
        user.total_questions = data.get("total_questions", 0)
        user.correct_answers = data.get("correct_answers", 0)
        user.current_difficulty = data.get("current_difficulty", 1)
    return user


def save_user_model(user: UserModel):
    session["user_model"] = {
        "total_questions": user.total_questions,
        "correct_answers": user.correct_answers,
        "current_difficulty": user.current_difficulty,
    }


@app.route("/", methods=["GET"])
def index():
    user = get_user_model()
    difficulty = user.current_difficulty

    question = select_question(questions_df, difficulty)
    question_dict = {
        "question": question["question"],
        "option_a": question["option_a"],
        "option_b": question["option_b"],
        "option_c": question["option_c"],
        "option_d": question["option_d"],
        "answer": question["answer"],
    }
    session["current_question"] = question_dict

    accuracy = user.accuracy()

    return render_template(
        "index.html",
        question=question_dict,
        difficulty=difficulty,
        accuracy=accuracy,
        total_questions=user.total_questions,
        correct_answers=user.correct_answers,
    )


@app.route("/submit", methods=["POST"])
def submit():
    selected = request.form.get("selected_option")
    current_question = session.get("current_question")

    if not current_question or not selected:
        flash("Please select an option.", "warning")
        return redirect(url_for("index"))

    user = get_user_model()

    correct = check_answer(selected, current_question["answer"])
    user.update(correct)

    if correct:
        flash("Correct! Great job.", "success")
    else:
        flash(f"Wrong! Correct answer: {current_question['answer']}", "danger")

    user.adjust_difficulty()
    save_user_model(user)

    return redirect(url_for("index"))

