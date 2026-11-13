import json

def calculate(expression):
    """Evaluate a mathematical expression"""
    for char in str(expression):
        if char not in '1234567890()+-/*= ':
            return json.dumps({"error": "Invalid expression"})
    result = eval(expression)  # Use safe evaluation in production
    return json.dumps({"result": result})