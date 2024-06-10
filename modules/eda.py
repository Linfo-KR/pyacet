import io
import os
import matplotlib
import warnings

import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from fpdf import FPDF

warnings.filterwarnings('ignore')
matplotlib.use('Agg')

class EDA:
    """
    EDA class
    
    Pandas DataFrame 자료형에 대한 EDA(탐색적 데이터 분석)를 수행하는 Module.
    Input Data로 EDA를 수행할 데이터를 입력.
    
    Attributes:
    -----------
        input :
            EDA를 수행할 Dataset (Pandas DataFrame / List / Dictionary / Numpy Array).
        
    Methods:
    --------
        _convert_to_df(input) :
            pd.DataFrame / list / dict / np.ndarray를 pd.DataFrame으로 변환하는 함수.
        _set_plot_style() :
            Plot의 Default Style을 설정하는 함수.
        _clear_plot() :
            matplotlib.pyplot을 clean(cla, clf, close)하는 함수.
        _save_plot(plot, filepath, gnames, *cols) :
            Plot의 Title를 지정하고, 결과물을 저장하는 함수.
        info() :
            Input Data에 대한 Information을 출력(Row, Col 수 / Head, Tail / ColName, Data Types / Missing Values 수 / Dupicated Values 수)하는 함수.
        summary() :
            Input Data의 기술통계를 출력(Numerical Values / Categorical Values / Datetime Values)하는 함수.
        correlation() :
            Input Data의 Numerical Features를 대상으로 변수 간 상관관계(Pearson Correlation)를 출력하는 함수.
        save_markdown(filename) :
            info(), summary() Function의 결과를 Markdown Documents로 저장하는 함수.
        save_pdf(filename) :
            info(), summary() Function의 결과를 PDF Documents로 저장하는 함수.
        visualize(filepath) :
            Input Data의 모든 변수에 대해 Visualization하는 함수.
        
    Update:
    -------
        save_pdf() :
            PDF Documents Layout Update 예정
        visualize() :
            Plot Design 개선 및 출력 Plot 조정 예정

        
        Processing...
    """
    
    def __init__(self, input):
        self.input = self._convert_to_df(input)
        self.num_cols = self.input.select_dtypes(include=[np.number]).columns
        self.cat_cols = self.input.select_dtypes(include=['object']).columns
        self.dt_cols = self.input.select_dtypes(include=['datetime']).columns
    
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
        
    def _set_plot_style(self):
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['axes.grid'] = True
        plt.rcParams['axes.titleweight'] = 'bold'
        plt.rcParams['axes.labelweight'] = 'bold'
        
    def _clear_plot(self):
        plt.cla()
        plt.clf()
        plt.close()
        
    def _save_plot(self, filepath, gnames, *cols):
        title = f'{gnames} of {", ".join(cols)}' if cols else f'{gnames}'
        plt.title(title)
        plt.tight_layout()
        plt.savefig(filepath + gnames + f'_' + '_'.join(cols) + '.png')
        print(f'Create Plot : {title}')
        self._clear_plot()
        
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
        print(self.input.isnull().sum(), file=buffer)
        
        print('\n\n1.5. Duplicated Values', file=buffer)
        print(self.input.duplicated().sum(), file=buffer)
                
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
            print('\n', file=buffer)
        else:
            print('2.2. Categorical Features Summary', file=buffer)
            print("Input Data's Categorical Columns aren't Exist.\n\n", file=buffer)
            pass
        
        if len(self.dt_cols) > 0:
            print('2.3. Datetime Features Summary', file=buffer)
            print(self.input[self.dt_cols].agg(['min', 'max', 'nunique']), file=buffer)
            print(self.input[self.dt_cols].dt.year.value_counts(), file=buffer)
            print(self.input[self.dt_cols].dt.month.value_counts(), file=buffer)
            print(self.input[self.dt_cols].dt.day.value_counts(), file=buffer)
            print(self.input[self.dt_cols].dt.dayofweek.value_counts(), file=buffer)
        else:
            print('2.3. Datetime Features Summary', file=buffer)
            print("Input Data's Datetime Columns aren't Exist.\n\n", file=buffer)
            pass
                
        summary_str = buffer.getvalue()
        buffer.close()
        
        return summary_str
    
    def correlation(self):
        buffer = io.StringIO()
        # if self.input[self.num_cols].isnull().any().any():
        #     print("Input Data's Numerical Columns have Missing Values (NULL or NaN).\n\n", file=buffer)
        #     pass
    
        correlation_matrix = round(self.input[self.num_cols].corr(method='pearson'), 2)
        correlation_matrix.to_string(buf=buffer)
        correlation_str = buffer.getvalue()
        buffer.close()
    
        return correlation_str
    
    # Preparing Methods Update
    # Layout UI Update
    def save_markdown(self, filename):
        info_str = self.info()
        summary_str = self.summary()
        correlation_str = self.correlation()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("EDA Report\n\n")
            f.write("01. Data Information\n\n")
            f.write(info_str)
            f.write("\n\n02. Data Summary\n\n")
            f.write(summary_str)
            f.write("\n\n03. Data Correlation Analysis\n\n")
            f.write(correlation_str)
            
    # Preparing Methods Update
    # Layout UI Update
    def save_pdf(self, filename):
        info_str = self.info()
        summary_str = self.summary()
        correlation_str = self.correlation()
        
        document = FPDF(orientation='L')
        document.add_page()
        document.add_font('MalgunGothic', '', 'C:/Windows/Fonts/malgun.ttf', uni=True)
        document.set_font('MalgunGothic', '', size=16)
        document.cell(w=200, h=10, txt='EDA Report\n\n', ln=1, align='L')
        
        document.set_font('MalgunGothic', '', size=14)
        document.cell(w=200, h=10, txt='01. Data Information\n\n', ln=1, align='L')
        document.set_font('MalgunGothic', '', size=10)
        document.multi_cell(w=0, h=5, txt=info_str)
        
        document.add_page()
        document.set_font('MalgunGothic', '', size=14)
        document.cell(w=200, h=10, txt='02. Data Summary\n\n', ln=1, align='L')
        document.set_font('MalgunGothic', '', size=10)
        document.multi_cell(w=0, h=5, txt=summary_str)
        
        document.add_page()
        document.set_font('MalgunGothic', '', size=14)
        document.cell(w=200, h=10, txt='03. Data Correlation Analysis\n\n', ln=1, align='L')
        document.set_font('MalgunGothic', '', size=8)
        document.multi_cell(w=0, h=5, txt=correlation_str)
        
        document.output(filename)
        
    # KDE 파트 에러 수정
    # 그래프 개수 줄이기 + 가시성 개선
    # Style Update
    # y axes 지정
    def visualize(self, filepath):
        self._set_plot_style()
        
        if not filepath.endswith('/'):
            filepath += '/'
        os.makedirs(filepath, exist_ok=True)
        
        # Numerical Data
        for col in self.num_cols.tolist():
            try:
                # gname : Histogram
                # Not Y Axes
                plt.figure()
                sns.histplot(self.input[col], kde=False)
                self._save_plot(filepath, 'Histogram', col)
                
                # gname : KDE
                # Not Y Axes
                plt.figure()
                sns.kdeplot(self.input[col], kde=True)
                self._save_plot(filepath, 'KDE', col)
                
                # gname : Histogram_KDE
                # Not Y Axes
                plt.figure()
                sns.histplot(self.input[col], kde=True)
                self._save_plot(filepath, 'Histogram_KDE', col)
                
                # gname : BoxPlot
            
            except Exception as e:
                print(f"Could not plot numerical data for column {col}: {e}")
                pass
            
        # Categorical Data
        for col in self.cat_cols.tolist():
            try:
                # gname : CountPlot
                plt.figure()
                sns.countplot(x=self.input[col])
                self._save_plot(filepath, 'CountPlot', col)
                
                # gname : BarPlot
                plt.figure()
                sns.barplot(x=self.input[col].value_counts().index, y=self.input[col].value_counts())
                self._save_plot(filepath, 'BarPlot', col)
                
                # gname : PointPlot
                plt.figure()
                sns.pointplot(x=self.input[col].value_counts().index, y=self.input[col].value_counts())
                self._save_plot(filepath, 'PointPlot', col)
                
                # gname : BoxPlot
                plt.figure()
                sns.boxplot(x=self.input[col])
                self._save_plot(filepath, 'BoxPlot', col)
                
                # gname : ViolinPlot
                plt.figure()
                sns.violinplot(x=self.input[col])
                self._save_plot(filepath, 'ViolinPlot', col)
                
                # gname : PiePlot
                plt.figure()
                self.input[col].value_counts().plot.pie()
                self._save_plot(filepath, 'PiePlot', col)
                
            except Exception as e:
                print(f"Could not plot categorical data for column {col}: {e}")
                pass
        
        # gname : Heatmap
        try:
            plt.figure()
            sns.heatmap(self.input.corr(), annot=True)
            self._save_plot(filepath, 'Heatmap')
            
        except Exception as e:
            print(f"Could not plot heatmap: {e}")
            pass
        
        for i, col1 in enumerate(self.num_cols.tolist()):
            for col2 in self.num_cols.tolist()[i+1:]:
                try:
                    # gname : LinePlot
                    plt.figure()
                    sns.lineplot(x=self.input[col1], y=self.input[col2])
                    self._save_plot(filepath, 'LinePlot', col1, col2)

                    # gname : ScatterPlot
                    plt.figure()
                    sns.scatterplot(x=self.input[col1], y=self.input[col2])
                    self._save_plot(filepath, 'ScatterPlot', col1, col2)
                    
                    # gname : Abline
                    plt.figure()
                    sns.regplot(x=self.input[col1], y=self.input[col2], ci=None)
                    self._save_plot(filepath, 'Abline', col1, col2)

                except Exception as e:
                    print(f"Could not plot relationship for columns {col1} and {col2}: {e}")
                    pass