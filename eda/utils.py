

def calculate_ndim(col_length=int, max_n=20):
    """
    col_length에 맞는 subplot의 차원을 계산하는 함수

    Parameters:
    -----------
    col_length : int
        subplot에 전달할 열의 길이
    max_n : int
        최대 subplot 수 (default=20)
        
    Returns:
    --------
    int
        subplot의 차원 수
    """
    if not isinstance(col_length, int):
        raise ValueError(f"col_length or hue_length should be an int, got {type(col_length)} instead.")
    
    for i in range(1, (max_n+1)):
        if (i-1)**2 < col_length <= i**2:
            return i
    else:
        raise ValueError(f"col_length({col_length}) is larger than max_n({max_n}).")