"""
Main Module: LW 3, Task 2
Developer: YARCEV A.A.
Description: Count integers > 12 until 133 is entered.
Version: 1.0
Date: 2026-03-20
"""

import utils
import logic

@utils.repeat_decorator
def main():
    """Main execution flow for Task 2."""
    print("\n" + "="*50)
    print("Task 2: Count numbers > 12 (Stop at 133)")
    print("="*50)

    result = logic.process_sequence(utils.safe_int_input)
    
    print("\n" + "-"*30)
    print(f"Total numbers greater than 12: {result}")
    print("-"*30)

if __name__ == "__main__":
    main()