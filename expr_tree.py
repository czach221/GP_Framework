import numpy as np
import sympy


#################################
#Here we define which operations can be used in the expression tree.
#Variables are named x_0, x_1, ... (no curly braces, x_{11} is x11)
#In order to add a new operation, add it into the dictionaries below.
#################################

# Node arity
NODE_ARITIES = {
    '+' : 2,
    '*' : 2,
    'sin' : 1,
    'cos' : 1,
    'tan' : 1,
    'exp' : 1,
    'log' : 1,
    'inv' : 1,
    'neg' : 1,
}

# Node operation
NODE_OPS = {
    '+' : lambda x, y: x + y,
    '*' : lambda x, y: x * y,
    'sin' : np.sin,
    'cos' : np.cos,
    'tan' : np.tan,
    'exp' : np.exp,
    'log' : np.log,
    'inv' : lambda x: 1/x,
    'neg' : lambda x: -x,
}

# Node operations sympy
NODE_OPS_SYMB = {
    '+' : lambda x, y: x + y,
    '*' : lambda x, y: x * y,
    'sin' : sympy.sin,
    'cos' : sympy.cos,
    'tan' : sympy.tan,
    'exp' : sympy.exp,
    'log' : sympy.log,
    'inv' : lambda x : 1/x,
    'neg' : lambda x: -x,
}

# Translation Sympy -> Tree
SYMPY2OP = {
    sympy.core.add.Add : '+',
    sympy.core.mul.Mul : '*',
    sympy.sin : 'sin',
    sympy.cos : 'cos',
    sympy.tan : 'tan',
    sympy.exp : 'exp',
    sympy.log : 'log',
    'inv' : 'inv',
    'neg' : 'neg'
}


#################################
#Classes for transforming lists into trees
#################################

class Node():

    def __init__(self, op : str):
        '''
        Class for an expression node.
        
        @Params:
            op... string indicator for operation on node (see NODE_OPS)
        '''

        self.is_number = isinstance(op, (int, float, complex)) and not isinstance(op, bool) or op == 'C'
        self.is_var = str(op).startswith('x_') or str(op) == 'var'
        self.is_calc = op in NODE_OPS

        assert self.is_number or self.is_var or self.is_calc, f'Operation {op} not supported at node!'
        self.op = op
        if self.is_calc:
            self.arity = NODE_ARITIES[self.op]
        else:
            self.arity = 0
        self.children = []

        # for comparision of subtrees
        self.eval_result = None

    def evaluate(self, X : np.ndarray, save_res : bool = False) -> np.ndarray:
        '''
        Evaluates the node on data.

        @Params:
            X... array of size (n_samples x dimensionality)
            save_res... If set, each node saves its intermediate result. Built in for subtree comparison. 
        @Returns:
            array of size n_samples
        '''
        assert len(X.shape) == 2, f'Expected 2-dim Data (n_data x n_variables) but got {len(X.shape)} dimensional data instead'
        res = None
        if self.is_var:
            var_idx = int(self.op.split('_')[-1])
            #the index of the variable shouldnt be above the dimension of the array/ the lenght of the function
            assert var_idx < X.shape[1], f'Cannot get {var_idx} of {X.shape[1]}-dimensional data!'
            res = X[:, var_idx]

        elif self.is_number:
            res = self.op*np.ones(len(X))
        else:
            #we check if the number of children of the op is equal to the number of children the arity should have (from the dict above) 
            arity = self.arity
            assert len(self.children) == arity, f'Node {self.op} has arity {arity} but {len(self.children)} children!'
            if arity == 1:
                v1 = self.children[0].evaluate(X, save_res)
                res =  NODE_OPS[self.op](v1)
            elif arity == 2:
                v1 = self.children[0].evaluate(X, save_res)
                v2 = self.children[1].evaluate(X, save_res)
                res = NODE_OPS[self.op](v1, v2)
            else:
                # We should never get here
                raise AssertionError(f'Nodes with arity {arity} are not supported')
        if save_res:
            self.eval_result = res
        return res

    def evaluate_symb(self, save_res : bool = False) -> sympy.Expr:
        '''
        Evaluates the node symbolically.

        @Params:
            consts... array that contains values for placeholder constants (nodes c_i)
            save_res... If set, each node saves its intermediate result. Built in for subtree comparison. 
        @Returns:
            array of size n_samples
        '''
        res = None
        if self.is_var:
            res = sympy.sympify(self.op)
        elif self.is_number:
            res = self.op
        else:
            arity = self.arity
            assert len(self.children) == arity, f'Node {self.op} has arity {arity} but {len(self.children)} children!'
            if arity == 1:
                v1 = self.children[0].evaluate_symb(save_res)
                res =  NODE_OPS_SYMB[self.op](v1)
            elif arity == 2:
                v1 = self.children[0].evaluate_symb(save_res)
                v2 = self.children[1].evaluate_symb(save_res)
                res = NODE_OPS_SYMB[self.op](v1, v2)
            else:
                # We should never get here
                raise AssertionError(f'Nodes with arity {arity} are not supported')
        if save_res:
            self.eval_result = res
        return res

class ExprTree():

    def __init__(self, node_list):
        '''
        Class for an expression tree.
        
        @Params:
            node_list... list of node operations in preorder
        '''
        
        self.node_list = node_list

        self.nodes = None # nodes in preorder
        self.root = None # reference to root
        self.depth = 0
        
        if (self.node_list is not None):
            self._init_from_preorder()

    def _get_root_from_preorder(self):
        '''
        Public method to initialize tree from preorder list and return the root node.
        
        @Params:
            node_list... list of node operations in preorder
        @Returns:
            root node of the tree
        '''
        node_list = self.node_list
        self._init_from_preorder()
        return self.root


    def evaluate(self, X : np.ndarray, save_res : bool = False) -> np.ndarray:
        '''
        Evaluates the tree on data.

        @Params:
            X... array of size (n_samples x dimensionality)
            save_res... If set, each node saves its intermediate result. Built in for subtree comparison. 
        @Returns:
            array of size n_samples
        '''

        assert self.root is not None, 'Tree is not initialized'
        return self.root.evaluate(X, save_res)

    def evaluate_symb(self, save_res : bool = False) -> sympy.Expr:
        '''
        Evaluates the tree symbolically.

        @Params:
            save_res... If set, each node saves its intermediate result. Built in for subtree comparison. 
        @Returns:
            array of size n_samples
        '''

        assert self.root is not None, 'Tree is not initialized'
        return self.root.evaluate_symb(save_res)


    def _get_depth(self, node : Node) -> int:
        '''
        Recursively evaluates depth of tree with given node as root.
        For a tree with one node we have depth = 0.

        @Params:
            node... root node

        @Returns:
            depth of tree starting at root node
        '''

        if len(node.children) == 0:
            return 0
        else:
            return max([self._get_depth(c) for c in node.children]) + 1
    
    def _get_nodes_preorder(self) -> list:
        '''
        Retrieves the tree as list of nodes in preorder

        @Returns:
            List of nodes
        '''

        assert self.root is not None, 'Tree is not initialized'
        return self._preorder_tree(self.root)

    def _preorder_tree(self, node : Node) -> list:
        '''
        Retrieves the tree from a given root as list of nodes in preorder

        @Returns:
            List of nodes
        '''
        ret = [node]
        for c in node.children:
            ret += self._preorder_tree(c)
        return ret

    def _init_from_preorder(self):
        '''
        Given a token list, initializes tree.
        Assumes tokens to be in preorder.
        '''

        nodes = []
        # 1. create nodes
        for op in self.node_list:
            nodes.append(Node(op))
        
        # 2. set children
        try:
            self._set_children(nodes, 0)
        except IndexError:
            raise AssertionError('Nodes do not seem to be in a valid preorder!')

        # 3. update lists
        self.root = nodes[0]
        self.depth = self._get_depth(self.root)
        self.nodes = self._get_nodes_preorder()
        self.expr = self.evaluate_symb()
    
    def _set_children(self, nodes : list, idx : int) -> int:
        '''
        Given a list of nodes and the index of the current node, recursively sets children for all nodes
        in subtree.

        @Params:
            nodes... list of nodes
            idx... index of root node

        @Returns:
            index of next node (sibling)
        '''


        current_node = nodes[idx]
        for _ in range(current_node.arity):
            current_node.children.append(nodes[idx+1])
            idx = self._set_children(nodes, idx + 1)
        return idx

   
    
    
class Validator():       
    @staticmethod
    def is_valid_preorder(preorder : list) -> bool:
        """
        Check if the given preorder list represents a valid expression tree.
        
        Params:
            node_list... list of node operations in preorder
        Returns:
            True if valid, False otherwise
        """

        stack = []

        # root has to be a operation if theres more than one op
        if preorder[0] not in NODE_OPS and len(preorder) > 1:
            return False

        # initialize the stack
        if preorder[0] in NODE_OPS:
            arity = NODE_ARITIES[preorder[0]]
            stack.append(arity)

        for i, op in enumerate(preorder[1:]):
            # stack shoulndt be empty if there is still a op left
            if not stack:
                return True

            # op is an operation -> adding the amount of availiable children knots from the operation
            if op in NODE_OPS:
                arity = NODE_ARITIES[op]
                stack.append(arity)
            
            else:
                # op is a nubmer or variable -> substracting 1 from the availiable children 
                stack[-1] -= 1
                while stack and stack[-1] == 0:
                    stack.pop()
                    if stack:
                        stack[-1] -= 1
            
        # stack should be empty
        return len(stack) == 0
         

    def is_valid_tree(self, node : Node):
        """
        Check if the given node represents a valid expression tree.
        
        Params:
            node... the root node of the tree
        Returns:
            True if valid, False otherwise
        """

        if node.is_calc:
            # Check if the node has the correct number of children
            if len(node.children) != node.arity:
                return False
            
            # Recursively check each child
            for child in node.children:
                if not Validator.is_valid_tree(child):
                    return False
        
        elif node.is_var or node.is_number:
            # Variables and numbers should not have children
            if len(node.children) != 0:
                return False
        
        else:
            # Unsupported node type
            return False
        
        return True

