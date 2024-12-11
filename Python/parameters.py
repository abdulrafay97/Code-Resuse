import ast

def get_python_method_parameters(node):
    parameters = []

    for arg in node.args.args:
        param_data = {"name": arg.arg}

        if arg.annotation:
            if isinstance(arg.annotation, ast.Name):
                param_data["type"] = arg.annotation.id  
            elif isinstance(arg.annotation, ast.Attribute):
                param_data["type"] = f"{arg.annotation.value.id}.{arg.annotation.attr}"
            else:
                param_data["type"] = ast.dump(arg.annotation)
        else:
            param_data["type"] = None

        parameters.append(param_data)

    return parameters