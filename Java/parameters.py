from .modifiers import get_mofifiers
from .annotations import get_annotations


def get_parameters(parameters_body):
    parameters_lst = []
    for param in parameters_body:
        param_type = getattr(param.type, 'name', 'Unknown')
        
        data = {
            "name": param.name,
            "type": param_type,
            "modifiers": get_mofifiers(param.modifiers),
            "annotations": get_annotations(param.annotations)
        }
        parameters_lst.append(data)

    return parameters_lst