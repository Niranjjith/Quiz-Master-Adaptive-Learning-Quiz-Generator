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


def pick_unique_question(difficulty, used_ids):
    df_local = questions_df
    subset = df_local[df_local["difficulty"] == difficulty]
    if used_ids:
        subset = subset[~subset.index.isin(used_ids)]
    if subset.empty:
        subset = df_local[~df_local.index.isin(used_ids)]
    if subset.empty:
        return None
    return subset.sample(1).iloc[0]


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
    finished = session.get("finished", False)
    question_count = session.get("question_count", 0)
    used_ids = session.get("used_question_ids", [])

    accuracy = user.accuracy()
    if accuracy >= 0.8:
        accuracy_level = "Excellent"
    elif accuracy >= 0.5:
        accuracy_level = "Good"
    elif accuracy > 0:
        accuracy_level = "Needs Improvement"
    else:
        accuracy_level = "Not enough data"

    if finished:
        return render_template(
            "index.html",
            finished=True,
            question=None,
            difficulty=user.current_difficulty,
            accuracy=accuracy,
            accuracy_level=accuracy_level,
            total_questions=min(question_count, 10),
            correct_answers=user.correct_answers,
        )

    difficulty = user.current_difficulty
    question = pick_unique_question(difficulty, used_ids)
    if question is None:
        session["finished"] = True
        return redirect(url_for("index"))

    qid = int(question.name)
    used_ids.append(qid)
    session["used_question_ids"] = used_ids
    question_dict = {
        "question": question["question"],
        "option_a": question["option_a"],
        "option_b": question["option_b"],
        "option_c": question["option_c"],
        "option_d": question["option_d"],
        "answer": question["answer"],
    }
    session["current_question"] = question_dict

    return render_template(
        "index.html",
        finished=False,
        question=question_dict,
        difficulty=difficulty,
        accuracy=accuracy,
        accuracy_level=accuracy_level,
        total_questions=question_count,
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

    question_count = session.get("question_count", 0) + 1
    session["question_count"] = question_count

    if correct:
        flash("Correct! Great job.", "success")
    else:
        flash(f"Wrong! Correct answer: {current_question['answer']}", "danger")

    user.adjust_difficulty()
    save_user_model(user)

    if question_count >= 10:
        session["finished"] = True

    return redirect(url_for("index"))


@app.route("/restart", methods=["POST"])
def restart():
    session.clear()
    return redirect(url_for("index"))

