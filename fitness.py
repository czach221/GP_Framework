from sympy import *
import numpy as np
import numbers
import warnings

class Fitness():
    @staticmethod
    def calculate_r2(x_data, y_data, func):
        """
        Calculates the R² (coefficient of determination) for the given data points and function.

        Args:
            x_data (list of lists): A list of lists of x values.
            y_data (list): A list of y values.
            func (sympy.Expr): The function as a sympy expression.

        Returns:
            float: The R² value indicating the goodness of fit or a large error value if evaluation fails.
        """
        #func = sympify(func)

        # Calculate the mean of the y values
        y_mean = np.mean(y_data)

        # Create a lambdified function for faster evaluation
        x_symbs = [symbols(f'x_{i}') for i in range(len(x_data[0]))]
        exec_func = lambdify(x_symbs, func, modules="numpy")

        # Transpose x_data to match the expected input format for lambdify
        x_data_transposed = list(map(list, zip(*x_data)))
        x_data = np.array(x_data)
        t=([x_data[:, i] for i in range(x_data.shape[1])])
        
        with warnings.catch_warnings():
            warnings. simplefilter('ignore')
            y_pred = exec_func(*[x_data[:, i] for i in range(x_data.shape[1])])
            if isinstance(y_pred, numbers.Number):
                y_pred = y_pred * np.ones(len(x_data))
            if not np.all(np.isfinite(y_pred)): 
                return float(-1e7)
         

        # Calculate the sum of squares of residuals (SSR) and total sum of squares (SST)
        sum_func = np.sum((np.array(y_data) - np.array(y_pred)) ** 2)
        sum_mean = np.sum((np.array(y_data) - y_mean) ** 2)

        # Calculate the R² error
        r2 = 1 - (sum_func / sum_mean) if sum_mean != 0 else float('-inf')
        return r2

    @staticmethod
    def populations_fitness(population, x_data, y_data):
        '''
        returns an array with all the organisms of the population and their fitness
        '''
        # initialize return dict
        population_fitness = {}

        for organism in population:
            fitness = organism.get_fitness(x_data, y_data)
            population_fitness[organism] = fitness

        return population_fitness

    @staticmethod
    def population_weights(populations_fitness : dict) -> dict:
        """
        Calculates the weight of each organism based on its fitness.

        Args:
            organisms_with_fitness (list): A nested list where each element is a list containing an organism and its R² fitness value.

        Returns:
            dict: A dictionary where keys are organisms and values are their weights.
        """
         
        fitnesses = list(populations_fitness.values())
    
        # calculate v = exp(1 - r2)
        v = np.exp(np.array(fitnesses) - 1)
        
        # calculate the sum of all v values
        s = np.sum(v)
        
        # calculate the weights as v / s
        weights = v / s
        
        return weights




class Data():
    @staticmethod
    def generate_data_points(func, start, end, step) -> list: ##### -> muss noch angepasst werden, bei unterschiedlichen x_ auch unterschiedliche variablen einzuberechnen
        """
        Generates data points by evaluating the given function over a range of x values.

        Args:
            func (callable): The function to evaluate.
            start (float): The starting value of x.
            end (float): The ending value of x.
            step (float): The step size for x values.

        Returns:
            list of y values: A list of y data points.
            list of x values: A 2 dimensional list of x values, allows multiple x values 
        """

        
        data_points_y = []
        data_points_x = []
        x = start

        while x <= end:
            y = func(x)
            data_points_y.append(y)
            data_points_x.append([x, x/2])
            x += step

        return data_points_x, data_points_y
    
    @staticmethod
    def generate_data_points_sympy(func, start, end, step) -> list:
        """
        Generates data points by evaluating the given sympy function over a range of x values.

        Args:
            func (sympy.Expr): The sympy function to evaluate.
            start (float): The starting value of x.
            end (float): The ending value of x.
            step (float): The step size for x values.

        Returns:
            list of tuple: A list of (x, y) data points.
        """
        data_points_y = []
        data_points_x = []
        x = symbols('x')

        current = start

        while current <= end:
            y = func.subs(x, current)
            data_points_y.append((current, float(y)))  # Convert sympy Float to Python float
            data_points_x.append()
            current += step

        return data_points_x, data_points_y