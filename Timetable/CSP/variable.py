from Timetable.models import Department
from Timetable.CSP.model import Class

departments = Department.objects.all()

classes = []
for department in departments:
    for course in department.courses.all():
        for i in range(course.number_of_lessions_per_week):            
            cl = Class(department.name, course, None, None, None, i + 1)
            classes.append(cl)

print(len(classes))

def get_class(idx):
    return classes[idx]

VARIABLES = []

for i in range(len(classes)):
    VARIABLES.append(i)
