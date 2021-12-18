from django.db import models
from django.db.models.deletion import SET_NULL

#from multiselectfield import MultiSelectField

# Create your models here.

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Instructor(models.Model):
    inst_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    number_of_students = models.IntegerField()
    number_of_lessions_per_week = models.IntegerField(default=1)
    instructors = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name
    
    @property
    def get_courses(self):
        return self.courses

class Timetable(models.Model):
    timetable_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.timetable_id


class Session(models.Model):

    # TIMESLOTS = (
    #     ("07:00", "07:50"),
    #     ("07:50", "08:40"),
    #     ("08:40", "09:30"),
    #     ("09:40", "10:30"),
    #     ("10:40", "11:30"),
    #     ("12:30", "13:20"),
    #     ("13:20", "14:10"),
    #     ("14:20", "15:10"),
    #     ("15:10", "16:00"),
    #     ("16:10", "17:00")
    # )

    TIMESLOTS = (
        ("07:00", "07:50"),
        ("07:50", "08:40"),
        ("08:40", "09:30"),
        ("09:40", "10:30"),
        ("10:40", "11:30"),       
    )

    DAYS = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
    )

    session_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    instructor = models.ForeignKey(Instructor, blank=True, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=SET_NULL)
    number_of_students = models.IntegerField()
    day = models.CharField(max_length=20, choices=DAYS)
    timeslots = models.CharField(max_length=20, choices=TIMESLOTS)
    timetable = models.ForeignKey(Timetable, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.department) + ", " + str(self.course) + ", " \
        + str(self.instructor) + ", " + str(self.room) + "\n"