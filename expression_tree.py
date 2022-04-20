import graphviz
import sympy as sym
import re


def parse_expression(expression: str):
    
    expression = re.sub(r'\s', '', expression)
    expression = re.sub(r'\*{2}', '^', expression)

    operator_dict = {
    'Add': {'+', '-'},
    'Mul': {'*', '/'},
    'Pow': {'^'}
    }

    def check_operator(operators, input):
        bracket_level = 0
        for i, c in enumerate(input):

            if c == '(':
                bracket_level += 1

            elif c == ')':
                bracket_level -= 1

            elif c in operators and bracket_level == 0:
                if i == 0 and c == '-':
                    continue
                return i
        
        return None

    def cleanup(input):
        bracket_level = 0
        if input[0] == '(' and input[-1] == ')':
            for i, c in enumerate(input):
                    
                if c == '(':
                    bracket_level += 1

                elif c == ')':
                    bracket_level -= 1
                    if bracket_level == 0 and i < len(input) - 1:
                        return input
            
            return input[1:-1]
        else:
            return input

    def rec(input):
        input = cleanup(input)
        for operators in ('Add', 'Mul', 'Pow'):
            idx = check_operator(operator_dict[operators], input)
            if idx != None:
                symbol = input[idx]
                node = Node(symbol)
                left_child = rec(input[:idx])
                right_child = rec(input[idx + 1:])
                node.set_children(left_child, right_child)
                return node

        return Node(input.strip())

    return Tree(rec(expression))


class Node():

    def __init__(self, symbol):
        self.symbol = symbol
        self.id = None
        self.level = None
        self.parent = None
        self.children = tuple()


    def set_children(self, left, right):
        self.children = (left, right)
        left.parent = self
        right.parent = self
    

    def _str_subtree(self):
        output = self.symbol
        if self.children:
            output += ' ('
            for i, child in enumerate(self.children):
                if i > 0:
                    output += ', '
                output += child._str_subtree()
            output += ') '
        return output


    def _set_level(self, level):
        self.level = level
        for child in self.children:
            child._set_level(level+1)
    

    def _set_id(self, id):
        self.id = id
        for i, child in enumerate(self.children):
            child._set_id(id + str(i))


    def _add_nodes_and_edges_to_graph(self, graph):
        for child in self.children:
            graph.node(child.id, child.symbol)
            graph.edge(self.id, child.id)
            child._add_nodes_and_edges_to_graph(graph)


    def _get_sympy_expr(self, evaluate):
        if not self.children:
            return sym.symbols(self.symbol)
        
        kids = self.children

        if self.symbol == '+':
            return sym.Add(kids[0]._get_sympy_expr(evaluate),
                           kids[1]._get_sympy_expr(evaluate),
                           evaluate=evaluate)

        if self.symbol == '-':
            return sym.Add(kids[0]._get_sympy_expr(evaluate),
                           sym.Mul(-1, kids[1]._get_sympy_expr(evaluate)),
                           evaluate=evaluate)

        if self.symbol == '*':
            return sym.Mul(kids[0]._get_sympy_expr(evaluate),
                           kids[1]._get_sympy_expr(evaluate),
                           evaluate=evaluate)

        if self.symbol == '/':
            return sym.Mul(kids[0]._get_sympy_expr(evaluate),
                           sym.Pow(kids[1]._get_sympy_expr(evaluate), -1),
                           evaluate=evaluate)

        if self.symbol == '^':
            return sym.Pow(kids[0]._get_sympy_expr(evaluate),
                           kids[1]._get_sympy_expr(evaluate),
                           evaluate=evaluate)
            


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


    def generate_graph(self, name='graph'):
        graph = graphviz.Digraph(name)
        graph.node(self.root.id, self.root.symbol)
        self.root._add_nodes_and_edges_to_graph(graph)
        return graph


    def get_sympy_expr(self, evaluate):
        return self.root._get_sympy_expr(evaluate)
