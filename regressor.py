from genetic import Genetic
import fitness
import expr_tree
import population as pop
import numpy as np
import sympy as sp

class Regressor():
    def __init__(self, params):
        self.x_data = params[0]
        self.y_data = params[1]
        self.generations = params[2]
        self.preorder_length = params[3]
        self.population_size = params[4]
        self.character_list = params[5]
        self.num_crossover = params[6]
        self.dimension = len(self.x_data[0])

        self.regressor()
        
        
    def regressor(self):
        
        # create the first population
        OG_popul = pop.Population_Generator.generate_random_valid_preorder_population(self.population_size, self.preorder_length, self.dimension, self.character_list)
        popul = pop.Population(self.x_data, self.y_data, OG_popul)

        # choosse a random org as best org
        best_org = popul.population_list[0]

        for i in range(self.generations):
            
            # population gets crossed over every generation
            crossover_population = Genetic.crossover_population(popul=popul, num_crossover=self.num_crossover, dimension=self.dimension, max_length=self.preorder_length, alpha=1, allow_duplicates=False, only_valid=True)
            popul.set_population(crossover_population)
            unique_popul = popul.remove_duplicates()
            add_popul = pop.Population_Generator.generate_random_valid_preorder_population(self.population_size - len(unique_popul), self.preorder_length, self.dimension, [['operations', 2], ['variables', 2], ['constants', 0]])

            new_popul = unique_popul +  add_popul
            popul.set_population(new_popul)

            # sort organisms and save the best organism
            best_of_current_gen = popul.sort_population_by_fitness()
            best_current_org = best_of_current_gen[-1]
            if best_current_org.fitness > best_org.fitness: best_org = best_current_org
                

            print(i)

        """
            sort = popul.sort_population_by_fitness()
            print(sort[0].get_preorder(), sort[0].get_fitness(self.x_data, self.y_data), '\ncount: ', i)
             """
        # return the last population and the best organism
        return popul, best_org