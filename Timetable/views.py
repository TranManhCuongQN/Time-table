from django.shortcuts import redirect, render
from django.contrib import messages
from itertools import combinations

from .forms import *
from .models import Course, Instructor, Room, Department, Session, Timetable
from .CSP.csp import CSP
from .CSP.model import Class
from .CSP.constraints import *

# Create your views here.

def home(request):
    return render(request, 'index.html', {})

def listCourses(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses.html', context)

def listInstructors(request):
    instructors = Instructor.objects.all()
    context = {'instructors': instructors}
    return render(request, 'instructors.html', context)

def listRooms(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'rooms.html', context)

def listDepartments(request):
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, 'departments.html', context)

def listTimetables(request):
    timetables = Timetable.objects.all()
    context = {'timetables': timetables}
    return render(request, 'timetables.html', context)

def addCourse(request):
    course_form = CourseForm()
    context = {'course_form': course_form}

    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        
        if course_form.is_valid():
            messages.success(request, 'Added course.')
            course_form.save()
            return redirect('courses')
        else:
            messages.success(request, 'Can not add course.')

    return render(request, 'add-course.html', context)


def addInstructor(request):
    instructor_form = InstructorForm()
    context = {'instructor_form': instructor_form}

    if request.method == 'POST':
        instructor_form = InstructorForm(request.POST)
        
        if instructor_form.is_valid():
            messages.success(request, 'Added instructor.')
            instructor_form.save()
            return redirect('instructors')
        else:
            messages.success(request, 'Can not add instructor.')

    return render(request, 'add-instructor.html', context)


def addRoom(request):
    room_form = RoomForm()
    context = {'room_form': room_form}

    if request.method == 'POST':
        room_form = RoomForm(request.POST)
        
        if room_form.is_valid():
            messages.success(request, 'Added room.')
            room_form.save()
            return redirect('rooms')
        else:
            messages.success(request, 'Can not add room.')

    return render(request, 'add-room.html', context)


def addDepartment(request):
    department_form = DepartmentForm()
    context = {'department_form': department_form}

    if request.method == 'POST':
        department_form = DepartmentForm(request.POST)
        
        if department_form.is_valid():
            messages.success(request, 'Added department.')
            department_form.save()
            return redirect('departments')
        else:
            messages.success(request, 'Can not add department.')

    return render(request, 'add-department.html', context)

def deleteCourse(request, pk):
    course = Course.objects.get(course_id=pk)

    if request.method == 'POST':
        course.delete()
        return redirect('courses')

def deleteInstructor(request, pk):
    instructor = Instructor.objects.get(inst_id=pk)
    
    if request.method == 'POST':
        instructor.delete()
        return redirect('instructors')

def deleteRoom(request, pk):
    room = Room.objects.get(room_id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('rooms')

def deleteDepartment(request, pk):
    department = Department.objects.get(dept_id=pk)

    if request.method == 'POST':
        department.delete()
        return redirect('departments')

def deleteTimetable(request, pk):
    timetable = Timetable.objects.get(timetable_id=pk)

    if request.method == 'POST':
        timetable.delete()
        return redirect('timetables')

def updateCourse(request, pk):
    course = Course.objects.get(course_id=pk)
    course_form = CourseForm(instance=course)
    context = {'course_form': course_form}

    if request.method == 'POST':
        course_form = CourseForm(request.POST, instance=course)

        if course_form.is_valid():
            course_form.save()
            return redirect('courses')
    
    return render(request, 'update-course.html', context)

def updateInstructor(request, pk):
    instructor = Instructor.objects.get(inst_id=pk)
    inst_form = InstructorForm(instance=instructor)
    context = {'instructor_form': inst_form}

    if request.method == 'POST':
        inst_form = InstructorForm(request.POST, instance=instructor)

        if inst_form.is_valid():
            inst_form.save()
            return redirect('instructors')
    
    return render(request, 'update-instructor.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(room_id=pk)
    room_form = RoomForm(instance=room)
    context = {'room_form': room_form}

    if request.method == 'POST':
        room_form = RoomForm(request.POST, instance=room)

        if room_form.is_valid():
            room_form.save()
            return redirect('rooms')
    
    return render(request, 'update-room.html', context)

def updateDepartment(request, pk):
    dept = Department.objects.get(dept_id=pk)
    dept_form = DepartmentForm(request.POST, instance=dept)
    context = {'department_form': dept_form}

    if request.method == 'POST':
        dept_form = DepartmentForm(request.POST, instance=dept)

        if dept_form.is_valid():
            dept_form.save()
            return redirect('departments')

    return render(request, 'update-department.html', context)

def updateTimetable(request, pk):
    timetable = Timetable.objects.get(timetable_id=pk)
    timetable_form = TimetableForm(request.POST, instance=timetable)
    context = {'timetable_form': timetable_form}

    if request.method == 'POST':
        timetable_form = TimetableForm(request.POST, instance=timetable)

        if timetable_form.is_valid():
            timetable_form.save()
            return redirect('timetables')
    
    return render(request, 'update-timetable.html', context)



def generateTimetableCSP(request):
    rooms = Room.objects.all()
    departments = Department.objects.all()

    classes = []
    for department in departments:
        for course in department.courses.all():
            for i in range(course.number_of_lessions_per_week):
                cl = Class(department.name, course, None, None, None, i)
                classes.append(cl)
    timeslots = []
    for i in range(25):
        timeslots.append(i)
    
    domains = {}
    for cl in classes:
        domains[cl] = [rooms, timeslots]

    scheduler = CSP(classes, domains)

    comb = combinations(classes, 2)
    for com in comb:
        scheduler.add_constraint(SameRoomTimeConstraint(com[0], com[1]))
        scheduler.add_constraint(SameInstuctorConstraint(com[0], com[1]))

    for clas in classes:
        scheduler.add_constraint(FitRoomCapacityConstraint(clas))
    result = scheduler.backtracking()

    if result is not None:
        timetable = Timetable.objects.create()
        timeslots = [
            "07:00 - 07:50",
            "07:50 - 08:40",
            "08:40 - 09:30",
            "09:40 - 10:30",
            "10:40 - 11:30",
        ]
        for session in result.keys():
            ses = Session()
            room_name = result[session][0].name
            ses.room = Room.objects.get(name=room_name)
            ses.department = Department.objects.get(name=session.department)
            ses.course = Course.objects.get(name=session.course.name)
            ses.instructor = Instructor.objects.get(name=session.instructor)
            ses.number_of_students = session.number_of_students
            ses.timetable = timetable
            
            no_of_timeslots_per_day = len(timeslots)
            ses.timeslots = timeslots[result[session][1] % no_of_timeslots_per_day]

            if result[session][1] < no_of_timeslots_per_day:
                ses.day = "Monday"
            elif result[session][1] >= no_of_timeslots_per_day and result[session][1] < no_of_timeslots_per_day * 2:
                ses.day = "Tuesday"
            elif result[session][1] >= no_of_timeslots_per_day * 2 and result[session][1] < no_of_timeslots_per_day * 3:
                ses.day = "Wednesday"
            elif result[session][1] >= no_of_timeslots_per_day * 3 and result[session][1] < no_of_timeslots_per_day * 4:
                ses.day = "Thursday"
            elif result[session][1] >= no_of_timeslots_per_day * 4 and result[session][1] < no_of_timeslots_per_day * 5:
                ses.day = "Friday"
            ses.save()
        return redirect('viewTimetable', pk=timetable.timetable_id)
    else:
        return redirect('timetables')
    

def viewTimetable(request, pk):
    timetable = Timetable.objects.get(timetable_id=pk)
    sessions = timetable.session_set.all()
    depts = Department.objects.all()
    MEETING_TIMES = [
        "07:00 - 07:50",
        "07:50 - 08:40",
        "08:40 - 09:30",
        "09:40 - 10:30",
        "10:40 - 11:30",
    ]
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    context = {
        'sessions': sessions,
        'departments': depts,
        'days': DAYS,
        'timeslots': MEETING_TIMES,
    }
    return render(request, 'view-timetable.html', context)
