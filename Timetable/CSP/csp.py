from abc import ABC, abstractclassmethod
from copy import deepcopy
from random import shuffle

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

    def domains_copy(self):
        if self.curr_domains is None:
            self.curr_domains = { var: deepcopy(self.domains[var]) for var in self.variables }
    
    def first_unassigned_value(self, assignment):
        unassigned = [var for var in self.variables if var not in assignment]
        return unassigned[0]

    def suppose(self, var, value):
        self.domains_copy()
        removals = [(var, val) for val in self.curr_domains[var] if val != value]
        self.curr_domains[var] = [value]
        return removals
    
    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def restore(self, removals):
        for var, val in removals:
            self.curr_domains[var].append(val)
   
    def no_inference(self, var, value, assignment, removals):
        return True

    def mrv(self, assignment):
        self.domains_copy()
        curr_domains_copy = deepcopy(self.curr_domains)
        #shuffle(curr_domains_copy)
        min_domain = max([len(curr_domains_copy[var]) for var in self.variables if var not in assignment])
        var_with_min_domain = self.first_unassigned_value(assignment)
        for var in self.variables:
           if var not in assignment:
               domain_len = len(self.curr_domains[var])
               if domain_len < min_domain:
                   min_domain = domain_len
                   var_with_min_domain = var
        return var_with_min_domain

    def forward_checking(self, variable, value, assignment, removals):
        self.domains_copy()
        for var in self.variables:
            if var != variable and var not in assignment:                
                for val in self.curr_domains[var]:
                    suppose_assignment = { variable: value, var: val }
                    if not self.consistent(var, suppose_assignment):
                        self.prune(var, val, removals)
                if not self.curr_domains[var]:
                    return False
        return True
         
    
    def backtracking(self, assignment = {}):
        if self.is_complete(assignment):
            return assignment
        var = self.first_unassigned_value(assignment)
        for room in self.domains[var][0]:
            for time in self.domains[var][1]:
                local_assignment = assignment.copy()               
                local_assignment[var] = [room, time]
                if self.consistent(var, local_assignment):
                    result = self.backtracking(local_assignment)
                    if result is not None:
                        return result
        return None 
   

    def backtracking2(self, assignment = {}, select_unassigned_value=first_unassigned_value, inferences=forward_checking):
        if self.is_complete(assignment):
            return assignment
        var = select_unassigned_value(self, assignment)       
        for value in self.domains[var]:
            local_assignment = assignment.copy()                        
            local_assignment[var] = value
            if self.consistent(var, local_assignment):
                removals = self.suppose(var, value)
                if inferences(self, var, value, assignment, removals):
                    result = self.backtracking2(local_assignment)
                    if result is not None:
                        return result
                self.restore(removals)
        return None  
