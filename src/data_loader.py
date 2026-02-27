import pandas as pd

def load_questions(path="data/raw/questions.csv"):
    df = pd.read_csv(path)
    return df