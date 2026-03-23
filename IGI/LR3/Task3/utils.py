"""
Helper functions for decorator.
"""

import functools

def repeat_decorator(func):
    """Decorator to handle the program repetition logic."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)
            while True:
                repeat = input("\nRun Task 3 again? (y/n): ").strip().lower()
                if repeat == 'y':
                    break
                elif repeat == 'n':
                    print("Exiting Task 3. Goodbye!")
                    return
                else:
                    print("Please enter 'y' or 'n'")
    return wrapper