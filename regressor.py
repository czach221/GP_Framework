from genetic import Genetic
import fitness
import expr_tree
import population as pop
import numpy as np
import sympy as sp

class Regressor:
    def __init__(self, x_data, y_data, generations, preorder_length):
        self.x_data = x_data
        self.y_data = y_data
        self.population_size = 100
        self.preorder_length = preorder_length
        self.dimension = len(x_data[0])
        self.character_list = [['operations', 1], ['variables', 3], ['constants', 1]]
        self.generations = generations
        self.num_crossover = 100

    def regressor(self):
        
        # create the first population
        population = pop.Population_Generator.generate_random_valid_preorder_population(self.population_size, self.preorder_length, self.dimension, self.character_list)

        for _ in range(self.generations):
            
            # population gets crossed over every generation
            fitnesses = fitness.Fitness.get_populations_fitness(population, self.x_data, self.y_data)
            population = Genetic.crossover_population(population, fitnesses, self.num_crossover, self.dimension, self.preorder_length, True, True)

        return population