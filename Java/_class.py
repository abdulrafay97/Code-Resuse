import javalang

from .modifiers import get_mofifiers
from .annotations import get_annotations
from .methods import get_methods
from .constructors import get_constructors
from .variables import get_variables



def get_class(node, tree, lines, repo_structure):

    if 'classes' not in repo_structure:
        repo_structure['classes'] = []

    class_details = {
        'name': node.name,
        'annotations': get_annotations(node.annotations),
        "modifiers": get_mofifiers(node.modifiers),
        "extends": node.extends.name if node.extends else None,
        "implements": [iface.name for iface in node.implements] if node.implements else [],
        "nested_classes": get_nested_classes(node),
        "variables": get_variables(node),
        "constructors": get_constructors(node.body, lines, tree),
        "methods": get_methods(node.body, lines, tree),
        "comment": node.documentation
    }

    repo_structure['classes'].append(class_details)


def get_nested_classes(node):
    nested_lst = []

    for inner_node in node.body:
        if isinstance(inner_node, javalang.tree.ClassDeclaration):
            nested_lst.append(inner_node.name)