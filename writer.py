import os
import pandas as pd
import xlsxwriter


class Writer:
    def writeAttendance(students, polls, attendancePolls):
        workbook = xlsxwriter.Workbook("Attendance.xlsx")
        worksheet = workbook.add_worksheet()

        days = list()
        for attendancePoll in attendancePolls:
            days.append(attendancePoll._pollDate)

        for poll in polls:
            days.append(poll._pollDate)

        days = list(dict.fromkeys(days))

        a = 0
        worksheet.write(a, 0, "Student ID")
        worksheet.write(a, 1, "Student Name")
        worksheet.write(a, 2, "Student Last Name")
        worksheet.write(a, 3, "Number of Days")
        worksheet.write(a, 4, "Attendance Rate")
        worksheet.write(a, 5, "Attendance Percentage")
        a += 1

        for student in students:
            attendanceCount = 0

            for day in days:
                for answer in student._answers:
                    if answer._question._poll._pollDate in day:
                        attendanceCount += 1
                        break

            name = " ".join(student._name)
            lastName = " ".join(student._lastName)

            worksheet.write(a, 0, student._studentID)
            worksheet.write(a, 1, name)
            worksheet.write(a, 2, lastName)
            worksheet.write(a, 3, len(days))
            worksheet.write(a, 4, str(attendanceCount) + "/" + str(len(days)))
            worksheet.write(a, 5, '%' + "{:.2f}".format((attendanceCount / len(days)) * 100))
            a += 1

        workbook.close()

    def writePollResults(students, poll):
        workbook = xlsxwriter.Workbook('Poll Results/' + poll._pollName + "_" + poll._pollDate + ".xlsx")
        worksheet = workbook.add_worksheet()

        a = 0
        worksheet.write(a, 0, "Student ID")
        worksheet.write(a, 1, "Student Name")
        worksheet.write(a, 2, "Student Last Name")

        for i in range(len(poll._questions)):
            Q = 'Q' + str(i + 1)
            worksheet.write(a, (i + 3), Q)

        i = 3 + len(poll._questions)
        worksheet.write(a, i, "Number of Questions")
        worksheet.write(a, i + 1, "Number of True Questions")
        worksheet.write(a, i + 2, "Number of Wrong Questions")
        worksheet.write(a, i + 3, "Number of Empty Questions")
        worksheet.write(a, i + 4, "Success Rate")
        worksheet.write(a, i + 5, "Success Percentage")

        for a, student in enumerate(students, start=1):
            name = " ".join(student._name)
            lastName = " ".join(student._lastName)

            worksheet.write(a, 0, student._studentID)
            worksheet.write(a, 1, name)
            worksheet.write(a, 2, lastName)

            isAttended = True
            totalCorrectAnswers = 0
            i = 3
            for question in poll._questions:
                for l, answer in enumerate(student._answers):
                    if answer._question == question:
                        worksheet.write(a, i, answer.isCorrect())
                        totalCorrectAnswers += answer.isCorrect()
                        i += 1
                        break

                    if l == len(student._answers) - 1:
                        isAttended = False

            totalWrongAnswers = 0
            totalEmptyAnswers = len(poll._questions)

            if isAttended:
                totalWrongAnswers = len(poll._questions) - totalCorrectAnswers
                totalEmptyAnswers = 0

            i = 3 + len(poll._questions)
            worksheet.write(a, i, len(poll._questions))
            worksheet.write(a, i + 1, totalCorrectAnswers)
            worksheet.write(a, i + 2, totalWrongAnswers)
            worksheet.write(a, i + 3, totalEmptyAnswers)
            worksheet.write(a, i + 4, str(totalCorrectAnswers) + "/" + str(len(poll._questions)))
            worksheet.write(a, i + 5, "%" + str((totalCorrectAnswers / len(poll._questions)) * 100.0))

        workbook.close()

    def writePollStatistics(students, poll):
        workbook = xlsxwriter.Workbook(
            'Poll Statistics/' + poll._pollName.replace(" ", "_") + "_" + poll._pollDate.replace(" ", "_") + ".xlsx")
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})

        data = list()
        data.append(list())
        for i in range(len(poll._questions)):
            data[0].append("Question " + str(i + 1))

        data.append(list())
        data.append(list())
        data.append(list())
        data.append(list())
        data.append(list())

        x = 19
        y = 1
        for question in poll._questions:
            options = []
            optionsOccur = []

            worksheet.merge_range(x, 0, x, 3, "Q" + str(y) + " Text")
            worksheet.merge_range(x, 4, x, 12, question._questionText)
            y += 1

            for student in students:
                for answer in student._answers:
                    if question == answer._question:
                        for studentAnswer in answer._studentAnswers:
                            if studentAnswer not in options:
                                options.append(studentAnswer)
                                optionsOccur.append(0)
                            optionsOccur[options.index(studentAnswer)] += 1

            while len(optionsOccur) != 5:
                optionsOccur.append(0)

            x += 1
            z = 1
            for choiceText in options:
                worksheet.merge_range(x, 0, x, 3, "Choice" + str(z) + " Text")
                worksheet.merge_range(x, 4, x, 12, choiceText)
                x += 1
                z += 1

            x += 1

            for j in range(len(optionsOccur)):
                data[j + 1].append(optionsOccur[j])

        headings = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
        worksheet.write_row(0, 0, headings, bold)

        i = 1
        for element in data:
            worksheet.write_row(i, 0, element)
            i += 1

        chart1 = workbook.add_chart({'type': 'column'})
        chart1.add_series({
            'name': ['Sheet1', 0, 0],
            'categories': ['Sheet1', 1, 0, 1, 9],
            'values': ['Sheet1', 2, 0, 2, 9],
        })

        chart1.add_series({
            'name': ['Sheet1', 0, 1],
            'categories': ['Sheet1', 1, 0, 1, 9],
            'values': ['Sheet1', 3, 0, 3, 9],
        })

        chart1.add_series({
            'name': ['Sheet1', 0, 2],
            'categories': ['Sheet1', 1, 0, 1, 9],
            'values': ['Sheet1', 4, 0, 4, 9],
        })

        chart1.add_series({
            'name': ['Sheet1', 0, 3],
            'categories': ['Sheet1', 1, 0, 1, 9],
            'values': ['Sheet1', 5, 0, 5, 9],
        })

        chart1.add_series({
            'name': ['Sheet1', 0, 4],
            'categories': ['Sheet1', 1, 0, 1, 9],
            'values': ['Sheet1', 6, 0, 6, 9],
        })

        chart1.set_title({'name': 'Question Results'})
        chart1.set_x_axis({'name': 'Questions'})
        chart1.set_y_axis({'name': 'Answer Amounts'})
        chart1.set_style(11)
        worksheet.insert_chart(0, 0, chart1, {'x_offset': 25, 'y_offset': 10})

        workbook.close()

    def writePollDetails(poll, student):
        name = "_".join(student._name)
        lastName = "_".join(student._lastName)
        workbook = xlsxwriter.Workbook(
            'Poll Details/' + poll._pollName + "_" + poll._pollDate + "_" + name + "_" + lastName + "_" + student._studentID + ".xlsx")
        worksheet = workbook.add_worksheet()

        a = 0
        worksheet.merge_range(a, 0, a, 6, "Question Text")
        worksheet.merge_range(a, 7, a, 10, "Given Answer")
        worksheet.merge_range(a, 11, a, 14, "Correct Answer")
        worksheet.write(a, 15, "Is Correct")
        a += 1

        for answer in student._answers:
            if answer._question._poll == poll:
                questionText = answer._question._questionText
                worksheet.merge_range(a, 0, a, 6, questionText)

                givenAnswer = ";".join(answer._studentAnswers)
                worksheet.merge_range(a, 7, a, 10, givenAnswer)

                correctAnswer = ";".join(answer._question._correctAnswers)
                worksheet.merge_range(a, 11, a, 14, correctAnswer)

                worksheet.write(a, 15, answer.isCorrect())
                a += 1

        workbook.close()

    def writeGlobal(students):
        workbook = xlsxwriter.Workbook("CSE3063_2020FALL_QuizGrading.xlsx")
        worksheet = workbook.add_worksheet()

        a = 0
        worksheet.write(a, 0, "Index")
        worksheet.write(a, 1, "Student ID")
        worksheet.write(a, 2, "Student Full Name")
        a += 1

        for student in students:
            name = " ".join(student._name)
            lastName = " ".join(student._lastName)

            worksheet.write(a, 0, str(a))
            worksheet.write(a, 1, student._studentID)
            worksheet.write(a, 2, name + " " + lastName)
            a += 1

        originalPath = os.getcwd()
        os.chdir('Poll Results')
        fileNames = os.listdir(os.getcwd())
        filePath = ""

        fileNamesSorted = list()
        for fileName in fileNames:
            if len(fileNamesSorted) == 0:
                fileNamesSorted.append(fileName)
                continue

            for i, fileNameSorted in enumerate(fileNamesSorted):
                if int(fileName[-24:-20]) > int(fileNameSorted[-24:-20]):  ## years comparison
                    continue
                elif int(fileName[-24:-20]) < int(fileNameSorted[-24:-20]):
                    fileNamesSorted.insert(i, fileName)
                    break
                else:
                    if int(fileName[-19:-17]) > int(fileNameSorted[-19:-17]):  ## month comparison
                        continue
                    elif int(fileName[-19:-17]) < int(fileNameSorted[-19:-17]):
                        fileNamesSorted.insert(i, fileName)
                        break
                    else:
                        if int(fileName[-16:-14]) > int(fileNameSorted[-16:-14]):  ## days comparison
                            continue
                        else:
                            fileNamesSorted.insert(i, fileName)
                            break

        studentsTotalCorrectAnswers = list()
        for i in range(len(students)):
            studentsTotalCorrectAnswers.append(0)

        totalQuestions = 0
        column = 3
        for fileName in fileNamesSorted:
            filePath = os.path.abspath(fileName)
            excel = pd.read_excel(filePath, header=0)

            a = 0
            worksheet.write(a, column, fileName[0:len(fileName) - 5])
            a += 1

            for j, (index, row) in enumerate(excel.iterrows()):
                if j == 0:
                    totalQuestions += int(row["Number of Questions"])

                totalCorrectAnswers = int(row["Number of True Questions"])
                studentsTotalCorrectAnswers[j] += totalCorrectAnswers
                worksheet.write(a, column, totalCorrectAnswers)
                a += 1

            column += 1

        a = 0
        worksheet.write(a, column, "Global Accuracy")
        a += 1

        for i in studentsTotalCorrectAnswers:
            worksheet.write(a, column, "%" + "{:.2f}".format((i / totalQuestions) * 100))
            a += 1

        os.chdir(originalPath)
        workbook.close()