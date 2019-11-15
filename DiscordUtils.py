def case(str_input, first_cap): 
    if isinstance(str_input, str) and isinstance(first_cap, bool):
        caseChange = ("Admin", "Dev", "Command")
        str_input = str_input.lower()
        for item in caseChange: 
            if item.lower() in str_input: 
                str_input = str_input.replace(item.lower(), item)
        
        if not first_cap: 
            str_input = str_input[:1].lower() + str_input[1:]
        
        return(str_input)
    else: 
        print("Please input a string and a boolean.")

def snake_case(str_input, cap, first_cap): 
    if isinstance(str_input, str) and isinstance(cap, bool): 
        div = ("admin", "dev")
        str_input = str_input.lower() 
        for item in div: 
            if item in str_input:
                str_input = str_input.replace(item, item + "_")
        if cap and first_cap: 
            str_input = case(str_input, True)
        elif cap and not first_cap: 
            str_input = case(str_input, False)
        return str_input
    else: 
        print("Please input a string and two booleans")
