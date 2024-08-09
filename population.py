import fitness
import expr_tree
import random
import population
import numpy as np

# Node arity
NODE_ARITIES = {
    '+' : 2,
    '*' : 2,
    'sin' : 1,
    'cos' : 1,
    'tan' : 1,
    'exp' : 1,
    'log' : 1,
    'inv' : 1,
    'neg' : 1,
}

class Population_Generator():
    @staticmethod
    def generate_random_valid_preorder_population(population_size, length, dimension, character_list):
        population = []
        operations = ['+', '+', '*', '*', 'exp', 'sin', 'cos', 'tan', 'log', 'inv', 'neg']
        variables = [f'x_{i}' for i in range(dimension)]
        character_list_updated = []
        for character, occurrences in character_list:
            character_list_updated.extend([character] * occurrences)
        random.shuffle(character_list_updated)
        while len(population) < population_size:
            preorder = []
            count = 0  # Counter for tracking required children nodes

            # Ensure the first character is an operation
            first_op = random.choice(operations)
            preorder.append(first_op)
            count += NODE_ARITIES[first_op] 

            print(len(population))
            
            while len(preorder) < length:
                remaining_positions = length - len(preorder)
                character = random.choice(character_list_updated)

                if count == 1 and remaining_positions > 1:
                    character = 'operations'
                elif count == remaining_positions: 
                    character = random.choice(['variables', 'constants'])

                if character == 'operations':
                    op = random.choice(operations)
                    arities = expr_tree.NODE_ARITIES[op]

                    if count + arities <= remaining_positions:
                        preorder.append(op)
                        count += arities - 1 ###### kann es sein das bei *, + nicht -1 gemacht wwerden soll?
                    else:
                        continue
                elif character == 'variables':
                    preorder.append(random.choice(variables))
                    count -= 1
                elif character == 'constants':
                    preorder.append(random.randint(1, 9))
                    count -= 1
                else:
                    return 'character not compatible'

                

            if count <= 0 and len(preorder) == length:
                organism = Organism(preorder)
                if organism.is_valid:
                    population.append(organism)

        return population 
    
    def generate_random_valid_preorder_population1(population_size : int, length : int, dimension : int, character_list : list):
        '''
        generate an x amount of valid organisms, with a random function in preorder.

        Params:
            population_size... size of population
            lenght... amount of characters in function
            num_variables... 
        '''
        population = []
        
        operations = ['+','*' ,'exp', 'sin', 'cos', 'tan', 'log', 'inv', 'neg', '*', '+']
        #operations = ['+','+','*','*', '+']


        # allows different dimensions for variables so x_0, x_1, x_2,... instead of x, a, b, ...
        variables = [f'x_{i}' for i in range(dimension)]
        
        # this list contains all the different characters allowed to use, with diff occurences 
        character_list_updated = []
        for character, occurences in character_list:
            for _ in range(occurences):
                character_list_updated.append(character)
                
        i = 0
        while len(population) < population_size:
            print(i, len(population))
            i+=1
            preorder = []
            for _ in range(length):
                # choosing the character to add from list
                character = random.choice(character_list_updated)

                if character == 'operations':
                    preorder.append(random.choice(operations))
                elif(character == 'variables'):
                    preorder.append(random.choice(variables))
                elif(character == 'constants'):
                    preorder.append(random.randint(1,9))
                else:
                    return 'character not compatible'
                
            # createds new organism with the preorder 
            organism = Organism(preorder)

            # in case only the valid preorders are searched for 
            
            if organism.is_valid:
                population.append(organism)
            
        return population

    def generate_random_preorder(population_size : int, length : int, num_variables : int, character_list : list, only_valid : bool= None):
        '''
        generate an x amount of organisms, with a random function in preorder.

        Params:
            population_size... size of population
            lenght... amount of characters in function
            num_variables... 
        '''
        population = []
        
        operations = ['+','*' ,'exp', 'sin', 'cos', 'tan', 'log', 'inv', 'neg', '*', '+']
        #operations = ['+','+','*','*', '+']


        # allows different dimensions for variables so x_0, x_1, x_2,... instead of x, a, b, ...
        variables = [f'x_{i}' for i in range(num_variables)]
        
        # this list contains all the different characters allowed to use, with diff occurences 
        character_list_updated = []
        for character, occurences in character_list:
            for _ in range(occurences):
                character_list_updated.append(character)
                

        for i in range(population_size):
            preorder = []
            for _ in range(length):
                # choosing the character to add from list
                character = random.choice(character_list_updated)

                if character == 'operations':
                    preorder.append(random.choice(operations))
                elif(character == 'variables'):
                    preorder.append(random.choice(variables))
                elif(character == 'constants'):
                    preorder.append(random.randint(1,9))
                else:
                    return 'character not compatible'
                
            # createds new organism with the preorder 
            organism = Organism(preorder)

            # in case only the valid preorders are searched for 
            if only_valid:
                if organism.is_valid:
                    population.append(organism)
            else: population.append(organism)

            print(i, len(population))
        return population
    



class Organism():
    
    def __init__(self, preorder_list):
        self.preorder_list = preorder_list
        self.fitness = None
        self.root = None
        self.is_valid = expr_tree.Validator.is_valid_preorder(preorder_list)
        self.length = len(preorder_list)
        self.func = None
        if self.is_valid:
            self.func = expr_tree.ExprTree(self.preorder_list).expr

        
    def get_fitness(self, data_x, data_y):
        """
        Calculate the fitness of the organism based on the given data and target values.
        
        Params:
            data... numpy array with input data
            func... numpy array with target values
        
        Returns fitness of organism
        """
        if self.fitness: return self.fitness

        self.fitness = fitness.Fitness.calculate_r2(data_x, data_y, self.func)
        if not isinstance(self.fitness, (int, float)) or self.fitness == 'NaN': self.fitness = -1e7
        
        return self.fitness

    def get_symbolic_expression(self):
        """
        Returns the symbolic expression of the tree as sympy func
        """
        return self.func

    def get_organism_root(self):
        '''
        Returns the root of the expressionTree of this organism 
        '''
        root = expr_tree.ExprTree(self.preorder_list)

    def get_preorder(self):
        '''
        returns the preorder list from this organism, to be used in crossovers for example
        '''
        return self.preorder_list
    
    def set_preorder(self, preorder):
        '''
        overrides the old preorder with a new one
        '''
        self.preorder_list = preorder
        self.func = expr_tree.ExprTree(self.preorder_list).evaluate_symb()

    def get_pretty_preorder(self) -> str:
        """
        Returns the preorder list in a readable string format.
        """
        return " ".join(map(str, self.preorder_list))

    
class Population():

    def __init__(self, x_data, y_data, population_list = []) -> None:
        self.x_data, self.y_data = x_data, y_data
        self.population_list = population_list
        self.fitness = self.get_populations_fitness()
        
    def add_organism(self, organism : Organism):
        self.population_list.append(organism)

    def add_population(self, population : list):
        self.population_list = population

    def add_organism_as_preorder(self, preorder : list):
        organism = Organism(preorder)
        self.population_list.append(organism)

    def get_populations_fitness(self):
        '''
        returns an array with all the organisms of the population and their fitness
        '''
        # initialize return dict
        population_fitness = []
        
        for organism in self.population_list:
            fitness = organism.get_fitness(self.x_data, self.y_data) if not organism.fitness else organism.fitness
            population_fitness.append(fitness)

        return population_fitness
    

    def population_weights(self, alpha = 1) -> np.array:
        """
        Calculates the weight of each organism based on its fitness.

        Args:
            organisms_with_fitness (list): A nested list where each element is a list containing an organism and its R² fitness value.

        Returns:
            dict: A dictionary where keys are organisms and values are their weights.
        """
        # calculate v = exp(1 - r2)
        v = np.exp((np.array(self.fitness) - 1) * alpha)
        
        # calculate the sum of all v values
        s = np.sum(v)
        
        # calculate the weights as v / s
        weights = v / s
        
        if not np.all(np.isfinite(weights)) or isinstance(weights, complex): 
            return float(-1e7)

        return weights

    def sort_population_by_fitness(self):
        """
        Sorts the list of organisms based on the corresponding fitness values.

        Args:
            population (list): List of organisms.
        Returns:
            list: Sorted list of organisms based on fitness values.
        """

        # Combine organisms and fitnesses into a list of tuples
        combined = list(zip(self.population_list, self.fitness))
        
        # Sort the combined list by the fitness values (second element of the tuple)
        sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
        
        # seperate 
        sorted_organisms = [item[0] for item in sorted_combined]

        return sorted_organisms
    
    def get_length(self)-> int:
        """
        Retruns the length of the population
        """
        return len(self.population_list)
    
    def set_population(self, population : list):
        self.population_list = population
        self.fitness = self.get_populations_fitness()

    def remove_duplicates(self):
        """
        Removes duplicate organisms based on their preorder lists.

        Returns:
            list: List of unique organisms.
        """
                
        unique_preorders = set()
        unique_population = []

        for organism in self.population_list:
            # Convert preorder list to a tuple
            preorder_tuple = tuple(organism.get_preorder())
            
            # Add the preorder tuple to the set and check for duplicates
            if preorder_tuple not in unique_preorders:
                unique_preorders.add(preorder_tuple)
                unique_population.append(organism)

        return unique_population