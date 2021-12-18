from abc import ABC, abstractmethod

class Chromosome(ABC):
    @abstractmethod
    def fitness(self):
        ...
    
    @classmethod
    @abstractmethod
    def random_instance(cls):
        ...

    @abstractmethod
    def crossover(self, other):
        ...
    
    @abstractmethod
    def mutate(self):
        ...