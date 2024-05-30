from sympy import * 

class Fitness():
    @staticmethod
    def evaluate_function(func, x_values):
        """
        Evaluates the given function string at the specified x value.

        Args:
            func_str (str): The function as a string.
            x_value (float): The x value at which to evaluate the function.

        Returns:
            float: The evaluated y value.
        """
        # creates hashmap for every i value in x_{i}
        substitutions = {Symbol(f'x_{i}'): x_values[i] for i in range(len(x_values))}
        y_value = func.subs(substitutions)

        return y_value 

    @staticmethod
    def calculate_r2(x_data, y_data, func):
        """
        Calculates the R² (coefficient of determination) for the given data points and function.

        Args:
            data_points (list of tuple): A list of (x, y) data points.
            func (str): The function as a string.

        Returns:
            float: The R² value indicating the goodness of fit.
        """
        #func should be a sympy function
        if isinstance(func, str):
            func = sympify(func)

        # Calculate the mean of the y values
        
        y_mean = sum(y_data) / len(y_data)

        # Initialize the sum of squares of residuals (SSR) and total sum of squares (SST)
        sum_func = 0  # Sum of squares of residuals
        sum_mean = 0  # Total sum of squares

        for x_values, y in zip(x_data, y_data):
            y_pred = Fitness.evaluate_function(func, x_values)  # Predicted y value by the function
            sum_func += (y - y_pred) ** 2  # Sum of squares of residuals
            sum_mean += (y - y_mean) ** 2  # Total sum of squares

        # Calculate the R² error
        r2 = 1 - (sum_func / sum_mean)
        
        return r2


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
            list of tuple: A list of (x, y) data points.
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