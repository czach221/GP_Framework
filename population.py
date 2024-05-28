import fitness
import expr_tree


class Population():
    
    def populationCreator(population_size, individuum_size, operators):
        population = []
        


class Organism():
    
    def __init__(self, preorder_list):
        
        self.preorder_list = preorder_list
        self.fitness_org = None
        self.root = None

    def _get_fitness(self, data):
        """
        Calculate the fitness of the organism based on the given data and target values.
        
        Params:
            data... numpy array with input data
            func... numpy array with target values
        """
        self.fitness_org = fitness.Fitness.calculate_r2(data, self._get_symbolic_expression)
        return self.fitness_org

    def _get_symbolic_expression(self):
        """
        Returns the symbolic expression of the tree as sympy func
        """
        tree = expr_tree.ExprTree(self.preorder_list)
        return tree.evaluate_symb()

    def _get_organism_root(self):
        '''
        Returns the root of the expressionTree of this organism 
        '''
        root = expr_tree.ExprTree(self.preorder_list)

    def _mutate(self):
        '''
        we create a mutation of the Organism.
        '''

    def _crossover(self, partner_preorder : list):
         """
        Performs a crossover with another organism and returns two offspring.
        
        Params:
            partner_preorder... list from other organism 
        Returns:
            Two new organisms as offspring
        """
    def _get_org_preorder(self):
        '''
        returns the preorder list from this organism, to be used in crossovers for example
        '''
        return self.preorder_list
    
    def _get_pretty_preorder(self) -> str:
        """
        Returns the preorder list in a readable string format.
        """
        return " ".join(map(str, self.preorder_list))


