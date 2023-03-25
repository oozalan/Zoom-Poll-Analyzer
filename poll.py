class Poll:
    def __init__(self):
        self._pollName = 'dummyName'
        self._pollDate = 'dummyDate'
        self._isMatched = False
        self._questions = list()

    def isThisThePoll(self, questionTexts):
        for questionText in questionTexts:
            i = 0
            for question in self._questions:
                if questionText.replace(" ", "") in question._questionText.replace(" ", ""):
                    break

                i += 1
                if i == len(self._questions):
                    return False

        return True

    def findQuestion(self, questionText):
        for question in self._questions:
            if questionText.replace(" ", "") in question._questionText.replace(" ", ""):
                return question
        return None