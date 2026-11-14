import json

def calculate(expression):
    #python -m doctest -v tools/calculate.py
    """Evaluate a mathematical expression
    >>> calculate('6*7')
    42
    >>> calculate('a*b')
    'Error: Invalid expression'
    """
    for char in str(expression):
        if char not in '1234567890()+-/*= ':
            return ('Error: Invalid expression')
    result = eval(expression)
    return result