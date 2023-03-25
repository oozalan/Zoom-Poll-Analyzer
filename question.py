class Question:
    def __init__(self, questionText, poll):
        self._questionText = questionText
        self._poll = poll
        self._correctAnswers = list()

    def addCorrectAnswer(self, correctAnswer):
        self._correctAnswers.append(correctAnswer)