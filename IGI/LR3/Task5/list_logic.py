"""
Basic logic for Task 5: Real-valued list processing.
1) Find index of the element with maximum absolute value.
2) Calculate product of elements between first and second non-zero elements.
"""

def get_max_abs_index(data_list):
    """Returns the 1-based index of the element with max absolute value."""
    if not data_list:
        return None
    
    max_val = abs(data_list[0])
    max_idx = 0
    
    for i in range(1, len(data_list)):
        if abs(data_list[i]) > max_val:
            max_val = abs(data_list[i])
            max_idx = i
            
    return max_idx + 1  


def get_product_between_non_zeros(data_list):
    """
    Calculates product of elements between the first and second non-zero elements.
    If no elements exist between them, returns 0.
    """
    non_zero_indices = [i for i, x in enumerate(data_list) if x != 0]
    
    if len(non_zero_indices) < 2:
        return None
    
    first_idx = non_zero_indices[0]
    second_idx = non_zero_indices[1]
    
    if second_idx - first_idx <= 1:
        return 0
    
    product = 1.0
    for i in range(first_idx + 1, second_idx):
        product *= data_list[i]
        
    return product