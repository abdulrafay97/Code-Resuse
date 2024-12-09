import re

def get_imports(tree, repo_structure):
    import_lst = []

    for imp in tree.imports:
        import_lst.append(imp.path)
    
    repo_structure['imports'] = import_lst


def get_imports_used_in_method(method_body, imports):
    used_imports = []
    for _import in imports:
        import_name = _import.path.split('.')[-1]
        
        pattern = r'\b' + re.escape(import_name) + r'\b'
        if any(re.search(pattern, line) for line in method_body.splitlines()):
            used_imports.append(_import.path)
            
    return used_imports
