class UserModel:
    def __init__(self):
        self.total_questions = 0
        self.correct_answers = 0
        self.current_difficulty = 1

    def update(self, correct):
        self.total_questions += 1
        if correct:
            self.correct_answers += 1

    def accuracy(self):
        if self.total_questions == 0:
            return 0
        return self.correct_answers / self.total_questions

    def adjust_difficulty(self):
        acc = self.accuracy()
        if acc > 0.8:
            self.current_difficulty = min(self.current_difficulty + 1, 2)
        elif acc < 0.5:
            self.current_difficulty = max(self.current_difficulty - 1, 0)

        return self.current_difficulty