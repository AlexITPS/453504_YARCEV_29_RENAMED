"""
Helper functions for input, output, and decorator.
"""

import functools

def repeat_decorator(func):
    """Decorator to handle the program repetition logic."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)
            while True:
                repeat = input("\nRun Task 1 again? (y/n): ").strip().lower()
                if repeat == 'y':
                    break
                elif repeat == 'n':
                    print("Exiting Task 1. Goodbye!")
                    return
                else:
                    print("Please enter 'y' or 'n'")
    return wrapper


def safe_float_input(prompt):
    """Safe float input with error handling."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                raise ValueError("Input cannot be empty")
            return float(value)
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")


def safe_int_input(prompt):
    """Safe integer input with error handling."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                raise ValueError("Input cannot be empty")
            return int(value)
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")


def display_results(results):
    """Display results in a clean, formatted table."""
    header = f"{'x':^10} | {'n':^6} | {'F(x)':^20} | {'Math F(x)':^20} | {'eps':^10}"
    separator = "=" * len(header)
    
    print(f"\n{separator}")
    print(header)
    print(separator)
    
    for x, n, f_x, math_f_x, eps in results:
        n_str = str(n)
        if isinstance(f_x, float):
            print(f"{x:^10.4f} | {n_str:^6} | {f_x:^20.10f} | {math_f_x:^20.10f} | {eps:^10.1e}")
        else:
            print(f"{x:^10.4f} | {n_str:^6} | {'Error':^20} | {'Error':^20} | {eps:^10.1e}")
            
    print(separator)