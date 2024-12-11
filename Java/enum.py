import javalang

from .modifiers import get_mofifiers
from .annotations import get_annotations
from .methods import get_methods
from .constructors import get_constructors
from .variables import get_variables


def get_enum(node, tree, lines, repo_structure):
    if 'enums' not in repo_structure:
        repo_structure['enums'] = []

    if isinstance(node, javalang.tree.EnumDeclaration):
        class_details = {
            'name': node.name,
            'annotations': get_annotations(node.annotations),
            "modifiers": get_mofifiers(node.modifiers),
            "implements": [iface.name for iface in node.implements] if node.implements else [],
            "constants": get_enum_constants(node),  
            "variables": get_variables(node),
            "constructors": get_constructors(node.body.declarations, lines, tree),
            "methods": get_methods(node.body.declarations, lines, tree),
            "comment": node.documentation
        }

        repo_structure['enums'].append(class_details)


def get_enum_constants(node):
    constants = []
    for body_item in node.body:
        if isinstance(body_item, javalang.tree.EnumConstantDeclaration):
            constants.append({
                "name": body_item.name,
                "annotations": get_annotations(body_item.annotations)
            })
    return constants