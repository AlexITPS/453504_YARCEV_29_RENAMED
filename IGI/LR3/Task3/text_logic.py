"""
Basic logic for Task 3: Counting digits in a string.
"""

def count_digits_in_string(text):
    """
    Analyzes the input string and counts occurrences of digits (0-9).
    
    :param text: The string to analyze.
    :return: Integer count of digits.
    """
    digit_count = 0
    for char in text:
        if char.isdigit():
            digit_count += 1
    return digit_count