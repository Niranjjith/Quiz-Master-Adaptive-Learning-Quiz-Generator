# Adaptive Quiz Master

Adaptive Quiz Master is a web-based quiz application that adjusts question difficulty in real time based on the learner's performance. It uses clustering and a simple user model to keep users in their optimal learning zone.

---

## Features

- **Adaptive difficulty** powered by a `UserModel` that tracks accuracy and adjusts levels.
- **Automatic difficulty clustering** of questions using `KMeans` (`scikit-learn`).
- **Professional web UI** built with **Flask** and **Bootstrap**, not Streamlit.
- **Session-based tracking** of total questions, correct answers, and accuracy.

---

## Project Structure

- `app.py` – Flask web app entry point and routes.
- `src/data_loader.py` – Loads questions from CSV.
- `src/clustering.py` – Clusters questions into difficulty levels.
- `src/user_model.py` – Tracks user performance and adjusts difficulty.
- `src/question_selector.py` – Selects a question at a given difficulty.
- `src/evaluation.py` – Checks if a selected answer is correct.
- `templates/index.html` – Main HTML template with the quiz UI.
- `data/raw/questions.csv` – Question bank (CSV) used by the app.

---

## Requirements

Install Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install:

- `flask`
- `pandas`
- `scikit-learn`
- `numpy`

---

## Running the App

From the project root:

```bash
python app.py
```

Then open your browser at:

```text
http://127.0.0.1:5000/
```

You will see the Adaptive Quiz Master web interface with:

- A central question card.
- Four multiple-choice options (A–D).
- A progress panel showing accuracy, total questions, and correct answers.

---

## Data Format

The questions CSV (`data/raw/questions.csv`) is expected to contain at least:

- `question` – the question text
- `option_a`, `option_b`, `option_c`, `option_d` – four answer choices
- `answer` – the correct option label (`A`, `B`, `C`, or `D`)
- `accuracy_rate` – numeric feature used for clustering
- `avg_time` – numeric feature used for clustering

Make sure these columns exist and are properly populated so clustering and question selection work correctly.

---

## Customization

- **UI / Styling**: Update `templates/index.html` (Bootstrap-based) for colors, layout, or branding.
- **Difficulty logic**: Adjust the thresholds or behavior in `src/user_model.py`.
- **Clustering**: Change the number of clusters or features in `src/clustering.py`.

---

## License

This project is provided as-is for educational and experimental use. Update this section with your preferred license if you plan to distribute it.

