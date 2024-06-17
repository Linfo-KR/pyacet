import numpy as np

def calculate_ndim(col_length=int):
    """
    col_length에 맞는 subplot의 차원을 계산하는 함수

    Parameters:
    -----------
    col_length : int
        subplot에 전달할 열의 길이
        
    Returns:
    --------
    n : int
        subplot의 차원
    """
    if not isinstance(col_length, int):
        raise ValueError(f"col_length or hue_length should be an int, got {type(col_length)} instead.")
    
    n = int(np.ceil(np.sqrt(col_length)))
    
    return n