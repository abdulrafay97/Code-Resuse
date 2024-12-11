import ast
from .parameters import get_python_method_parameters
from ._return import get_return_info
from .imports import get_used_imports



def get_class_methods(parsed_ast, imports):
    methods = []

    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.FunctionDef):
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



def get_python_classs(parsed_ast, imports):    
    classes = []

    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.ClassDef):
            for func in node.body:
                if isinstance(func, ast.FunctionDef):
                    methods = get_class_methods(parsed_ast, imports)

            data = {
                "name": node.name,
                "base_classes": [base.id if hasattr(base, "id") else base.attr for base in node.bases],
                "methods": methods,
                "docstring": ast.get_docstring(node)
            }

            classes.append(data)

    return classes