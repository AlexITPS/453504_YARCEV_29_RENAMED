"""
Functions for initializing the sequence of x values.
"""

def init_from_generator(start, end, num_points):
    """Generate a linear range of x values."""
    if num_points <= 1:
        return [start]
    step = (end - start) / (num_points - 1)
    return [round(start + i * step, 4) for i in range(num_points)]


def init_from_user_input():
    """Get x values from user input and validate range immediately."""
    while True:
        try:
            user_input = input("Enter x values (|x| < 1) separated by spaces: ").strip()
            if not user_input:
                print("Error: Input is empty.")
                continue
            
            raw_values = [float(val) for val in user_input.split()]
            
            valid_values = []
            for v in raw_values:
                if -1 < v < 1:
                    valid_values.append(v)
                else:
                    print(f"Warning: Value {v} ignored (out of range -1 < x < 1)")
            
            if not valid_values:
                print("No valid values entered. Try again.")
                continue
                
            return valid_values
        except ValueError:
            print("Error: Please enter only numbers.")