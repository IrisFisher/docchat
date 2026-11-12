import json

with open("tools/tools.json", encoding='utf-8') as f:
    tools = json.load(f)

def calculate(expression):
    """Evaluate a mathematical expression"""
    for char in str(expression):
        if char not in '1234567890()+-/*= ':
            return json.dumps({"error": "Invalid expression"})
    result = eval(expression)  # Use safe evaluation in production
    return json.dumps({"result": result})

#available_functions = {
    #"calculate": calculate,
    # Add more tools here as you build them
    # "get_weather": get_weather,
    # "search_database": search_database,
#}

def execute_tool_call(tool_call):
    """Parse and execute a single tool call"""
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    
    # Call the function with unpacked arguments
    return function_to_call(**function_args)