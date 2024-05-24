import io

import numpy as np
import pandas as pd

from fpdf import FPDF


class EDA:
    """
    Pandas DataFrame 자료형에 대한 EDA(탐색적 데이터 분석)를 수행하는 Module.
    Input Data로 EDA를 수행할 데이터를 입력.
    
    Attributes:
        input : EDA를 수행할 Dataset (Pandas DataFrame / List / Dictionary / Numpy Array).
        
    Methods:
        _convert_to_df(input) : pd.DataFrame / list / dict / np.ndarray를 pd.DataFrame으로 변환하는 함수.
        info() : Input Data에 대한 Information을 출력(Row, Col 수 / Head, Tail / ColName, Data Types / Missing Values 수)하는 함수.
        summary() : Input Data의 기술통계를 출력(Numerical Values / Categorical Values)하는 함수.
        save_markdown(filename) : info(), summary() Function의 결과를 Markdown Documents로 저장하는 함수.
        save_pdf(filename) : info(), summary() Function의 결과를 PDF Documents로 저장하는 함수.
    """
    
    def __init__(self, input):
        self.input = self._convert_to_df(input)
        self.num_cols = self.input.select_dtypes(include=[np.number]).columns
        self.cat_cols = self.input.select_dtypes(include=['object']).columns
    
    def _convert_to_df(self, input):
        if isinstance(input, pd.DataFrame):
            return input
        elif isinstance(input, dict):
            return pd.DataFrame.from_dict(input, orient='columns')
        elif isinstance(input, list):
            return pd.DataFrame(input)
        elif isinstance(input, np.ndarray):
            return pd.DataFrame(input)
        else:
            raise TypeError('Input Data Must Be a Pandas DataFrame, Dict, List or Numpy Array.')
        
    def info(self):
        buffer = io.StringIO()
        print('1.1. Data Information', file=buffer)
        print(f'Number of Rows : {self.input.shape[0]}', file=buffer)
        print(f'Number of Cols : {self.input.shape[1]}\n\n', file=buffer)
        
        print('1.2. Data Example', file=buffer)
        print('Head', file=buffer)
        print(self.input.head(), '\n', file=buffer)
        print('Tail', file=buffer)
        print(self.input.tail(), '\n\n', file=buffer)
        
        print('1.3. Column Names and Data Types', file=buffer)
        self.input.info(buf=buffer)
        
        print('\n\n1.4. Missing Values', file=buffer)
        print(self.input.isnull().sum(), '\n\n', file=buffer)
        
        info_str = buffer.getvalue()
        buffer.close()
        
        return info_str
        
    def summary(self):
        buffer = io.StringIO()
        if len(self.num_cols) > 0:
            print('2.1. Numerical Features Summary', file=buffer)
            print(round(self.input[self.num_cols].describe(), 2), '\n\n', file=buffer)
        else:
            print('2.1. Numerical Features Summary', file=buffer)
            print("Input Data's Numerical Columns aren't Exist.\n\n", file=buffer)
            pass
            
        if len(self.cat_cols) > 0:
            print('2.2. Categorical Features Summary', file=buffer)
            for col in self.cat_cols:
                sums = self.input[col].value_counts()
                print(f'{col} : {sums}\n', file=buffer)
            print('\n\n', file=buffer)
        else:
            print('2.2. Categorical Features Summary', file=buffer)
            print("Input Data's Categorical Columns aren't Exist.\n\n", file=buffer)
            pass
        
        summary_str = buffer.getvalue()
        buffer.close()
        
        return summary_str
        
    def save_markdown(self, filename):
        info_str = self.info()
        summary_str = self.summary()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("EDA Report\n\n")
            f.write("01. Data Information\n\n")
            f.write(info_str)
            f.write("\n\n02. Data Summary\n\n")
            f.write(summary_str)
            
    def save_pdf(self, filename):
        info_str = self.info()
        summary_str = self.summary()
        
        document = FPDF()
        document.add_page()
        document.set_font('Arial', 'B', size=16)
        document.cell(w=200, h=10, txt='EDA Report\n\n', ln=1, align='L')
        
        document.set_font('Arial', 'B', size=14)
        document.cell(w=200, h=10, txt='01. Data Information\n\n', ln=1, align='L')
        document.set_font('Arial', size=12)
        document.multi_cell(w=0, h=5, txt=info_str)
        
        document.add_page()
        document.set_font('Arial', 'B', size=14)
        document.cell(w=200, h=10, txt='02. Data Summary\n\n', ln=1, align='L')
        document.set_font('Arial', size=12)
        document.multi_cell(w=0, h=5, txt=summary_str)
        
        document.output(filename)