import random

def select_question(df, difficulty):
    subset = df[df["difficulty"] == difficulty]

    if subset.empty:
        subset = df

    return subset.sample(1).iloc[0]