import numpy as np
import fitness
import genetic
import population
import expr_tree
import sympy as sp

class GP_main(): 
    # Example usage
    preorder_list = ['+','*','x_0','x_0','*', 3, 'x_0']
    #ExprTreeValidator.is_valid_preorder(preorder_list)
    #root_ = expr_tree.ExprTree(preorder_list).root
    #print(expr_tree.ExprTree(preorder_list)._get_root_from_preorder())
    #print(ExprTreeValidator.is_valid_tree(root_))

    #print(ExprTreeValidator.is_valid_preorder(preorder_list)) 

    expr_tree_ = expr_tree.ExprTree(preorder_list)
    tmp = expr_tree_.evaluate_symb()
    
    
    

    x_0 = sp.symbols('x_0')
    symbolic_function = x_0**3 + 3*x_0 + 2*x_0
     
    generated_function = sp.lambdify(x_0, symbolic_function, 'numpy')

    #print(tmp, symbolic_function, generated_function)

    #print(expr_tree_)
    data_x, data_y = fitness.Data().generate_data_points(generated_function, start=-10, end=10, step=1)
    #print(data_x, data_y)
    
    org_1 = population.Organism(preorder_list)
    tmp_2 = org_1.get_preorder()
    root = org_1.get_organism_root()
    symp = org_1.get_symbolic_expression()

    
    
    #is_preorder = expr_tree.Validator.is_valid_preorder(preorder_list)
    
    
    
    
    
    
    #tmp_1 = org_1._get_fitness(data_x, data_y)
    #print(tmp_1)
    
    #fit = fitness.Fitness.calculate_r2(data_x, data_y, symbolic_function)
    #print(fit)

   


    population = population.Population.generate_random_preorder(10000, 5, 1, [['operations', 2], ['variables', 3], ['constants', 1]], True)
    for i, organism in enumerate(population): 
        root_org = expr_tree.ExprTree(organism.get_preorder())
        func_org = root_org.evaluate_symb()
        print('fitness: '+str(organism.get_fitness(data_x, data_y)), '\n', func_org)
        #print(str(root_org.evaluate_symb()), str(i) +"\n")

        #print(str(organism._get_preorder()), str(i) +"\n")
        
    print("population lenght: "+str(len(population)))

