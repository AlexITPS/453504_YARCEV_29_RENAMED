"""
Main Module: LW 3, Task 1
Developer: YARCEV A.A.
Description: Power series expansion for ln(1-x)
Date: 2026-03-20
"""

import math
import utils
import math_logic
import sequence_init

def get_method_choice():
    """UI for choosing the initialization method."""
    print("\nHow to initialize x values?")
    print("1. Generate a range (start, end, count)")
    print("2. Enter specific values manually")
    while True:
        choice = input("Enter choice (1/2): ").strip()
        if choice in ('1', '2'):
            return choice
        print("Invalid choice. Enter 1 or 2.")

@utils.repeat_decorator
def main():
    """Main execution flow for Task 1."""
    print("\n" + "="*40)
    print("Task 1: ln(1-x) Caclulation")
    print("="*40)

    eps = utils.safe_float_input("Enter precision (e.g., 1e-5): ")
    if eps <= 0:
        print("Precision must be positive. Setting to 1e-6.")
        eps = 1e-6

    method = get_method_choice()
    x_values = []

    if method == '1':
        while True:
            start = utils.safe_float_input("Start x (-1 < x < 1): ")
            end = utils.safe_float_input("End x (-1 < x < 1): ")
            if -1 < start < 1 and -1 < end < 1:
                break
            print("Error: Both Start and End must be between -1 and 1.")
            
        count = utils.safe_int_input("Number of points: ")
        x_values = sequence_init.init_from_generator(start, end, count)
    else:
        x_values = sequence_init.init_from_user_input()

    results = []
    for x in x_values:
        try:
            res_val, iters = math_logic.calculate_ln_series(x, eps)
            math_val = math.log(1 - x)
            results.append((x, iters, res_val, math_val, eps))
        except (ValueError, ZeroDivisionError) as e:
            print(f"\nCalculation error for x = {x}: {e}")
            results.append((x, "Err", None, None, eps))

    if results:
        utils.display_results(results)
    else:
        print("No results to display.")

if __name__ == "__main__":
    main()