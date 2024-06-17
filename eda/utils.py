import numpy as np
import pandas as pd

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

def generate_testset():
    np.random.seed(42)
    date_range = pd.date_range(start='2021-01-01', end='2023-12-31', freq='D')
    df = pd.DataFrame(date_range, columns=['date'])
    
    df['value'] = np.random.randn(len(date_range)) * 10 + np.linspace(10, 20, len(date_range))
    outliers = np.random.choice(len(date_range), size=5, replace=False)
    df.loc[outliers, 'value'] *= 3
    
    df['temperature'] = np.random.normal(loc=15, scale=10, size=len(date_range))
    df['temperature'] += np.linspace(-5, 5, len(date_range))
    df.loc[outliers, 'temperature'] *= -1
    
    df['humidity'] = np.random.uniform(low=20, high=100, size=len(date_range))
    df['humidity'] += np.sin(np.linspace(0, 2 * np.pi, len(date_range))) * 10
    
    df['rainfall'] = np.random.binomial(n=1, p=0.3, size=len(date_range))
    
    df['holiday'] = np.random.binomial(n=1, p=0.1, size=len(date_range))
    
    df['day_of_week'] = df['date'].dt.day_name()
    
    texts = ['A', 'B', 'C', 'D', 'E']
    df['text_data'] = np.random.choice(texts, size=len(date_range))
    
    weathers = ['Hot', 'Cold', 'Sunny', 'Rain', 'Cloud']
    df['weather'] = np.random.choice(weathers, size=len(date_range))
    
    return df