from abc import ABC, abstractclassmethod
from copy import deepcopy
from random import shuffle

from Timetable.CSP.variable import get_class

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
        self.neighbors = {}
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            self.neighbors[variable] = []

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def add_neighbor(self, variable, neighbor):
        if variable not in self.variables:
            raise LookupError("Variable not in CSP")
        else:
            self.neighbors[variable].append(neighbor)
    
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
        class_1 = get_class(variable)
        timeslot_of_variable = []
        for i in range(class_1.course.number_of_lessions_per_week):
            timeslot_of_variable.append(value + i)
        for var in self.neighbors[variable]:
            if var not in assignment:    
                class_2 = get_class(var)                           
                for val in self.curr_domains[var]:   
                    timeslot_of_var = []
                    if val + class_2.course.number_of_lessions_per_week - 1 > 24:
                        self.prune(var, val, removals)
                        continue
                    for i in range(class_2.course.number_of_lessions_per_week):
                        timeslot_of_var.append(val + i)
                    suppose_assignment = { variable: timeslot_of_variable, var: timeslot_of_var }
                    if not self.consistent(var, suppose_assignment):
                        self.prune(var, val, removals)
                if not self.curr_domains[var]:
                    return False
        return True       

    def AC3(self, queue=None, removals=None):
        if queue is None:
            queue = {(Xi, Xj) for Xi in self.variables for Xj in self.neighbors[Xi]}
        self.domains_copy()
           
        while queue:
            (Xi, Xj) = queue.pop()
            for x in self.curr_domains[Xi]:
                if not in_one_section(Xi, x):
                    self.prune(Xi, x, removals)
            revised = self.revise(Xi, Xj, removals)
            if revised:
                if not self.curr_domains[Xi]:
                    return False
                for Xk in self.neighbors[Xi]:
                    if Xk != Xj:
                        queue.add((Xk, Xi))
        return True
    
    def revise(self, Xi, Xj, removals):
        revised = False
        class_1 = get_class(Xi)
        class_2 = get_class(Xj)
        for x in self.curr_domains[Xi][:]:
            conflict = True
            timeslot_of_Xi = []
            if x + class_1.course.number_of_lessions_per_week - 1 > 24:
                self.prune(Xi, x, removals)
                continue
            for i in range(class_1.course.number_of_lessions_per_week):
                timeslot_of_Xi.append(x + i)
            for y in self.curr_domains[Xj]:
                timeslot_of_Xj = []
                if y + class_2.course.number_of_lessions_per_week - 1 > 24: 
                    continue
                for i in range(class_2.course.number_of_lessions_per_week):
                    timeslot_of_Xj.append(y + i)
                suppose_assigment = {Xi: timeslot_of_Xi, Xj: timeslot_of_Xj}
                if self.consistent(Xj, suppose_assigment):
                    conflict = False
                if not conflict: 
                    break
            if conflict:
                self.prune(Xi, x, removals)
                revised = True
        return revised

    
    def mac(self, var, value, assignment, removals, constraint_propagation=AC3):
        return constraint_propagation(self, {(X, var) for X in self.neighbors[var]}, removals)
           

    def backtracking(self, assignment = {}, select_unassigned_value=first_unassigned_value, inferences=mac):
        if self.is_complete(assignment):
            return assignment
        var = select_unassigned_value(self, assignment)       
        for value in self.curr_domains[var]:
            local_assignment = assignment.copy()  
            timeslots = []
            cl = get_class(var)
            number_of_lessions = cl.course.number_of_lessions_per_week
            if value + number_of_lessions - 1 > 24:
                self.prune(var, value, None)
                continue
            for i in range (number_of_lessions):
                timeslots.append(value + i)
            local_assignment[var] = timeslots
            if self.consistent(var, local_assignment):
                removals = self.suppose(var, value)
                if inferences(self, var, value, local_assignment, removals):
                    result = self.backtracking(local_assignment)
                    if result is not None:
                        return result
                self.restore(removals)
        return None 


def in_one_section(variable, value):
    cl = get_class(variable)
    start = value % 5
    end =  (value + cl.course.number_of_lessions_per_week - 1) % 5

    if end < start:
        return False
    return True