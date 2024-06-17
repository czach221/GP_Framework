import genetic
import fitness
import expr_tree
import population
import numpy as np
import sympy as sp

class Regressor:
    def __init__(self, x_data, y_data, generations, preorder_length, ):
        self.x_data = x_data
        self.y_data = y_data
        self.population_size = 100
        self.preorder_length = preorder_length
    def regressor(self):
        
        first_population = population.Population.generate_random_valid_preorder_population(self.population_size, )