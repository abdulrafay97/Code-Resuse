import javalang


def get_annotations(annotations_body):

    annotations_data = []
    
    if annotations_body:
        for annotation in annotations_body:
            annotation_data = {"name": annotation.name, "type": "Annotation"}
            
            if annotation.element:
                if isinstance(annotation.element, javalang.tree.Literal):
                    annotation_data["type"] = "Literal"
                    annotation_data["value"] = annotation.element.value
                
                elif isinstance(annotation.element, javalang.tree.MemberReference):
                    annotation_data["type"] = "MemberReference"
                    annotation_data["qualifier"] = annotation.element.qualifier
                    annotation_data["member"] = annotation.element.member
                
            
            annotations_data.append(annotation_data)
    
    return annotations_data
