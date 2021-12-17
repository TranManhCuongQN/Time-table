from .csp import *

class SameRoomTimeConstraint(Constraint):
    def __init__(self, variable_1, variable_2):
        super().__init__([variable_1, variable_2])
        self.variable_1 = variable_1
        self.variable_2 = variable_2
    
    # return True: not violated, Fasle: violated
    def satisfied(self, assignment):
        if self.variable_1 not in assignment or self.variable_2 not in assignment:
            return True

        # assignement[var][0]: room, assignment[var][1]: time
        if assignment[self.variable_1][0].name == assignment[self.variable_2][0].name \
            and assignment[self.variable_1][1] == assignment[self.variable_2][1]:
            return False
        return True

class SameInstuctorConstraint(Constraint):
    def __init__(self, variable_1, variable_2):
        super().__init__([variable_1, variable_2])
        self.variable_1 = variable_1
        self.variable_2 = variable_2
    
    def satisfied(self, assignment):
        # check if it is first variable in assignment
        if self.variable_1 not in assignment or self.variable_2 not in assignment:
            return True

        # different department, same course, same instructor, same time
        if self.variable_1.department != self.variable_2.department and self.variable_1.course.name == self.variable_2.course.name \
            and self.variable_1.instructor.name == self.variable_2.instructor.name and assignment[self.variable_1][1] == assignment[self.variable_2][1]:
            return False

        # same department, difference course, same instructor, same time
        if self.variable_1.department == self.variable_2.department and self.variable_1.course.name != self.variable_2.course.name \
            and self.variable_1.instructor.name == self.variable_2.instructor.name and assignment[self.variable_1][1] == assignment[self.variable_2][1]:
            return False

        # difference department, difference course, same instructor, same time
        if self.variable_1.department != self.variable_2.department and self.variable_1.course.name != self.variable_2.course.name \
            and self.variable_1.instructor.name == self.variable_2.instructor.name and assignment[self.variable_1][1] == assignment[self.variable_2][1]:
            return False
        return True

class FitRoomCapacityConstraint(Constraint):
    def __init__(self, variable):
        super().__init__([variable])
        self.variable = variable
    def satisfied(self, assignment):
        # assignment[var][0]: room
        if self.variable.number_of_students > assignment[self.variable][0].capacity:
            return False
        return True
