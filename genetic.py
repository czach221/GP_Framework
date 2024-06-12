import sympy
import random
from expr_tree import Validator
import fitness
import population


class genetic():
    @staticmethod
    def crossover(parent1 : population.Organism, parent2 : population.Organism, max_lenght, dimension, only_valid=False):
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
        if len(parent1) < max_lenght:
            preorder_parent1 = parent1.get_preoder()
            # using generate_random_preorder to generate a short preorder in the length of the difference between max_length and the length of the preorder
            fill_up_char = population.Population.generate_random_preorder(1, max_lenght-len(parent1), dimension, [['operations', 2], ['variables', 3], ['constants', 1]])
            preorder_parent1.append(fill_up_char[0].get_preorder())
        else: 
            preorder_parent1 = parent1.get_preorder()

        if len(parent2) < max_lenght:
            preorder_parent2 = parent2.get_preorder()
            fill_up_char = population.Population.generate_random_preorder(1, max_lenght-len(parent1), 1, [['operations', 2], ['variables', 3], ['constants', 1]])
            preorder_parent2.append(fill_up_char[0].get_preorder())
        else: 
            preorder_parent2 = parent2.get_preorder() 

        new_preorder = [
            random.choice([preorder_parent1[i], preorder_parent2[i]]) for i in range(max_lenght)
        ]
        organism = population.Organism(new_preorder)

        if only_valid:
            if organism.is_valid:
                return organism
        else:
            return organism

   