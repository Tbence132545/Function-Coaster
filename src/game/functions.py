import sympy 
import numpy as np


x = sympy.symbols('x')

def parse_function(user_input):
    try:
        if '[' in user_input and ']' in user_input:
            expr_str, interval_str = user_input.split('[')
            expr_str = expr_str.strip()
            interval_str = interval_str.strip('[] ')
            a, b = map(float, interval_str.split(','))
            interval = (a, b)
        else:
            expr_str = user_input.strip()
            interval = (-float('inf'), float('inf'))  # No interval specified

        expr = sympy.sympify(expr_str, locals={'x': x})
        f = sympy.lambdify(x, expr, modules=["numpy"])
        return f, interval
    
    except (sympy.SympifyError, TypeError, ValueError) as e:
        print(f"Error parsing function: {e}")
        return None, None