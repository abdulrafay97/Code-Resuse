import ast

def get_return_info(node):
    return_info = []

    if isinstance(node, ast.FunctionDef):
        return_type = node.returns.id if isinstance(node.returns, ast.Name) else None
        
        for subnode in node.body:
            if isinstance(subnode, ast.Return):  
                if isinstance(subnode.value, ast.Name): 
                    return_info.append({
                        "variable_name": subnode.value.id,
                        "return_type": return_type
                    })
                elif isinstance(subnode.value, ast.BinOp):
                    return_info.append({
                        "variable_name": "expression",
                        "return_type": return_type
                    })

    return return_info