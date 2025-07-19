import sympy 
import numpy as np


x = sympy.symbols('x')

def parse_function(user_input):
    x = sympy.symbols('x')
    try:
        expr = sympy.sympify(user_input, locals={'x': x})
        f = sympy.lambdify(x, expr, modules=["numpy"])
        return f
    except (sympy.SympifyError, TypeError) as e:
        print(f"Error parsing function: {e}")
        return None