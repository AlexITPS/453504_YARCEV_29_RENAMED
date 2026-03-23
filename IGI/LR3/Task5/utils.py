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
                repeat = input("\nRun Task 5 again? (y/n): ").strip().lower()
                if repeat == 'y':
                    break
                elif repeat == 'n':
                    print("Exiting Task 5. Goodbye!")
                    return
                else:
                    print("Please enter 'y' or 'n'")
    return wrapper

def input_real_list():
    """Reads a list of float numbers from user input with validation."""
    while True:
        try:
            user_input = input("Enter float numbers separated by spaces: ").strip()
            if not user_input:
                print("Error: List cannot be empty.")
                continue
            return [float(x) for x in user_input.split()]
        except ValueError:
            print("Error: Please enter only valid real numbers.")