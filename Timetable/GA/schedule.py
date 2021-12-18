import numbers
import random
from copy import deepcopy
from random import sample, shuffle, choice, random, randrange

from Timetable.GA.chromosome import Chromosome
from Timetable.models import Room, Department



TIMESLOTS = []
for i in range(25):
    TIMESLOTS.append(i)

class Class:
    def __init__(self, department, course, lession_no):
        self.department = department    # string: department name
        self.course = course            # django db model
        self.room = None                # django db model 
        self.timeslot = None            # list(int): index of timeslot
        self.lession_no = lession_no    # int: lession number

    def get_department(self): return self.department
    
    def get_course(self): return self.course

    def get_room(self): return self.room

    def get_timeslot(self): return self.timeslot

    def get_lession_no(self): return self.lession_no

    def set_room(self, room): self.room = room

    def set_timeslot(self, timeslot): self.timeslot = timeslot

class Timetable(Chromosome):
    def __init__(self, classes):
        self.classes = classes
        self.fitness_value = 0

    def get_classes(self): return self.classes

    def fitness(self):
        number_of_conflicts = 0
        for i in range(len(self.classes)):

            # number of students langer than room capacity
            if self.classes[i].course.number_of_students > self.classes[i].room.capacity:
                number_of_conflicts += 1
            for j in range(len(self.classes)):
                if j > i:                    
                    fst_class = self.classes[i]
                    snd_class = self.classes[j]

                    for fst_timeslot in fst_class.timeslot:
                        if fst_timeslot in snd_class.timeslot:
                            if fst_class.room.name == snd_class.room.name:
                                number_of_conflicts += 1
                            if fst_class.department != snd_class.department:
                                if fst_class.course.course_id == snd_class.course.course_id:
                                    if fst_class.course.instructors.inst_id == snd_class.course.instructors.inst_id:
                                        number_of_conflicts += 1
                                else:
                                    if fst_class.course.instructors.inst_id == snd_class.course.instructors.inst_id:
                                        number_of_conflicts += 1
                            else:
                                if fst_class.course.course_id != snd_class.course.course_id:
                                    number_of_conflicts += 1
                                    if fst_class.course.instructors.inst_id == snd_class.course.instructors.inst_id:
                                        number_of_conflicts += 1
                    """
                    # difference department, same course, same time, same instructor
                    if fst_class.department != snd_class.department \
                        and fst_class.course.course_id == snd_class.course.course_id \
                        and fst_class.timeslot == snd_class.timeslot \
                        and fst_class.course.instructors.inst_id == snd_class.course.instructors.inst_id:
                        number_of_conflicts += 1

                    # difference department, difference course, same time, same instructor
                    if fst_class.department != snd_class.department \
                        and fst_class.course.course_id != snd_class.course.course_id \
                        and fst_class.timeslot == snd_class.timeslot \
                        and fst_class.course.instructors.inst_id == snd_class.course.instructors.inst_id:
                        number_of_conflicts += 1

                    # same department, difference course, same time, same instructor
                    if fst_class.department == snd_class.department \
                        and fst_class.course.course_id != snd_class.course.course_id \
                        and fst_class.timeslot == snd_class.timeslot \
                        and fst_class.course.instructors.inst_id == snd_class.course.instructors.inst_id:
                        number_of_conflicts += 1
                    
                    period = abs(fst_class.timeslot - snd_class.timeslot)
                    """
                  

        return 1 / (1.0 * number_of_conflicts + 1)
    """
    @classmethod
    def random_instance(cls):
        classes = []
        rooms = Room.objects.all()
        departments = Department.objects.all()
        for dept in departments:
            courses = dept.courses.all()
            for course in courses:
                for lession in range(course.number_of_lessions_per_week):
                    newClass = Class(dept.name, course, lession)
                    newClass.set_timeslot(TIMESLOTS[randrange(0, len(TIMESLOTS))])
                    newClass.set_room(rooms[randrange(0, len(rooms))])
                    classes.append(newClass)
        shuffle(classes)
        return Timetable(classes)
    """

    @classmethod
    def random_instance(cls):
        classes = []
        rooms = Room.objects.all()
        departments = Department.objects.all()
        for dept in departments:
            courses = dept.courses.all()
            for course in courses:               
                newClass = Class(dept.name, course, 0)
                timeslots = []
                rand = randrange(0, len(TIMESLOTS) - 1)
                while rand + course.number_of_lessions_per_week >= len(TIMESLOTS):
                    rand = randrange(0, len(TIMESLOTS))
                for i in range(course.number_of_lessions_per_week):
                    timeslots.append(rand + i)
                newClass.set_timeslot(timeslots)
                newClass.set_room(rooms[randrange(0, len(rooms))])
                classes.append(newClass)
        shuffle(classes)
        return Timetable(classes)


    def crossover(self, other):
        timetable1 = deepcopy(self)
        timetable2 = deepcopy(other)

        timetable_crossover = Timetable.random_instance()
        """
        for i in range(0, len(timetable_crossover.classes)):
            if random() > 0.5:
                timetable_crossover.classes[i] = timetable1.classes[i]
            else:
                timetable_crossover.classes[i] = timetable2.classes[i]
        """

        rand = randrange(0, len(timetable_crossover.classes))
        timetable_crossover.classes[:rand] = timetable1.classes[:rand]
        timetable_crossover.classes[rand:] = timetable2.classes[rand:]
        return deepcopy(timetable_crossover)

    
        

    def mutate(self):
        rooms = Room.objects.all()
        for i in range(0, len(self.classes)):
            self.classes[i].set_room(rooms[randrange(0, len(rooms))])
            timeslots = []
            rand = randrange(0, len(TIMESLOTS) - 1)
            while rand + self.classes[i].course.number_of_lessions_per_week >= len(TIMESLOTS):
                rand = randrange(0, len(TIMESLOTS))
            for i in range(self.classes[i].course.number_of_lessions_per_week):
                timeslots.append(rand + i)
            self.classes[i].set_timeslot(timeslots)
            

