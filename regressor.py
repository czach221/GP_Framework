from genetic import Genetic
import fitness
import expr_tree
import population as pop
import numpy as np
import sympy as sp

class Regressor():
    def __init__(self, x_data, y_data, generations, preorder_length):
        self.x_data = x_data
        self.y_data = y_data
        self.population_size = 1000
        self.preorder_length = preorder_length
        self.dimension = len(x_data[0])
        self.character_list = [['operations', 1], ['variables', 3], ['constants', 0]]
        self.generations = generations
        self.num_crossover = 100

    def regressor(self):
        
        # create the first population
        OG_popul = pop.Population_Generator.generate_random_valid_preorder_population(self.population_size, self.preorder_length, self.dimension, self.character_list)
        popul = pop.Population(OG_popul, self.x_data, self.y_data)
        for i in range(self.generations):
            
            # population gets crossed over every generation
            crossover_population = Genetic.crossover_population(popul, self.num_crossover, self.dimension, self.preorder_length, False, True)
            popul.set_population(crossover_population)
            print(i)
            #sort = popul.sort_population_by_fitness()
            #print(sort[0].get_preorder(), sort[0].get_fitness(self.x_data, self.y_data), '\ncount: ', i)
        return popul