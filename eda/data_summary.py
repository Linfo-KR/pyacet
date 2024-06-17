from data_loader import DataLoader

class DataSummary:
    """
    데이터에 대한 요약 정보 및 기술통계 정보와 같은 데이터의 Summary를 출력하는 Class.

    Attributes:
    -----------
        input (pandas.DataFrame, list, dict, numpy.ndarray, json):
            EDA를 수행할 Dataset.
        num_cols (list):
            입력 데이터의 수치형 열 이름 목록.
        cat_cols (list):
            입력 데이터의 범주형 열 이름 목록.
        dt_cols (list):
            입력 데이터의 날짜/시간 열 이름 목록.
    """
    def __init__(self, input):
        self.input = DataLoader(input).load_data()
        self.num_cols = DataLoader(input).get_numerical_cols()
        self.cat_cols = DataLoader(input).get_categorical_cols()
        self.dt_cols = DataLoader(input).get_datetime_cols()
        
    def data_info(self):
        """
        입력 데이터의 각 feature 별 데이터 개수, NULL 여부, 데이터 타입 등의 정보를 출력하는 함수.

        Returns:
        --------
            tuple:
            
                - pandas.DataFrame.info: 데이터프레임 정보 요약.
                
                - tuple: 데이터프레임의 행과 열 개수.
                
                - pandas.DataFrame: 데이터프레임의 처음 5개 행.
                
                - pandas.Series: 각 열의 결측치 개수.
                
                - int: 중복 행의 개수.
        """
        data_shape = self.input.shape
        data_head = self.input.head()
        data_null = self.input.isnull().sum()
        data_duplication = self.input.duplicated().sum()
        
        return self.input.info(), data_shape, data_head, data_null, data_duplication
    
    def data_numerical_summary(self):
        """
        입력 데이터의 수치형 열에 대한 기술통계량을 출력하는 함수.

        Returns:
        --------
            pandas.DataFrame: 수치형 열에 대한 기술통계량 요약.
        """
        if len(self.num_cols) > 0:
            num_cols_summary = round(self.input[self.num_cols].describe(), 2)
        else:
            print('There are no numerical columns in the dataset.')
            pass
        
        return num_cols_summary
    
    def data_categorical_summary(self):
        """
        입력 데이터의 범주형 열에 대한 기술통계량을 출력하는 함수.

        Returns:
        --------
            pandas.DataFrame: 범주형 열에 대한 기술통계량 요약.
            dict: 범주형 열의 feature 고유값 및 개수 요약.
        """
        if len(self.cat_cols) > 0:
            cat_cols_summary = self.input[self.cat_cols].describe(include='O')
            features_dict = {}
            for col in self.cat_cols:
                features = self.input[self.cat_cols].unique()
                features_dict[col] = {'features': features.tolist(),
                                      'num_features': len(features)}
        else:
            print('There are no categorical columns in the dataset.')
            pass
        
        return cat_cols_summary, features_dict
    
    def data_datetime_summary(self):
        """
        입력 데이터의 datetime 열에 대한 기술통계량을 출력하는 함수.

        Returns: 
        --------
            dict: datetime 열에 대한 기술통계량 요약(Min / Max / Nunique / Year / Month / Day / DayOfWeek).
        """
        if len(self.dt_cols) > 0:
            dt_cols_summary = {
                'summary': self.input[self.dt_cols].agg(['min', 'max', 'nunique']),
                'year': self.input[self.dt_cols].dt.year.value_counts(),
                'month': self.input[self.dt_cols].dt.month.value_counts(),
                'day': self.input[self.dt_cols].dt.day.value_counts(),
                'dayofweek': self.input[self.dt_cols].dt.dayofweek.value_counts()
            }
        else:
            print('There are no datetime columns in the dataset.')
            pass
        
        return dt_cols_summary

    def data_correlation(self, methods='pearson'):
        """
        입력 데이터의 수치형 열 간의 상관관계를 출력하는 함수(Numerical columns only).
        
        Arguments:
        ----------
        methods (str): 상관계수 계산 방법.
            'pearson' - 피어슨 상관계수 (Pearson's correlation coefficient)
            
            'kendall' - 켄달 상관계수 (Kendall's tau)
            
            'spearman' - 스피어만 상관계수 (Spearman's rank correlation)

        Returns:
        --------
            pandas.DataFrame: Correlation Matrix 요약.
        """
        corr_matrix = round(self.input[self.num_cols].corr(method=methods), 2)
        
        return corr_matrix