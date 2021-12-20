from .csp import *

# class SameRoomTimeConstraint(Constraint):
#     def __init__(self, variable_1, variable_2):
#         super().__init__([variable_1, variable_2])
#         self.variable_1 = variable_1
#         self.variable_2 = variable_2
    
#     # return True: not violated, Fasle: violated
#     def satisfied(self, assignment):
#         if self.variable_1 not in assignment or self.variable_2 not in assignment:
#             return True

#         # assignement[var][0]: room, assignment[var][1]: time
#         if assignment[self.variable_1][0].name == assignment[self.variable_2][0].name \
#             and assignment[self.variable_1][1] == assignment[self.variable_2][1]:
#             return False
#         return True

class SameRoomTimeConstraint2(Constraint):
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

# class SameInstuctorConstraint(Constraint):
#     def __init__(self, variable_1, variable_2):
#         super().__init__([variable_1, variable_2])
#         self.variable_1 = variable_1
#         self.variable_2 = variable_2
    
#     def satisfied(self, assignment):
#         # check if it is first variable in assignment
#         if self.variable_1 not in assignment or self.variable_2 not in assignment:
#             return True

#         # different department, same course, same instructor, same time
#         if self.variable_1.department != self.variable_2.department and self.variable_1.course.name == self.variable_2.course.name \
#             and self.variable_1.instructor.name == self.variable_2.instructor.name and assignment[self.variable_1][1] == assignment[self.variable_2][1]:
#             return False

#         # same department, difference course, same instructor, same time
#         if self.variable_1.department == self.variable_2.department and self.variable_1.course.name != self.variable_2.course.name \
#             and self.variable_1.instructor.name == self.variable_2.instructor.name and assignment[self.variable_1][1] == assignment[self.variable_2][1]:
#             return False

#         # difference department, difference course, same instructor, same time
#         if self.variable_1.department != self.variable_2.department and self.variable_1.course.name != self.variable_2.course.name \
#             and self.variable_1.instructor.name == self.variable_2.instructor.name and assignment[self.variable_1][1] == assignment[self.variable_2][1]:
#             return False
#         return True
    


class SameInstuctorConstraint2(Constraint):
    def __init__(self, variable_1, variable_2):
        super().__init__([variable_1, variable_2])
        self.variable_1 = variable_1
        self.variable_2 = variable_2
    
    def satisfied(self, assignment):
        # check if it is first variable in assignment
        if self.variable_1 not in assignment or self.variable_2 not in assignment:
            return True

        # different department, same course, same instructor, same time
        if self.variable_1.department != self.variable_2.department \
            and self.variable_1.course.course_id == self.variable_2.course.course_id \
            and self.variable_1.instructor.inst_id == self.variable_2.instructor.inst_id \
            and self.variable_1.lession_no != self.variable_2.lession_no \
            and assignment[self.variable_1][1] == assignment[self.variable_2][1]:
            return False
            
        # same department, difference course, same instructor, same time
        if self.variable_1.department == self.variable_2.department \
            and self.variable_1.course.course_id != self.variable_2.course.course_id \
            and self.variable_1.instructor.inst_id == self.variable_2.instructor.inst_id \
            and assignment[self.variable_1][1] == assignment[self.variable_2][1]:
            return False
            

        # difference department, difference course, same instructor, same time
        if self.variable_1.department != self.variable_2.department \
            and self.variable_1.course.course_id != self.variable_2.course.course_id \
            and self.variable_1.instructor.inst_id == self.variable_2.instructor.inst_id \
            and assignment[self.variable_1][1] == assignment[self.variable_2][1]:
            return False
        return True

class InOneSessionConstraint(Constraint):
    def __init__(self, variable_1, variable_2):
        super().__init__([variable_1, variable_2])
        self.variable_1 = variable_1
        self.variable_2 = variable_2

    def satisfied(self, assignment):
        if self.variable_1 not in assignment or self.variable_2 not in assignment:
            return True
        
        start = assignment[self.variable_1][1] % 5
        if self.variable_1.lession_no == 1:
            calc_end = assignment[self.variable_1][1] + self.variable_1.course.number_of_lessions_per_week - 1   
            end_in_session = calc_end % 5
            if start > end_in_session:
                return False
            return True
      
        end = assignment[self.variable_2][1] % 5       
        if end < start:
            return False
        return True

    # def satisfied(self, assignment):
    #     # each 5 hourse is a session (0 -> 4, 4 -> 9, 9 -> 14 ...)
    #     start = assignment[self.variable][1][0] % 5
    #     end = assignment[self.variable][1][-1] % 5
    #     if end < start:
    #         return False
    #     return True
        
        

class ConnectedLessionsConstraint(Constraint):
    def __init__(self, variable_1, variable_2):
        super().__init__([variable_1, variable_2])
        self.variable_1 = variable_1
        self.variable_2 = variable_2

    def satisfied(self, assignment):      
        if self.variable_1 not in assignment or self.variable_2 not in assignment:
            return True

        if self.variable_1.department != self.variable_2.department:
            return False
        else:
            if self.variable_1.course.course_id != self.variable_2.course.course_id:
                return False
            else:
                period = assignment[self.variable_2][1] - assignment[self.variable_1][1]
                if assignment[self.variable_1][0].room_id == assignment[self.variable_2][0].room_id and period == 1:
                    return True
                else:
                    return False
                 


# class FitRoomCapacityConstraint(Constraint):
#     def __init__(self, variable):
#         super().__init__([variable])
#         self.variable = variable
#     def satisfied(self, assignment):
#         # assignment[var][0]: room
#         if self.variable.number_of_students > assignment[self.variable][0].capacity:
#             return False
#         return True
