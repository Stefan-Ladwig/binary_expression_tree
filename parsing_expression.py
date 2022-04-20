import re
import sympy as sym
import tree


# input = 'dw+(dasd+(sd+(ds-9))+((2*3)-r))'
        #0123456789012345678901234567890

input = '7 - 3 * 4**(3 / 2)'
        #0123456789012345678901234567890

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


def rec(input, pos='s'):
    input = cleanup(input)
    print(pos, input)
    for operators in ('Add', 'Mul', 'Pow'):
        idx = check_operator(operator_dict[operators], input)
        if idx != None:
            symbol = input[idx]
            node = tree.Node(symbol)
            left_child = rec(input[:idx], pos+'l')
            right_child = rec(input[idx + 1:], pos+'r')
            node.set_children(left_child, right_child)
            return node

    return tree.Node(input.strip())

input = re.sub(r'\s', '', input)
input = re.sub(r'\*{2}', '^', input)
my_tree = tree.Tree(rec(input))
my_tree.print_prefix()
print(my_tree.root.symbol, my_tree.root.id)
graph = my_tree.generate_graph()
graph.render(filename='graph.dot', directory='generated_graphs', view=True) 
expr=my_tree.get_sympy_expr(False)
print(sym.srepr(expr))
sym.preview(expr, dvioptions=['-D 200'])