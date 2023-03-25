import os

from reader import Reader
from writer import Writer


class Controller:
    @staticmethod
    def start():
        students = Reader.readStudents()
        polls = Reader.readAnswerKeys()
        attendancePolls = list()
        Reader.readPolls(students, polls, attendancePolls)

        for poll in polls:
            if not poll._isMatched:
                polls.remove(poll)

        try:
            os.mkdir("Poll Results")
        except FileExistsError:
            pass

        try:
            os.mkdir("Poll Details")
        except FileExistsError:
            pass

        try:
            os.mkdir("Poll Statistics")
        except FileExistsError:
            pass

        Writer.writeAttendance(students, polls, attendancePolls)

        for poll in polls:
            Writer.writePollResults(students, poll)
            # Writer.writePollStatistics(students, poll)

        Writer.writeGlobal(students)

        for poll in polls:
            for student in students:
                Writer.writePollDetails(poll, student)