import io
import datetime as dt

from pyacet.data_loader import DataLoader

class DataSummary:
    def __init__(self, input, cols):
        self.input = DataLoader(input, cols).load_data()
        self.num_cols = DataLoader(input, cols).get_numerical_cols()
        self.cat_cols = DataLoader(input, cols).get_categorical_cols()
        self.dt_cols = DataLoader(input, cols).get_datetime_cols()
        
    def data_info(self):
        buffer = io.StringIO()
        self.input.info(buf=buffer)
        
        data_info = buffer.getvalue()
        data_shape = self.input.shape
        data_head = self.input.head()
        data_null = self.input.isnull().sum()
        data_duplication = self.input.duplicated().sum()
        
        return data_info, data_shape, data_head, data_null, data_duplication
    
    def data_numerical_summary(self):
        if self.num_cols is not None and len(self.num_cols) > 0:
            num_cols_summary = round(self.input[self.num_cols].describe(), 2)
            return num_cols_summary
        else:
            pass
    
    def data_categorical_summary(self, exclude_cols=None):
        if self.cat_cols is not None and len(self.cat_cols) > 0:
            cat_cols_summary = self.input[self.cat_cols].describe(include='O')
            features_dict = {}
            if exclude_cols is not None:
                for col in [cols for cols in self.cat_cols if cols not in exclude_cols]:
                    features = self.input[col].unique()
                    features_dict[col] = {'features': features.tolist(),
                                          'num_features': len(features)}
            else:
                for col in self.cat_cols:
                    features = self.input[col].unique()
                    features_dict[col] = {'features': features.tolist(),
                                        'num_features': len(features)}
            return cat_cols_summary, features_dict
        else:
            pass
    
    def data_datetime_summary(self):
        if self.dt_cols is not None and len(self.dt_cols) > 0:
            dt_cols_summary = {
                'summary': self.input[self.dt_cols].agg(['min', 'max', 'nunique'])
            }
            for col in self.dt_cols:
                dt_cols_summary[col] = {
                    'year': self.input[col].dt.year.value_counts(),
                    'month': self.input[col].dt.month.value_counts(),
                    'day': self.input[col].dt.day.value_counts(),
                    'dayofweek': self.input[col].dt.dayofweek.value_counts()
                }
            return dt_cols_summary
        else:
            pass

    def data_correlation(self, methods='pearson'):
        if self.num_cols is not None and len(self.num_cols) > 0:
            corr_matrix = round(self.input[self.num_cols].corr(method=methods), 2)
            return corr_matrix
        else:
            pass