import numpy as np
import fitness
import genetic
import population
import expr_tree
import sympy as sp

class GP_main(): 
    # Example usage
    preorder_list = ['+','+','*','x_0','x_1','*',3,'x_2',2]
    #ExprTreeValidator.is_valid_preorder(preorder_list)
    #root_ = expr_tree.ExprTree(preorder_list).root
    #print(expr_tree.ExprTree(preorder_list)._get_root_from_preorder())
    #print(ExprTreeValidator.is_valid_tree(root_))

    #print(ExprTreeValidator.is_valid_preorder(preorder_list)) 

    expr_tree_ = expr_tree.ExprTree(preorder_list)
    tmp = expr_tree_.evaluate_symb()
    
    #print(tmp)

    x = sp.symbols('x')
    symbolic_function = x**2 + 3*x + 2
    generated_function = sp.lambdify(x, symbolic_function, 'numpy')

    #print(expr_tree_)
    data_points = fitness.Data().generate_data_points(generated_function, start=-10, end=10, step=1)
    #print(data_points)
    
    org_1 = population.Organism(preorder_list)
    tmp_2 = org_1._get_org_preorder()
    root = org_1._get_organism_root()
    #ex = expr_tree.ExprTree()._preorder_tree(root)
    #print(ex)
    #print(tmp_2)
    tmp_1 = org_1._get_fitness(data_points)

    fit = fitness.Fitness.calculate_r2(data_points, symbolic_function)
    print(fit)

    #org_1._get_fitness(data_points)


