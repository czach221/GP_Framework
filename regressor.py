from genetic import Genetic
import fitness
import expr_tree
import population as pop
import numpy as np
import sympy as sp
import params

class Regressor():
    def __init__(self, params: params.Params):
        self.x_data = params.x_data
        self.y_data = params.y_data
        self.generations = params.generations
        self.preorder_length = params.preorder_length
        self.population_size = params.population_size
        self.character_list = params.character_list
        self.num_crossover = params.num_crossover
        self.dimension = params.dimension
        
        
    def regressor(self):
        
        # create the first population
        OG_popul = pop.Population_Generator.generate_random_valid_preorder_population(self.population_size, self.preorder_length, self.dimension, self.character_list)
        popul = pop.Population(self.x_data, self.y_data, OG_popul)

        # choosse a random org as best org
        best_org = popul.population_list[0]

        for i in range(self.generations):
            
            # population gets crossed over every generation
            crossover_population = Genetic.crossover_population(popul=popul, num_crossover=self.num_crossover, dimension=self.dimension, max_length=self.preorder_length, alpha=1, allow_duplicates=True, only_valid=True)
            popul.set_population(crossover_population)

            # create a unique population, without duplicates
            unique_popul = popul.remove_duplicates()

            add_popul = pop.Population_Generator.generate_random_valid_preorder_population(self.population_size - len(unique_popul), self.preorder_length, self.dimension, [['operations', 1], ['variables', 2], ['constants', 0]])

            new_popul = unique_popul +  add_popul
            popul.set_population(new_popul)

            # sort organisms and save the best organism
            best_of_current_gen = popul.sort_population_by_fitness()
            best_current_org = best_of_current_gen[0]
            if best_current_org.fitness > best_org.fitness: 
                best_org = best_current_org
                print('new best')
            print(best_org.get_preorder(), best_org.fitness)    
            print(i)

            # quit the loop if the organism with fitness 1 has been found (best fitness)
            if best_org.fitness == 1: return popul, best_org     
            
        """
            sort = popul.sort_population_by_fitness()
            print(sort[0].get_preorder(), sort[0].get_fitness(self.x_data, self.y_data), '\ncount: ', i)
             """
        # return the last population and the best organism
        return popul, best_org