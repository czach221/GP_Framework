class Params:     
    def __init__(self, params):
        self.x_data = params[0]
        self.y_data = params[1]
        self.generations = params[2]
        self.preorder_length = params[3]
        self.population_size = params[4]
        self.character_list = params[5]
        self.num_crossover = params[6]
        self.dimension = len(self.x_data[0])
        
    def __repr__(self):
        return (f"Params(data_x={self.data_x}, data_y={self.data_y}, num_generations={self.num_generations}, "
                f"preorder_length={self.preorder_length}, population_size={self.population_size}, "
                f"used_characters={self.used_characters}, num_crossovers={self.num_crossovers})")
