class Class:
    def __init__(self, department, course, room, time, date, lession_no):
        self.department = department
        self.course = course
        self.instructor = course.instructors
        self.room = room
        self.time = time
        self.date = date
        self.number_of_students = course.number_of_students
        self.lession_no = lession_no