import sympy
import random
from expr_tree import Validator
import fitness
import population
import numpy as np

class Genetic():
    @staticmethod
    def crossover(parents, max_length, dimension, only_valid=False):
        """
        Performs a crossover between two parent organisms to create a new organism.

        Params:
            parent1... First parent organism (Organism object)
            parent2... Second parent organism (Organism object)
            only_valid... Boolean indicating whether only valid preorders should be returned

        Returns:
            new_organism... New organism (Organism object) created by crossover
        """
        # we are adding random chars to the end of the parents preorders so its the length of max_lenght

        parent_preorder = []
        for parent in parents:
            if parent.length < max_length:
                # using generate_random_preorder to generate a short preorder in the length of the difference between max_length aiind the length of the preorder
                fill_up_char = population.Population_Generator.generate_random_preorder(1, max_length-parent.length, dimension, [['operations', 2], ['variables', 3], ['constants', 1]])
                
                # adding the filler preorder to the original preorder
                parent_preorder.append(parent.get_preorder() + fill_up_char[0].get_preorder())
            else: 
                parent_preorder.append(parent.get_preorder())
        
        new_preorder = [
            random.choice([parent_preorder[0][i], parent_preorder[1][i]]) for i in range(max_length)
        ]
        organism = population.Organism(new_preorder)

        if only_valid:
            if organism.is_valid:
                return organism
        else:
            return organism

    @staticmethod
    def crossover_population(population, fitnesses, num_crossover, dimension, max_length, allow_duplicates=True, only_valid=False):
        """
        Selects pairs of organisms for crossover based on their weights.

        Args:
            organisms (list): List of organisms.
            fitnesses (list): List of R² fitness values for each organism.
            num_crossover (int): Number of crossover pairs to select.
            allow_duplicates (bool): If True, the same organism can be selected more than once.
                                     If False, each pair will consist of different organisms.

        Returns:
            list: A list of tuples, each containing two organisms selected for crossover.
        """
        # get the list of the organism weights
        weights = fitness.Fitness.population_weights(fitnesses)

        crossover_population = []

        for _ in range(num_crossover):
            if allow_duplicates:
                # select two organismss randomly. duplicates allowed
                parents = np.random.choice(population, size=2, p=weights)

            else: 
                # select two different organism. replace=False removes the previous pick from the list
                parents = np.random.choice(population, size=2, replace=False, p=weights)

            # create crossover between the two parents
            child = Genetic.crossover(parents, max_length, dimension, only_valid)
            if child:
                crossover_population.append(child)

        return crossover_population

   
   