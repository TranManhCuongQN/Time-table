from random import shuffle
from Timetable.models import Department, Room
from Timetable.CSP.model import Class

departments = Department.objects.all()
rooms = Room.objects.all()
lst_room = [room for room in rooms]
#lst_room.sort(key=lambda r: r.capacity)
#shuffle(lst_room)
# init variables
classes = []
for department in departments:
    for course in department.courses.all():   
        number_of_rooms = 0
        r = lst_room[0]
        for room in lst_room:
            if room.capacity >= course.number_of_students:
                for cls in classes:
                    if room == cls.room:
                        number_of_rooms += 1
                # maximum course of one room in a week is 5
                if number_of_rooms < 5:
                    r = room
        cl = Class(department.name, course, r, None, None, 0)          
        classes.append(cl)

def get_class(idx):
    return classes[idx]

VARIABLES = []

for i in range(len(classes)):
    VARIABLES.append(i)
