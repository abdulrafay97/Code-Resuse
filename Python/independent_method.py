import ast

from .parameters import get_python_method_parameters
from ._return import get_return_info
from .imports import get_used_imports

def get_independent_methods(parsed_ast, imports):
    methods = []

    annotate_parents(parsed_ast)

    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.FunctionDef):

            if not isinstance(node.parent, ast.ClassDef):
                data = {
                    "name": node.name,
                    "parameters": get_python_method_parameters(node), 
                    "defaults": [ast.dump(d) for d in node.args.defaults],
                    "decorators": [ast.dump(d) for d in node.decorator_list],
                    "return_value": get_return_info(node),
                    "docstring": ast.get_docstring(node),
                    "uses_imports": get_used_imports(node, imports)
                }
                methods.append(data)
    
    return methods


def annotate_parents(node, parent=None):
    node.parent = parent
    for child in ast.iter_child_nodes(node):
        annotate_parents(child, node)