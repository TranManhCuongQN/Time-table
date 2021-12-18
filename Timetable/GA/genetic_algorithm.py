from copy import deepcopy
from typing import Callable
from random import choices, random
from heapq import nlargest
from statistics import mean

class GeneticAlgorithm():

    def __init__(self, initial_population, threshold, max_generations = 200, mutation_chance = 0.05, crossover_chance = 0.7):
        self.population = initial_population
        self.threshold = threshold
        self.max_generations = max_generations
        self.mutation_chance = mutation_chance
        self.crossover_chance = crossover_chance        
        self.fitness_key: Callable = type(self.population[0]).fitness

    def pick_tournament(self, num_participants):
        participants = choices(self.population, k=num_participants)
        return tuple(nlargest(2, participants, key=self.fitness_key))
    
    def reproduce(self):
        new_population = []

        while len(new_population) <  len(self.population):
            parents = self.pick_tournament(len(self.population) // 2)

            if random() < self.crossover_chance:
                new_population.append(parents[0].crossover(parents[1]))
            else:
                parent1 = deepcopy(parents[0])
                parent2 = deepcopy(parents[1])
                new_population.append(parent1)
                new_population.append(parent2)            
        if len(new_population) > len(self.population):
            new_population.pop()
        self.population = new_population

    def mutate(self):
        for individual in self.population:
            if random() < self.mutation_chance:
                individual.mutate()

    def run(self):
        best = max(self.population, key=self.fitness_key)

        for generation in range(self.max_generations):
            if best.fitness() >= self.threshold:
                return best            
            print(f"Generation {generation} Best {best.fitness()} Avg {mean(map(self.fitness_key, self.population))}")
            self.reproduce()
            self.mutate()
            highest = max(self.population, key=self.fitness_key)
            if highest.fitness() > best.fitness():
                best = highest
        return best
