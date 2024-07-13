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
    def get_datapoints_from_files(file_name, num_lines, rand_line=False):
        x_data = []
        y_data = []

        # Fester Dateipfad
        base_path = os.path.expanduser('/home/colin-zach/User/Documents/Uni/BA/Datapoints_for_regression/Feynman_with_units')
        file_path = os.path.join(base_path, file_name)


        # Prüfen, ob die Datei existiert
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Die Datei {file_path} wurde nicht gefunden.")

        # Datei öffnen und Zeilen lesen
        with open(file_path, 'r') as file:
            lines = file.readlines()

        total_lines = len(lines)

        # Überprüfen, ob genügend Zeilen vorhanden sind
        if num_lines > total_lines:
            raise ValueError(f"Die Datei enthält nur {total_lines} Zeilen, aber {num_lines} wurden angefordert.")

        # Zufälligen Startwert wählen, wenn rand_line True ist
        start_line = 0
        if rand_line:
            start_line = random.randint(0, total_lines - num_lines)

        # Verarbeiten der ausgewählten Zeilen
        for i in range(start_line, start_line + num_lines):
            line = lines[i]
            # Split the line into numbers
            values = list(map(float, line.split()))
            # The last value is the y_value
            y_value = values[-1]
            # The rest are x_values
            x_values = values[:-1]

            y_data.append(y_value)
            x_data.append(x_values)

        return x_data, y_data




    #x, y = get_datapoints_from_files('1.6.2.txt', 10)
    #print(x, y)
