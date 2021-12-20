from abc import ABC, abstractclassmethod
from copy import deepcopy

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
        self.curr_domains = None
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

    def backtracking2(self, assignment = {}):
        if self.is_complete(assignment):
            return assignment
        var = self.select_unassigned_value(assignment)       
        for value in self.domains[var]:
            local_assignment = assignment.copy()                        
            local_assignment[var] = value
            if self.consistent(var, local_assignment):
                result = self.backtracking2(local_assignment)
                if result is not None:
                    return result
        return None  

    def domains_copy(self):
        if self.curr_domains is None:
            self.curr_domains = { var: deepcopy(self.domains[var]) for var in self.variables }

    def AC3(self, queue = None, removals = None):
        if queue is None:
            queue = { (Xi, Xj) for Xi in self.variables for Xj in self.variables if Xj != Xi }
        self.domains_copy()
        while queue:
            (Xi, Xj) = queue.pop()
            revised = self.revise(self, Xi, Xj)
            if revised:
                if not self.curr_domains[Xi]:
                    return False
                for Xk in self.variables:
                    if Xk != Xi:
                        queue.add((Xk, Xi))
        return True

    
   
        
