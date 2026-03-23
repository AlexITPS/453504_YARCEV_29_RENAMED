"""
Function calculate ln(1-x) using power series.
Formula: ln(1-x) = -x - (x^2)/2 - (x^3)/3 - ...
"""

def calculate_ln_series(x, eps, max_iter=500):
    """
    Computes the sum of the power series for ln(1-x).
    
    :param x: Argument value (|x| < 1)
    :param eps: Target precision
    :param max_iter: Maximum iterations (default = 500)
    :return: (sum_value, iterations_count)
    """
    if not (-1 < x < 1):
        raise ValueError(f"Convergence range is (-1 < x < 1). Got x = {x}")
    
    sum_value = 0.0
    n = 1
    
    while n <= max_iter:
        term = -(x**n / n)
        sum_value += term
        
        if abs(term) < eps:
            return sum_value, n
        n += 1
        
    return sum_value, max_iter