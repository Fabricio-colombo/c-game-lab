# game_py/genetic.py
from ai_player import AIPlayer
import numpy as np

class GeneticAlgorithm:
    def __init__(self, pop_size=30, input_size=3):
        self.pop_size = pop_size
        self.input_size = input_size
        self.population = [AIPlayer(input_size) for _ in range(pop_size)]
        self.generation = 1

    def select_parents(self, fitnesses):
        indices = np.argsort(fitnesses)[::-1]
        selected = indices[:len(indices) // 2]
        return [self.population[i] for i in selected]

    def evolve(self, fitnesses):
        best_index = np.argmax(fitnesses)
        best_player = self.population[best_index]

        parents = self.select_parents(fitnesses)
        new_population = []

        mutation_rate = max(0.1, 1.0 / self.generation)

        while len(new_population) < self.pop_size:
            p1, p2 = np.random.choice(parents, 2, replace=False)
            child = p1.crossover(p2)
            child.mutate(rate=mutation_rate)
            new_population.append(child)

        new_population[0] = best_player

        self.population = new_population
        self.generation += 1
