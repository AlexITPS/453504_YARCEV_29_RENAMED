"""
Main Module: LW 3, Task 3
Developer: YARCEV A.A.
Description: Count the number of digits in a user-provided string.
Version: 1.0
Date: 2026-03-20
"""

import utils
import text_logic

@utils.repeat_decorator
def main():
    """Main execution flow for Task 3."""
    print("\n" + "="*50)
    print("TASK 3: DIGIT COUNTER IN STRING")
    print("="*50)

    user_string = input("Please enter a string to analyze: ").strip()
    
    if not user_string:
        print("The string is empty. No digits found.")
        return

    total_digits = text_logic.count_digits_in_string(user_string)
    
    print("\n" + "-"*30)
    print(f"Original text: '{user_string}'")
    print(f"Number of digits found: {total_digits}")
    print("-"*30)

if __name__ == "__main__":
    main()