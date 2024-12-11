import javalang

from .modifiers import get_mofifiers
from .annotations import get_annotations
from .parameters import get_parameters
from .throws import get_throws
from .imports import get_imports_used_in_method
from .code_body import extract_code_without_signature
from .get_line_by_line import get_body_code


def get_methods(node, lines, tree):
    method_lst = []
    
    for body_item in node:

        if isinstance(body_item, javalang.tree.MethodDeclaration):
            full_method_code = extract_code_without_signature(body_item, lines)
            data = {
                "name": body_item.name,
                "modifiers": get_mofifiers(body_item.modifiers),
                "return_type": body_item.return_type.name if body_item.return_type else 'void',
                "annotations": get_annotations(body_item.annotations),
                "parameters": get_parameters(body_item.parameters),
                "throws": get_throws(body_item.throws),
                "used_imports": get_imports_used_in_method(full_method_code, tree.imports),
                "method_body": get_body_code(full_method_code),
                "comment": body_item.documentation
            }
            method_lst.append(data)
    
    return method_lst