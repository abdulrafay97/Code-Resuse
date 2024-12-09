import javalang

from .modifiers import get_mofifiers
from .annotations import get_annotations
from .parameters import get_parameters
from .throws import get_throws
from .code_body import extract_code_without_signature
from .imports import get_imports_used_in_method
from .get_line_by_line import get_body_code


def get_constructors(node, lines, tree):

    constructor_lst = []
    
    for body_item in node.body:
        full_constructor_code = extract_code_without_signature(body_item, lines)

        if isinstance(body_item, javalang.tree.ConstructorDeclaration):
            
            data = {
                "name": body_item.name,
                "modifiers": get_mofifiers(body_item.modifiers),
                "annotations": get_annotations(body_item.annotations), 
                "parameters": get_parameters(body_item.parameters), 
                "used_imports": get_imports_used_in_method(full_constructor_code, tree.imports), 
                "throws": get_throws(body_item.throws),
                "constructor_body": get_body_code(full_constructor_code)
            }
            constructor_lst.append(data)
    
    return constructor_lst
