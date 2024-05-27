import fitness
import expr_tree


class Population():


    def populationCreator(population_size, individuum_size, operators):
        population = []
        


class Organism():
    def __init__(self, preorder_list):
        
        self.preorder_list = preorder_list
        self.fitness = None
        self.ExprTree = expr_tree.ExprTree
        
    def calculate_fitness(self, data, target):
        """
        Berechnet die Fitness des Organismus basierend auf den gegebenen Daten und Zielwerten.
        
        Params:
            data... numpy array mit den Eingabedaten
            target... numpy array mit den Zielwerten
        """
        tree = self.ExprTree(self.preorder_list)
        self.fitness = fitness.calculate(tree, data, target)
        return self.fitness

    def get_symbolic_expression(self):
        """
        Gibt den symbolischen Ausdruck des Baums zurück.
        """
        tree = self.ExprTree(self.preorder_list)
        return tree.evaluate_symb()

    def compare(self, other):
        """
        Vergleicht die Fitness dieses Organismus mit einem anderen.
        
        Params:
            other... der andere Organismus zum Vergleich
        Returns:
            -1, 0, oder 1 wenn dieser Organismus eine niedrigere, gleiche oder höhere Fitness hat.
        """
        if self.fitness < other.fitness:
            return -1
        elif self.fitness > other.fitness:
            return 1
        else:
            return 0