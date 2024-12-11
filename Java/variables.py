import javalang

from .modifiers import get_mofifiers
from .annotations import get_annotations


def get_variables(node):
    variable_lst = []
    
    for body_item in node.body:
        if isinstance(body_item, javalang.tree.FieldDeclaration):
            for declarator in body_item.declarators:
                field_type = extract_field_type(body_item.type)


                data = {
                    "name": declarator.name,
                    "type": field_type,
                    "modifiers": get_mofifiers(body_item.modifiers),
                    "annotations": get_annotations(body_item.annotations),
                    "comment": body_item.documentation
                }

                variable_lst.append(data)
    
    return variable_lst


def extract_field_type(field_type_node):

    if not field_type_node:
        return "Unknown"


    if hasattr(field_type_node, 'arguments') and field_type_node.arguments:
        generic_args = []
        for arg in field_type_node.arguments:
            if isinstance(arg, javalang.tree.TypeArgument) and arg.type:
                generic_args.append(extract_field_type(arg.type)) 
            else:
                generic_args.append("Unknown") 

        return f"{field_type_node.name}<{', '.join(generic_args)}>"

    return field_type_node.name

