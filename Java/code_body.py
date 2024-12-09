def extract_code_without_signature(entity, lines):
    if entity.position:
        start_line = entity.position[0] - 1 
        
        open_brackets = 0
        end_line = start_line
        for i in range(start_line, len(lines)):
            open_brackets += lines[i].count('{')
            open_brackets -= lines[i].count('}')
            if open_brackets == 0:
                end_line = i
                break

        return "\n".join(lines[start_line + 1:end_line])
    return "<Code could not be extracted>"