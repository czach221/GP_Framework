import fitness
import expr_tree
import random



class Population():
    
    def generate_random_valid_preorder_population(population_size : int, length : int, num_variables : int, character_list : list):
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
        variables = [f'x_{i}' for i in range(num_variables)]
        
        # this list contains all the different characters allowed to use, with diff occurences 
        character_list_updated = []
        for character, occurences in character_list:
            for _ in range(occurences):
                character_list_updated.append(character)
                

        while len(population) < population_size:
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
        return population



class Organism():
    
    def __init__(self, preorder_list):
        self.preorder_list = preorder_list
        self.fitness_org = None
        self.root = None
        self.is_valid = expr_tree.Validator.is_valid_preorder(preorder_list)
        self.length = len(preorder_list)
        
    def get_fitness(self, data_x, data_y):
        """s
        Calculate the fitness of the organism based on the given data and target values.
        
        Params:
            data... numpy array with input data
            func... numpy array with target values
        
        Returns fitness of organism
        """
        self.fitness_org = fitness.Fitness.calculate_r2(data_x, data_y, self.get_symbolic_expression())
        return self.fitness_org

    def get_symbolic_expression(self):
        """
        Returns the symbolic expression of the tree as sympy func
        """
        tree = expr_tree.ExprTree(self.preorder_list)
        return tree.evaluate_symb()

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
        preorder = self.preorder_list

    def get_pretty_preorder(self) -> str:
        """
        Returns the preorder list in a readable string format.
        """
        return " ".join(map(str, self.preorder_list))

    
