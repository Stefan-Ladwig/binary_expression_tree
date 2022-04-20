import graphviz
import sympy as sym


class Node():
    def __init__(self, symbol):
        self.symbol = symbol
        self.id = None
        self.level = None
        self.parent = None
        self.children = None

    def set_children(self, left, right):
        self.children = (left, right)
        left.parent = self
        right.parent = self
    
    def _str_subtree(self):
        output = self.symbol
        if self.children != None:
            output += ' ('
            for i, child in enumerate(self.children):
                if i == 1:
                    output += ', '
                output += child._str_subtree()
            output += ') '
        return output

    def _set_level(self, level):
        self.level = level
        if self.children != None:
            for child in self.children:
                child._set_level(level+1)
    
    def _set_id(self, id):
        self.id = id
        if self.children != None:
            for i, child in enumerate(self.children):
                child._set_id(id + str(i))

    def _add_nodes_and_edges_to_graph(self, graph):
        if self.children != None:
            for child in self.children:
                graph.node(child.id, child.symbol)
                graph.edge(self.id, child.id)
                child._add_nodes_and_edges_to_graph(graph)

    def _get_sympy_expr(self, evaluate):
        if self.children == None:
            return sym.symbols(self.symbol)
        
        kids = self.children

        if self.symbol == '+':
            return sym.Add(kids[0]._get_sympy_expr(evaluate), kids[1]._get_sympy_expr(evaluate), evaluate=evaluate)

        if self.symbol == '-':
            return sym.Add(kids[0]._get_sympy_expr(evaluate), sym.Mul(-1, kids[1]._get_sympy_expr(evaluate)), evaluate=evaluate)

        if self.symbol == '*':
            return sym.Mul(kids[0]._get_sympy_expr(evaluate), kids[1]._get_sympy_expr(evaluate), evaluate=evaluate)

        if self.symbol == '/':
            return sym.Mul(kids[0]._get_sympy_expr(evaluate), sym.Pow(kids[1]._get_sympy_expr(evaluate), -1), evaluate=evaluate)

        if self.symbol == '^':
            return sym.Pow(kids[0]._get_sympy_expr(evaluate), kids[1]._get_sympy_expr(evaluate), evaluate=evaluate)
            

class Tree():
    def __init__(self, root):
        self.root = root
        self.update_level()
        self.update_id()

    def print_prefix(self):
        print(self.root._str_subtree())
    
    def update_level(self):
        self.root._set_level(0)

    def update_id(self):
        self.root._set_id('0')

    def generate_graph(self):
        graph = graphviz.Digraph('graph')
        graph.node(self.root.id, self.root.symbol)
        self.root._add_nodes_and_edges_to_graph(graph)
        return graph

    def get_sympy_expr(self, evaluate):
        return self.root._get_sympy_expr(evaluate)
