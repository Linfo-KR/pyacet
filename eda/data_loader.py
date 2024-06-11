import json
import numpy as np
import pandas as pd

class DataLoader:
    """
    # DataLoader Class
    
    데이터를 로드하는 클래스로 다양한 Format(Pandas DataFrame / List / Dictionary / Numpy Array / Json)의 데이터를 Pandas DataFrame으로 변환.
    
    Attributes:
    -----------
        input :
            EDA를 수행할 Dataset (Pandas DataFrame / List / Dictionary / Numpy Array / Json).
        
    Methods:
    --------
        load_data() :
            Pandas DataFrame / List / Dictionary / Numpy Array / Json을 pd.DataFrame으로 변환하는 함수.
        get_numerical_cols() :
            input data의 numerical columns를 출력하는 함수.
        get_categorical_cols() :
            input data의 categorical columns를 출력하는 함수.
        get_datetime_cols() :
            input data의 datetime columns를 출력하는 함수.
    """
    def __init__(self, input):
        self.input = input

    def load_data(self):
        if isinstance(self.input, pd.DataFrame):
            return self.input
        elif isinstance(self.input, dict):
            return pd.DataFrame.from_dict(self.input, orient='columns')
        elif isinstance(self.input, list):
            return pd.DataFrame(self.input)
        elif isinstance(self.input, np.ndarray):
            return pd.DataFrame(self.input)
        elif isinstance(self.input, json):
            return pd.read_json(self.input)
        else:
            raise TypeError('Input Data Must Be a Pandas DataFrame, Dict, List or Numpy Array.')
        
    def get_numerical_cols(self):
        num_cols = self.input.select_dtypes(include=[np.number]).columns
        if not num_cols.empty:
            return num_cols
        else:
            print('There are no numerical columns in the dataset.')
            return None
    
    def get_categorical_cols(self):
        cat_cols = self.input.select_dtypes(include=['object']).columns
        if not cat_cols.empty:
            return cat_cols
        else:
            print('There are no categorical columns in the dataset.')
            return None
    
    def get_datetime_cols(self):
        dt_cols = self.input.select_dtypes(include=['datetime']).columns
        if not dt_cols.empty:
            return dt_cols
        else:
            print('There are no datetime columns in the dataset.')
            return None