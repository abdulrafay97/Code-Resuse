from .modifiers import get_mofifiers
from .annotations import get_annotations
from .methods import get_methods
from .constructors import get_constructors
from .variables import get_variables

import javalang


def get_interface(node, tree, lines, repo_structure):
    if 'interfaces' not in repo_structure:
        repo_structure['interfaces'] = []

    if isinstance(node, javalang.tree.InterfaceDeclaration):
        interface_details = {
            'name': node.name,
            'annotations': get_annotations(node.annotations),
            "modifiers": get_mofifiers(node.modifiers),
            "extends": (
                [ext.name for ext in node.extends] if isinstance(node.extends, list) else
                node.extends.name if node.extends else None
            ),
            "variables": get_variables(node),
            "constructors": get_constructors(node.body, lines, tree),
            "methods": get_methods(node.body, lines, tree),
            "comment": node.documentation
        }

        repo_structure['interfaces'].append(interface_details)
    else:
        print(f"Unexpected node type: {node}")
