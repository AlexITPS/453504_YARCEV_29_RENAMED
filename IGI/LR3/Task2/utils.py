"""
Helper functions for input and decorator.
"""

import functools

def repeat_decorator(func):
    """Decorator to handle the program repetition logic."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)
            while True:
                repeat = input("\nRun Task 2 again? (y/n): ").strip().lower()
                if repeat == 'y':
                    break
                elif repeat == 'n':
                    print("Exiting Task 2. Goodbye!")
                    return
                else:
                    print("Please enter 'y' or 'n'")
    return wrapper

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