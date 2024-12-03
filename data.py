import sympy
import os
import random
import pickle

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
            data_points_x.append([x])
            x += step

        return data_points_x, data_points_y
    
    @staticmethod
    def get_datapoints_from_files(file_name, problem_number):
        """
        method to get the datapoints in 2 arrays, from datapoint-files
        input:
            file_name -> name of file [Feynman, Feynman_bonus, Nguyen, Strogatz]
            problem_number -> number of problem 

        return:
            x -> array of x-datapoint (multidimensional)
            y -> array of y-datapoints (results)
            expr -> the real expression we are looking for
        """
       
        path = f'datasets/{file_name}/tasks.p'
        #path = os.path.join(current_dir, 'datasets', file_name, 'tasks.p')
        with open(path, 'rb') as handle:
            task_dict = pickle.load(handle)

        problem_name = list(task_dict.keys())[problem_number]
        x, y, expr = task_dict[problem_name]['X'], task_dict[problem_name]['y'][:, 0], task_dict[problem_name]['expr'][0]

        return x, y, expr
    #get_datapoints_from_files('Feynman', 0)


    #x, y = get_datapoints_from_files('1.6.2.txt', 10)
    #print(x, y)
