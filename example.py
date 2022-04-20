import sympy as sym
import expression_tree


# input = 'dw+(dasd+(sd+(ds-9))+((2*3)-r))'
        #0123456789012345678901234567890

input = '7 - 3 * 4**(3 / 2)'
        #0123456789012345678901234567890


my_tree = expression_tree.parse_expression(input)
my_tree.print_prefix()
print(my_tree.root.symbol, my_tree.root.id)
graph = my_tree.generate_graph()
graph.render(filename='graph.dot', directory='generated_graphs', view=True, format='png') 
expr=my_tree.get_sympy_expr(False)
print(sym.srepr(expr))
sym.preview(expr, dvioptions=['-D 200'])