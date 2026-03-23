"""
Basic logic for Task 2: Counting numbers greater than 12.
"""

def process_sequence(input_func):
    """
    Reads integers and counts how many are > 12.
    Ends when 133 is entered.
    
    :param input_func: A function to get the next integer.
    :return: Total count of numbers > 12.
    """
    count = 0
    TARGET_STOP = 133
    THRESHOLD = 12

    while True:
        value = input_func("Enter integer (133 to stop): ")
        
        if value == TARGET_STOP:
            break
            
        if value > THRESHOLD:
            count += 1
            
    return count