from tkinter import *
from dbHandler import *


# To see it, run MainWindow with one of the student test IDs on line 13
# Sorry it's messy - Connor

# some new student IDs from DB v2 //Gary
# Test IDs  1733675
#           1734055
#           1735936


# Made a few edits so it can be displayed in the main window


############################################################
#
# to Connor:
# I'm sorry, from yesterday the old DB structure won't be available
# let's see how could you get the data for this view
# at first let's word it:
# you need the *grade(s)* for each *module* the of one single *student*
#
# by design data in *module* is just the description of the modules, it doesn't link to elsewhere but to *groupset* table
#
# these are the basic tables, with fields:
# grade: id, grade, gradeType, studentID, groupsetID
# groupset: id, groupsetName, year, semester, moduleCode, teacherID
# module: id, moduleCode, moduleName, moduleDescription
# student: id, studentID, studentGender, studentSurname, studentName, studentEmail, studentPassword
#
# so lets go through what we need as a sequence:
# 1. we have the studentID, that's where we can start
# 2. simple as is, we can search grade table for the studentID, and we get a bunch of data, good, but
# we will not know which modules are those IDs for, neither the year/semester
# 3. so we need to decide, either find all different groupsetIDs from the last search and build on that
# or we can do a search on groupset table with the studentID and year at the same time, so we have a list of the students groups too
# if you chose the second (I would) you can do the query on groupset first, and then use that data to search on grades
# 4. anyway, we will verbose the modules, by getting their name from another query from module table,
# that's simple, we have the moduleIDs from groupset query
#
# to sort this out, I would use multiple arrays for each query, would limit the fields to the ones we really need to work with/display
# such as teacherID from groupset, to keep it simple, we don't care *as a student* who was the teacher (at least this stage)
# or if you want a challenge, you can write a complex query by using standard SQL language using IN, EXIST, ORDER BY, and so on.
# For example: http://stackoverflow.com/questions/4622453/where-col1-col2-in-sql-subquery-using-composite-primary-key
#
# (a little hint for 'order by') we do not store 'year' as DATE, it's just a simple TEXT field, it's sloppy but should be ok.
# I'll change the DB once more if we get there ever.
#
# if you need multiple fields from a table, it could be done with a single DB query, like:
# self.c.execute("SELECT * FROM student WHERE studentID = '" + self.userID + "'")
# and then skim through it with a for loop, or
# self.c.execute("SELECT studentName, studentSurname FROM student WHERE studentID = '" + self.userID + "'")
# so you will get back the tuple with these two fields in a list
#
# I reckon it seems a bit much but one you start it will be kind of straight forward,
# use a lot of prints to console to see if you get and pass the data you wanted, etc. but you know this anyway
#
# Give me a shout if you stuck somewhere
# Keep up!
# Gary
#
############################################################

class Student(object):

    crDB = DbConn("db/crDB.db")
    c = crDB.cursor

    def __init__(self):
        self.userID = ""
        self.userName = ""
        self.userSurname = ""
        self.userModuleCode = []
        self.userModuleNames = []
        self.userGrade = []
        self.userYear = []
        self.userSemester = []
        self.userTeacherID = []
        self.userTeacherName = []
        self.userTeacherSurname = []
        self.usergroupsetID = []

    def setID(self, userID):
        self.userID = userID

    def getinfo(self):

        # Gets the student name and any sets they are in
        self.c.execute("SELECT studentName FROM student WHERE studentID = '" + self.userID + "'")
        self.userName = self.c.fetchone()[0]
        self.c.execute("SELECT studentSurname FROM student WHERE studentID = '" + self.userID + "'")
        self.userSurname = self.c.fetchone()[0]
        self.c.execute("SELECT groupsetID FROM grade WHERE studentID = '" + self.userID + "'")
        self.usergroupsetID = self.c.fetchall()

        # Gets info for each module set
        c = 0
        for i in self.usergroupsetID:
            self.c.execute("SELECT moduleCode FROM groupset WHERE groupsetID = '" + str(i[0]) + "'")
            self.userModuleCode.append(self.c.fetchone())
            self.c.execute("SELECT moduleName FROM module WHERE moduleCode = '" + self.userModuleCode[c][0] + "'")
            self.userModuleNames.append(self.c.fetchone())
            self.c.execute("SELECT gradeType FROM grade WHERE studentID = '" + self.userID + "'")
            self.userGrade.append(self.c.fetchone())
            self.c.execute("SELECT year FROM groupset WHERE groupsetID = '" + str(i[0]) + "'")
            self.userYear.append(self.c.fetchone())
            self.c.execute("SELECT semester FROM groupset WHERE groupsetID = '" + str(i[0]) + "'")
            self.userSemester.append(self.c.fetchone())
            self.c.execute("SELECT teacherID FROM groupset WHERE groupsetID = '" + str(i[0]) + "'")
            self.userTeacherID.append(self.c.fetchone())
            self.c.execute("SELECT teacherName FROM teacher WHERE teacherID = '" + self.userTeacherID[c][0] + "'")
            self.userTeacherName.append(self.c.fetchone())
            self.c.execute("SELECT teacherSurname FROM teacher WHERE teacherID = '" + self.userTeacherID[c][0] + "'")
            self.userTeacherSurname.append(self.c.fetchone())
            c+=1





def displaystudentview(student, mainFrame):

    # Headers
    intro = Label(mainFrame, text="Viewing grades for ", bg="chartreuse3")
    sName = Label(mainFrame, text=student.userName + " " + student.userSurname, bg="chartreuse3")
    sID = Label(mainFrame, text=student.userID, bg="chartreuse3")


    intro.grid(row=0, column=0, sticky=W + E)
    sName.grid(row=0, column=1, sticky=W + E)
    sID.grid(row=0, column=2, sticky=W + E)

    # Column Titles
    mName = Label(mainFrame, text="Module Name", bg="grey52")
    mCode = Label(mainFrame, text="Module Code", bg="grey52")
    mGrade = Label(mainFrame, text="Grade", bg="grey52")
    mYear = Label(mainFrame, text="Year", bg="grey52")
    mSemester = Label(mainFrame, text="Semester", bg="grey52")
    mTeacher = Label(mainFrame, text="Teacher", bg="grey52")

    mName.grid(row=2, column=0, sticky=W+E)
    mCode.grid(row=2, column=1, sticky=W+E)
    mGrade.grid(row=2, column=2, sticky=W+E)
    mYear.grid(row=2, column=3, sticky=W+E)
    mSemester.grid(row=2, column=4, sticky=W+E)
    mTeacher.grid(row=2, column=5, sticky=W+E)

    # Aesthetics
    alabel = Label(mainFrame, text=" ", bg="chartreuse3")
    alabel.grid(row=1, columnspan=6, sticky=W+E)

    alabel2 = Label(mainFrame, text=" ", bg="chartreuse3")
    alabel2.grid(row=0, column=3, columnspan=3, sticky=W+E)


# Creates and displays a label for each module taken by the student
def displayLabels(student, mainFrame):

    c = 0
    for i in student.userModuleCode:
        uP = Label(mainFrame, text=student.userModuleNames[c][0], bg="snow")  # module name
        uPCode = Label(mainFrame, text=student.userModuleCode[c][0], bg="snow")  # moduleCode
        uPGrade = Label(mainFrame, text=student.userGrade[c][0], bg="snow")  # Grade
        uPyear = Label(mainFrame, text=student.userYear[c][0], bg="snow")  # Year
        uPSemester = Label(mainFrame, text=student.userSemester[c][0], bg="snow")  # Semester
        uPTeacher = Label(mainFrame, text=student.userTeacherName[c][0] + " " + student.userTeacherSurname[c][0],
                      bg="snow")  # Teacher

        uP.grid(row=3 + c, column=0, sticky=W + E)
        uPCode.grid(row=3 + c, column=1, sticky=W + E)
        uPGrade.grid(row=3 + c, column=2, sticky=W + E)
        uPyear.grid(row=3 + c, column=3, sticky=W + E)
        uPSemester.grid(row=3 + c, column=4, sticky=W + E)
        uPTeacher.grid(row=3 + c, column=5, sticky=W + E)

        c += 1



