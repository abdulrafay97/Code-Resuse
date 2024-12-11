import ast

def get_python_imports(parsed_ast):
    imports = []

    for node in ast.walk(parsed_ast):        
        if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "module": alias.name,
                        "alias": alias.asname
                    })
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append({
                    "module": node.module,
                    "name": alias.name,
                    "alias": alias.asname
                })

    return imports



def get_used_imports(node, imports):
    used_imports = []

    for subnode in ast.walk(node):

        if isinstance(subnode, ast.Import):
            for alias in subnode.names:
                
                if any(imp['module'] == alias.name for imp in imports if 'module' in imp):
                    used_imports.append({"name": alias.name})

        elif isinstance(subnode, ast.ImportFrom):
            if any(imp['module'] == subnode.module for imp in imports if 'module' in imp):
                for alias in subnode.names:
                    
                    used_imports.append({
                        "module": subnode.module,
                        "attribute": alias.name
                    })

        elif isinstance(subnode, ast.Name):
            for imp in imports:
                if 'module' in imp and imp['module'] == subnode.id:
                    used_imports.append({"name": subnode.id})
                
                elif 'name' in imp and imp['name'] == subnode.id:
                    used_imports.append({
                        "module": imp['module'],
                        "attribute": imp['name']
                    })

        elif isinstance(subnode, ast.Attribute):
            if hasattr(subnode.value, 'id'):
                for imp in imports:
                    if 'module' in imp and imp['module'] == subnode.value.id:
                        used_imports.append({
                            "module": subnode.value.id,
                            "attribute": subnode.attr
                        })

    return used_imports