import numpy as np
import fitness
import genetic
import population as pop
import expr_tree
import sympy as sp
import regressor
from pyinstrument import Profiler

class GP_main(): 

    tests = [
            (['+','*','*' ,'*', 'x_0', 'x_0', 'x_0', 2, '*', 2, 'x_0'], "2x³ + 2x"),
            (['*','*' ,'*', 'x_0', 'x_0', 'x_0', 2,], "2x³"),
            (['+', 'x_0', 'x_1'], "Simple addition"),
            (['*', 'x_0', 'x_1'], "Simple multiplication"),
            (['+', '*', 'x_0', 'x_0', 3], "Quadratic addition with constant"),
            (['sin', 'x_0'], "Sine function"),
            (['cos', 'x_0'], "Cosine function"),
            (['tan', 'x_0'], "Tangent function"),
            (['exp', 'x_0'], "Exponential function"),
            (['log', 'x_0'], "Logarithmic function"),
            (['inv', 'x_0'], "Inverse function"),
            (['neg', 'x_0'], "Negation function"),
            (['+', 'sin', 'x_0', 'cos', 'x_1'], "Sine and Cosine addition"),
            (['*', 'exp', 'x_0', 'log', 'x_1'], "Exponential and Log multiplication"),
            (['+', '*', 'x_0', 2, 'x_1'], "Linear combination with multiplication"),
            (['+', 'x_0', 'x_1'], "Subtraction"),
            (['+', '*', 'x_0', 'x_1', '*', 'x_0', 'x_1'], "Multiplication and addition"),
            (['tan', 'cos', 'x_0'], "Nested trigonometric functions"),
            (['+', 'exp', 'x_0', 'log', 'x_1'], "Exponential and Logarithmic addition"),
            (['+', 'inv', 'x_0', 'neg', 'x_1'], "Inverse and Negation addition"),
            (['+', '*', 'x_0', 3, '*', 'x_1', 2], "Polynomial addition"),
            (['*', 'sin', 'x_0', 'cos', 'x_1'], "Sine and Cosine subtraction"),
        ]
    

    


    def main():

        # reference function
        x_0 = sp.symbols('x_0')
        cos = sp.cos
        symbolic_function = 2*cos(x_0)+x_0  # -> +, 4, *, 2, cos, x_0
        generated_function = sp.lambdify(x_0, symbolic_function, 'numpy')


        # creating datapoints
        data_x, data_y = fitness.Data().generate_data_points(generated_function, start=-10, end=10, step=1)
        '''
        Params:
        '''
        param1 = [
            data_x, 
            data_y,
            20, # number of generations
            9, # length of each preorder
            50, # size of the population
            [['operations', 1], ['variables', 3], ['constants', 0]], # list of used characters in the preorders
            140 # number of crossovers per generation
                ]

        
    #################################################################################
        # running the regressor
        population, best = regressor.Regressor(param1)
    #################################################################################

        # sorting population by fitness
        sorted_population = population.sort_population_by_fitness()
        # evaluating the best organisms
        for i in range(5):
            organism = sorted_population[i]
            print(organism.get_preorder(), organism.get_symbolic_expression(), '\n', 'fitness: ', organism.get_fitness(data_x, data_y))

        print('best organism overall: ', best.get_preorder(), best.fitness)
        
        
    def test(self, data_x, data_y):

        popul= []
        for preorder,_ in self.tests:
            popul.append(pop.Organism(preorder))
        pop_fit=fitness.Fitness.populations_fitness(popul, data_x, data_y)
        new_popul= genetic.Genetic.crossover_population(pop_fit, 100, len(data_x[0]), 5, True)

        for child in new_popul:
            print(child.get_preorder())
            if child: print(child.get_fitness(data_x, data_y))
                    


if __name__ == "__main__":
    gp = GP_main()  # Instanz der Klasse erstellen
    prof = Profiler()
    prof.start()

    gp.main()
    
    prof.stop()  
    prof.print()

