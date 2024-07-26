import numpy as np
import pandas as pd

class DataLoader:
    def __init__(self, input, cols):
        self.input = input
        self.cols = cols

    def load_data(self):
        if isinstance(self.input, pd.DataFrame):
            return self.input
        elif isinstance(self.input, dict):
            return pd.DataFrame.from_dict(self.input, orient='columns')
        elif isinstance(self.input, list):
            return pd.DataFrame(self.input, columns=self.cols)
        elif isinstance(self.input, tuple):
            return pd.DataFrame([self.input], columns=self.cols)
        elif isinstance(self.input, np.ndarray):
            return pd.DataFrame(self.input, columns=self.cols)
        elif isinstance(self.input, str):
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