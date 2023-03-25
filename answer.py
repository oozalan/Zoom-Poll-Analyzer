class Answer:
    def __init__(self, student, studentAnswers):
        self._student = student
        self._studentAnswers = studentAnswers

    def isCorrect(self):
        for studentAnswer in self._studentAnswers:
            for correctAnswer in self._question._correctAnswers:
                if studentAnswer.replace(" ", "") == correctAnswer.replace(" ", ""):
                    return 1
        return 0