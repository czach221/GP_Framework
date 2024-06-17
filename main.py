import numpy as np
import fitness
import genetic
import population
import expr_tree
import sympy as sp

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
    

    


    def main(self):

        # Example usage
        preorder_list = ['+','*','x_0','x_0','*', 3, 'x_0']
        
        expr_tree_ = expr_tree.ExprTree(preorder_list)
        tmp = expr_tree_.evaluate_symb()
        
        
        

        x_0 = sp.symbols('x_0')
        cos = sp.cos
        symbolic_function = 2*cos(x_0)**3
        generated_function = sp.lambdify(x_0, symbolic_function, 'numpy')

       

        
        data_x, data_y = fitness.Data().generate_data_points(generated_function, start=1, end=100, step=0.5)
        #print(data_x, data_y)
        
        org_1 = population.Organism(preorder_list)
        tmp_2 = org_1.get_preorder()
        root = org_1.get_organism_root()
        symp = org_1.get_symbolic_expression()


        preorder_liste = [['+', '*', '*', 'x_0', 'x_0', 4, 7]]  
        

        self.test(data_x, data_y)


        #self.ppl = population.Population.generate_random_preorder(100, 5, 1, [['operations', 1], ['variables', 3], ['constants', 1]], True)
        
        
    def test(self, data_x, data_y):

        """
        i = 0
        for preord, description in self.tests: 
            organism = population.Organism(preord)
            root_org = expr_tree.ExprTree(organism.get_preorder())
            func_org = root_org.evaluate_symb()
            print('fitness: '+str(organism.get_fitness(data_x, data_y)), '\n', func_org, description)
            #print(str(root_org.evaluate_symb()), str(i) +"\n")

            print(str(organism.get_preorder()), str(i) +"\n")
            i += 1
        print("population lenght: "+str(len(self.tests)))
        """

        #population = population.Population.generate_random_preorder(1000, 5, 1, [['operations', 1], ['variables', 3], ['constants', 1]], True)
        popul= []
        for preorder,_ in self.tests:
            popul.append(population.Organism(preorder))
        pop_fit=fitness.Fitness.populations_fitness(popul, data_x, data_y)
        new_popul= genetic.Genetic.crossover_population(pop_fit, 10, len(data_x[0]), 5, True)

        for child in new_popul:
            print(child.get_preorder())
            
            if child: print(child.get_fitness(data_x, data_y))
                    


if __name__ == "__main__":
    gp = GP_main()  # Instanz der Klasse erstellen
    gp.main()  

