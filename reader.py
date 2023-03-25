import copy
import os

import pandas as pd

from answer import Answer
from poll import Poll
from question import Question
from student import Student


class Reader:
    @staticmethod
    def readStudents():
        excel = pd.read_excel(r'CES3063_Fall2020_rptSinifListesi.xls', header=12, usecols="C,E,H")
        excel = excel.dropna()
        students = list()

        for index, row in excel.iterrows():
            if "Öğrenci No" in row["Öğrenci No"]:
                continue

            nameBlock = ''
            nameBlock = row["Adı"]
            nameBlock = nameBlock.split()
            lastNameBlock = ''
            lastNameBlock = row["Soyadı"]
            lastNameBlock = lastNameBlock.split()

            s1 = Student(row["Öğrenci No"], nameBlock, lastNameBlock)
            students.append(s1)
        return students
    @staticmethod
    def readAnswerKeys():
        polls = list()

        originalPath = os.getcwd()
        os.chdir('Answer Keys')
        fileNames = os.listdir(os.getcwd())
        filePath = ""

        for fileName in fileNames:
            filePath = os.path.abspath(fileName)
            answerKey = open(filePath, 'r', encoding='utf-8')

            for line in answerKey:
                # New poll is found
                if line.startswith(' Poll '):
                    poll = Poll()
                    poll._pollName = line[1:].split("\t")[0]
                    poll._pollName = poll._pollName.replace(":", " ")
                    poll._pollName = poll._pollName.replace(" ", "_")
                    polls.append(poll)
                    continue

                # New question is found
                if line[0:1].isnumeric():
                    lineSplitted = line[3:].split("(")
                    lineSplitted.pop()
                    questionText = ""

                    for part in lineSplitted:
                        if questionText == "":
                            questionText = questionText + part
                        else:
                            questionText = questionText + "(" + part

                    questionText = questionText.replace("\r", "")
                    questionText = questionText.replace("\n", "")
                    question = Question(questionText, poll)
                    poll._questions.append(question)
                    continue

                # New answer is found
                if line.startswith('Answer'):
                    text = line[10:]
                    text = text.replace("\r", "")
                    text = text.replace("\n", "")
                    question.addCorrectAnswer(text)

            answerKey.close()

        os.chdir(originalPath)
        return polls

    def readPolls(students, polls, attendancePolls):
        originalPath = os.getcwd()
        os.chdir('Poll Reports')
        fileNames = os.listdir(os.getcwd())
        filePath = ""

        for fileName in fileNames:
            print(fileName)
            filePath = os.path.abspath(fileName)
            dateString = ""
            pollCsv = pd.read_csv(filePath, header=None, error_bad_lines=False, engine='python', skiprows=3,
                                  names=range(0, 30))

            currentPoll = Poll()
            for j, (index, row) in enumerate(pollCsv.iterrows()):
                if j == 0:
                    dateString = row[2]
                    dateString = dateString.replace("-", "_")
                    dateString = dateString.replace(" ", "_")
                    dateString = dateString.replace(":", "_")
                    currentPoll._pollDate = dateString
                    continue

                if j in [1, 2]:
                    continue

                student = None
                nameBlock = row[1]
                emailBlock = row[2]
                dateTime = row[3]
                currentPollQuestions = []
                studentCurrentPollAnswers = []

                for s in students:
                    if s.nameCheck(nameBlock, emailBlock):
                        student = s
                        break

                if student == None:
                    print("===========>couldn't find student: " + str(row[1]) + "<===========")
                    continue

                for i in range(4, len(pollCsv.columns), 2):
                    if str(row[i]) == 'None' or str(row[i]) == 'nan':
                        if i + 2 == len(pollCsv.columns):
                            break
                        continue

                    question_text = str(row[i])
                    question_text = question_text.replace("\r", "")
                    question_text = question_text.replace("\n", "")
                    student_answers = str(row[i + 1])
                    student_answers = student_answers.replace("\r", "")
                    student_answers = student_answers.replace("\n", "")

                    if ';' in student_answers:
                        studentAnswerList = list()
                        studentAnswerList = student_answers.split(";")
                        answer = Answer(student, studentAnswerList)
                        studentCurrentPollAnswers.append(answer)
                        currentPollQuestions.append(question_text)
                    else:
                        studentAnswerList = list()
                        studentAnswerList.append(student_answers)
                        answer = Answer(student, studentAnswerList)
                        studentCurrentPollAnswers.append(answer)
                        currentPollQuestions.append(question_text)

                isAttendancePoll = True
                for poll in polls:
                    if poll.isThisThePoll(currentPollQuestions):
                        isAttendancePoll = False
                        if poll._isMatched:
                            if currentPoll._pollName != poll._pollName:
                                newPoll = copy.deepcopy(poll)
                                polls.append(newPoll)
                                currentPoll._isMatched = True
                                currentPoll._pollDate = dateString
                                currentPoll = newPoll
                            i = 0
                            for answer in studentCurrentPollAnswers:
                                answer._question = currentPoll.findQuestion(currentPollQuestions[i])
                                student._answers.append(answer)
                                i += 1
                        else:
                            if currentPoll._pollName != poll._pollName:
                                currentPoll._isMatched = True
                                currentPoll._pollDate = dateString
                                currentPoll = poll

                            i = 0
                            for answer in studentCurrentPollAnswers:
                                answer._question = poll.findQuestion(currentPollQuestions[i])
                                student._answers.append(answer)
                                i += 1
                        break

                if isAttendancePoll:  # The case that we can not find the poll --> Attendance poll detected!
                    if currentPoll._pollName != "Attendance Poll":
                        attendancePoll = Poll()
                        attendancePoll._pollName = "Attendance Poll"
                        attendanceQuestion = Question("Are you attending this lecture?", attendancePoll)
                        attendancePoll._questions.append(attendanceQuestion)
                        currentPoll._pollDate = dateString
                        currentPoll = attendancePoll
                        attendancePoll._pollDate = dateString
                        attendancePolls.append(attendancePoll)

                    for answer in studentCurrentPollAnswers:
                        answer._question = attendanceQuestion
                        student._answers.append(answer)

                if (j == len(pollCsv) - 1):
                    currentPoll._isMatched = True
                    currentPoll._pollDate = dateString

        os.chdir(originalPath)
