from sympy import *
import numpy as np
import numbers
import warnings

class Fitness():
    #'''
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
        if y_mean == 'inf': return ''#################################### wie kann ich das programm hier abbrechen lassen
        # Create a lambdified function for faster evaluation
        x_symbs = [symbols(f'x_{i}') for i in range(len(x_data[0]))]
        try:
            exec_func = lambdify(x_symbs, func, modules="numpy")
        except KeyError as k:
            print(func)
            return float(-1e7)

        # Transform the x_data list, to n-dimension list, with the values of each dimension/varaible
        x_data = np.array(x_data)
        t=([x_data[:, i] for i in range(x_data.shape[1])])
        
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            y_pred = exec_func(*[x_data[:, i] for i in range(x_data.shape[1])])
            if isinstance(y_pred, numbers.Number):
                y_pred = y_pred * np.ones(len(x_data))
            if not np.all(np.isfinite(y_pred)) or isinstance(y_pred, complex): 
                return float(-1e7)
         

        # Calculate the sum of squares of residuals (SSR) and total sum of squares (SST)
        sum_func = np.sum((np.array(y_data) - np.array(y_pred)) ** 2)
        sum_mean = np.sum((np.array(y_data) - y_mean) ** 2)

        # Calculate the R² error
        r2 = 1 - (sum_func / sum_mean) if sum_mean != 0 else float('inf')
        return r2
'''
    def calculate_fitness(x_data, y_data, y_pred):
        y_mean = np.mean(y_data)
        sum_func = np.sum((y_data - y_pred) ** 2)
        sum_mean = np.sum((y_data - y_mean) ** 2)
        r2 = 1 - (sum_func / sum_mean) if sum_mean != 0 else float('inf')
        return r2

    @staticmethod
    def calculate_r2(x_data, y_data, func):
        x_symbs = [symbols(f'x_{i}') for i in range(len(x_data[0]))]
        exec_func = lambdify(x_symbs, func, modules="numpy")
        x_data = np.array(x_data)
        y_pred = exec_func(*[x_data[:, i] for i in range(x_data.shape[1])])
        if isinstance(y_pred, numbers.Number):
            y_pred = y_pred * np.ones(len(x_data))
        if not np.all(np.isfinite(y_pred)): 
            return float(-1e7)
        return Fitness.calculate_fitness(x_data, y_data, y_pred)
        '''

