from .csp import *
from .variable import get_class

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
        for timeslot in assignment[self.variable_1]:
            if timeslot in assignment[self.variable_2]:
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

        for timeslot in assignment[self.variable_1]:
            if timeslot in assignment[self.variable_2]:
                return False

        return True


class InOneSessionConstraint(Constraint):
    def __init__(self, variable):
        super().__init__([variable])
        self.variable = variable

    def satisfied(self, assignment):        
        start = assignment[self.variable][0] % 5
        end = assignment[self.variable][-1] % 5

        if end < start:
            return False
        return True