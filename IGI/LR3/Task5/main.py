"""
Main Module: LW 3, Task 5
Developer: YARCEV A.A.
Description: Real-valued list processing (Max abs index and product between non-zeros).
Version: 1.0
Date: 2026-03-21
"""

import utils
import list_logic

@utils.repeat_decorator
def main():
    """Main execution flow for Task 5."""
    print("\n" + "="*50)
    print("TASK 5: LIST PROCESSING")
    print("="*50)

    data = utils.input_real_list()
    print(f"\nYour list: {data}")

    max_idx = list_logic.get_max_abs_index(data)
    print(f"1) Position of max absolute element: {max_idx}")

    product = list_logic.get_product_between_non_zeros(data)
    
    if product is None:
        print("2) Product calculation: Error (at least two elements required).")
    else:
        print(f"2) Product of elements between first two non-zeros: {product:.4f}")

if __name__ == "__main__":
    main()