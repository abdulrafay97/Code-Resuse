from .modifiers import get_mofifiers
from .annotations import get_annotations
from .methods import get_methods
from .constructors import get_constructors
from .variables import get_variables



def get_interface(node, tree, lines, repo_structure):
    if 'interfaces' not in repo_structure:
        repo_structure['interfaces'] = []
    
    class_details = {
        'name': node.name,
        'annotations': get_annotations(node.annotations),
        "modifiers": get_mofifiers(node.modifiers),
        "extends": node.extends.name if node.extends else None,
        "variables": get_variables(node),
        "constructors": get_constructors(node, lines, tree),
        "methods": get_methods(node, lines, tree)
    }

    repo_structure['interfaces'].append(class_details)