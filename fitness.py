import sympy as sp

class fitness():

    def evaluate_function(func_str, x_value):
        x = sp.symbols('x')
        func = sp.sympify(func_str)
        y_value = func.subs(x, x_value)
        return y_value 
    
    def calculate_r2(data_points, func):
        # Berechnung des Durchschnitts der y-Werte
        y_mean = sum(y for _, y in data_points) / len(data_points)

        # Initialisierung der Summen der Quadrate der Residuen (SSR) und der totalen Summe der Quadrate (SST)
        sum_func = 0  # Summe der Quadrate der Residuen
        sum_mean = 0  # Totale Summe der Quadrate

        for x, y in data_points:
            y_pred = fitness.evaluate_function(func, x)  # Vorhergesagter y-Wert durch die Funktion
            sum_func += (y - y_pred) ** 2  # Summe der Quadrate der Residuen
            sum_mean += (y - y_mean) ** 2  # Totale Summe der Quadrate

        # Berechnung des R²-Fehlers
        r2 = 1 - (sum_func / sum_mean)
        return r2


       


    def generate_data_points(func, start, end, step):
        data_points = []
        x = start
        while x <= end:
            y = func(x)
            data_points.append((x, y))
            x += step
        return data_points