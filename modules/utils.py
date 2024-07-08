import os
import time

import numpy as np
import pandas as pd

from functools import wraps

def ensure_trailing_slash(path):
    return path if path.endswith('/') else path + '/'

def create_output_directory(output):
    if not os.path.exists(output):
        os.makedirs(output, exist_ok=True)
        
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        stime = time.perf_counter()
        result = func(*args, **kwargs)
        etime = time.perf_counter()
        runtime = round((etime - stime), 0)
        print(f"{func.__qualname__}'s runtime: {runtime} sec", flush=True)
        return result
    return wrapper

def generate_testset():
    np.random.seed(42)
    date_range = pd.date_range(start='2021-01-01', end='2023-12-31', freq='D')
    df = pd.DataFrame(date_range, columns=['date'])
    
    df['value'] = np.random.randn(len(date_range)) * 10 + np.linspace(10, 20, len(date_range))
    outliers = np.random.choice(len(date_range), size=5, replace=False)
    df.loc[outliers, 'value'] *= 3
    df['value'] = round(df['value'], 1)
    
    df['temperature'] = np.random.normal(loc=15, scale=10, size=len(date_range))
    df['temperature'] += np.linspace(-5, 5, len(date_range))
    df.loc[outliers, 'temperature'] *= -1
    df['temperature'] = round(df['temperature'], 1)
    
    df['humidity'] = np.random.uniform(low=20, high=100, size=len(date_range))
    df['humidity'] += np.sin(np.linspace(0, 2 * np.pi, len(date_range))) * 10
    df['humidity'] = round(df['humidity'], 1)
    
    df['uv'] = np.random.uniform(low=0, high=80, size=len(date_range))
    df['uv'] = round(df['uv'], 1)
    
    df['atmosphere'] = np.random.randint(low=0, high=200, size=len(date_range))
    
    df['rainfall'] = np.random.binomial(n=1, p=0.3, size=len(date_range))
    
    df['holiday'] = np.random.binomial(n=1, p=0.1, size=len(date_range))
    
    df['day_of_week'] = df['date'].dt.day_name()
    
    texts = ['A', 'B', 'C', 'D', 'E']
    df['text_data'] = np.random.choice(texts, size=len(date_range))
    
    weathers = ['Hot', 'Cold', 'Sunny', 'Rain', 'Cloud']
    df['weather'] = np.random.choice(weathers, size=len(date_range))
    
    regions = ['NAEC', 'NAWC', 'SAEC', 'SAWC', 'ASIA', 'WAF', 'ESAF', 'NEUR', 'MID', 'AUZ']
    df['region'] = np.random.choice(regions, size=len(date_range))
    
    num_duplicates = int(len(df) * 0.05)
    duplicate_index = np.random.choice(len(df), size=num_duplicates, replace=True)
    duplicate_data = df.sample(n=1).iloc[0].to_dict()
    for idx in duplicate_index:
        df.iloc[idx] = duplicate_data
    
    return df