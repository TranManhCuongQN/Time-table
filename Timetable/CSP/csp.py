from abc import ABC, abstractclassmethod

class Constraint(ABC):
    def __init__(self, variables):
        self.variables = variables

    @abstractclassmethod
    def satisfied(self, assignment):
        ...
    

class CSP():
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = domains
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable not in CSP")
            else:
                self.constraints[variable].append(constraint)
    
    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def is_complete(self, assignment):
        if len(assignment) == len(self.variables):
            return True
        return False
    
    def select_unassigned_value(self, assignment):
        unassigned = [var for var in self.variables if var not in assignment]
        return unassigned[0]
    
    def backtracking(self, assignment = {}):
        if self.is_complete(assignment):
            return assignment
        var = self.select_unassigned_value(assignment)
        for room in self.domains[var][0]:
            for time in self.domains[var][1]:
                local_assignment = assignment.copy()
                local_assignment[var] = [room, time]
                if self.consistent(var, local_assignment):
                    result = self.backtracking(local_assignment)
                    if result is not None:
                        return result
        return None       
