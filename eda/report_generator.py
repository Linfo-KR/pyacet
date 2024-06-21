import io

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from fpdf import FPDF

from data_loader import DataLoader
from data_summary import DataSummary
from utils import *

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.header_font_size = 18
        self.lv1_font_size = 16
        self.lv2_font_size = 14
        self.lv3_font_size = 12
        self.content_font_size = 12
        self.table_font_size = 12
        self.content_margin = 10
        self.tbl_padding = 3
        self.new_x = 'LMARGIN'
        self.new_y = 'NEXT'
        
    def header(self):
        self.set_font('Helvetica', 'B', self.header_font_size)
        self.cell(0, 10, 'Data Summary Report', new_x=self.new_x, new_y=self.new_y, align='C')
        self.ln(self.content_margin)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', new_x=self.new_x, new_y=self.new_y, align='C')

    def chapter_title(self, title, level):
        if level == 1:
            self.set_font('Helvetica', 'B', self.lv1_font_size)
        elif level == 2:
            self.set_font('Helvetica', 'B', self.lv2_font_size)
        elif level == 3:
            self.set_font('Helvetica', 'B', self.lv3_font_size)
        else:
            self.set_font('Helvetica', 'B', self.content_font_size)
        self.cell(0, 10, title, new_x=self.new_x, new_y=self.new_y, align='L')
        self.ln(self.content_margin / 5)
        
    def chapter_body(self, title, body, level, none_title=False, last=False, custom_ln=None):
        if isinstance(body, tuple):
            body = ", ".join(map(str, body))
        elif isinstance(body, list):
            body = "\n".join(map(str, body))
        elif isinstance(body, dict):
            body = "\n".join(f"{k}: {v}" for k, v in body.items())
        elif isinstance(body, (int, float, np.integer, np.floating)):
            body = str(body)
        else:
            body = str(body)
            
        lines = body.split('\n')
        total_h = len(lines) * self.font_size * 1.5
        
        # Add space for title
        if level == 1:
            title_h = self.lv1_font_size * 1.5
        elif level == 2:
            title_h = self.lv2_font_size * 1.5
        elif level == 3:
            title_h = self.lv3_font_size * 1.5
        else:
            title_h = self.content_font_size * 1.5
            
        # Check if need to add a new page
        if self.get_y() + total_h + title_h > self.h - self.b_margin:
            self.add_page()
            self.chapter_title(title, level)
        else:
            if none_title:
                pass
            else:
                self.chapter_title(title, level)
        
        self.set_font('Helvetica', '', self.content_font_size)
        self.multi_cell(0, 10, body)
        if last:
            self.ln(self.content_margin)
        elif custom_ln is not None:
            self.ln(custom_ln)
        else:
            self.ln(self.content_margin / 10)

    def add_table(self, df):
        if isinstance(df, pd.DataFrame):
            df = df
        elif isinstance(df, dict):
            df = pd.DataFrame.from_dict(df, orient='columns')
        elif isinstance(df, list) or isinstance(df, np.ndarray):
            df = pd.DataFrame(df)
        else:
            print(f"Dataset isn't appropriate type{type(df)} to convert to table.")
            
        self.set_font('Helvetica', '', self.table_font_size)
        th = self.font_size
        
        # Calculate column and index widths
        idx_header_width = self.get_string_width('No')
        idx_value_width = max(self.get_string_width(str(idx)) for idx in df.index)
        idx_width = max(idx_value_width, idx_header_width) + self.tbl_padding
        
        col_widths = []
        for col in df.columns:
            header_width = self.get_string_width(str(col))
            value_width = max(self.get_string_width(str(val)) for val in df[col].values)
            col_width = max(header_width, value_width) + self.tbl_padding
            col_widths.append(col_width)
            
        # Calculate max columns per page(width)
        available_width = self.epw - idx_width
        max_cols_per_page = 0
        current_width = 0
        for width in col_widths:
            if current_width + width > available_width:
                break
            current_width += width
            max_cols_per_page += 1
            
        # Split dataframe into multiple tables
        for i in range(0, len(df.columns), max_cols_per_page):
            sub_df = df.iloc[:, i:i+max_cols_per_page]
            sub_col_widths = col_widths[i:i+max_cols_per_page]
            
            if self.get_y() + (len(df) + 1) * th > self.h - self.b_margin:
                self.add_page()
    
            # Add table header
            def add_table_header():
                self.cell(idx_width, th, 'No', border=1, align='C')
                for j, col in enumerate(sub_df.columns):
                    self.cell(sub_col_widths[j], th, str(col), border=1, align='C')
                self.ln()
            
            add_table_header()
        
            # Add table data
            for row in sub_df.itertuples(index=True, name=None):
                self.cell(idx_width, th, str(row[0]), border=1, align='C')
                for j, cell in enumerate(row[1:]):
                    cell_text = str(cell)
                    if sub_col_widths[j] < self.get_string_width(cell_text):
                        start_x = self.get_x()
                        start_y = self.get_y()
                        self.multi_cell(sub_col_widths[j], th, cell_text, border=1, align='C')
                        end_y = self.get_y()
                        self.set_xy(start_x + sub_col_widths[j], start_y)
                        if end_y > start_y:
                            self.set_y(end_y)
                    else:
                        self.cell(sub_col_widths[j], th, cell_text, border=1, align='C')
                self.ln()
                if self.get_y() > self.h - self.b_margin - th:
                    self.add_page()
                    add_table_header()
            self.ln(self.content_margin)

    def add_image(self, image):
        self.image(image, w=self.epw)
        self.ln(self.content_margin)

class ReportGenerator:
    def __init__(self, input, output_dir):
        self.summary = DataSummary(input)
        self.output_dir = output_dir

    def generate_report(self):
        pdf = PDF()
        pdf.add_page()
        
        # Data Info
        info, shape, head, nulls, duplicates = self.summary.data_info()
        pdf.chapter_title('01. Data Information', level=1)
        pdf.chapter_body('1.1. Data Information', info, level=2)
        pdf.chapter_body('1.2. Data Shape', shape, level=2, last=True)
        pdf.chapter_title('1.3. Data Head', level=2)
        pdf.add_table(head)
        pdf.chapter_body('1.4. Missing Values', nulls.to_dict(), level=2, last=True)
        pdf.chapter_body('1.5. Duplicated Rows', f"Number of duplicated rows : {duplicates} rows", level=2)
        pdf.chapter_body('', f"Number of data length : {shape[0]} rows", none_title=True, level=4)
        pdf.chapter_body('', f"Ratio of duplicated rows : {round((duplicates / shape[0]) * 100, 2)}%", none_title=True, level=4, last=True)

        # Numerical Summary
        numerical_summary = self.summary.data_numerical_summary()
        pdf.add_page()
        pdf.chapter_title('02. Numerical Columns Summary', level=1)
        pdf.chapter_title('2.1. Numerical Columns Statistics', level=2)
        pdf.add_table(numerical_summary)

        # Categorical Summary
        categorical_summary, features_dict = self.summary.data_categorical_summary()
        pdf.add_page()
        pdf.chapter_title('03. Categorical Columns Summary', level=1)
        pdf.chapter_title('3.1. Categorical Columns Statistics', level=2)
        pdf.add_table(categorical_summary)
        pdf.chapter_title('3.2. Features Information', level=2)
        for key, value in features_dict.items():
            features = value['features']
            num_features = value['num_features']
            body = f"Number of features : {num_features}\nFeatures :\n" + ", ".join(features)
            pdf.chapter_body(key, body, level=3, custom_ln=1)

        # Datetime Summary
        datetime_summary = self.summary.data_datetime_summary()
        pdf.add_page()
        pdf.chapter_title('04. Datetime Columns Summary', level=1)
        for idx, (key, value) in enumerate(datetime_summary.items()):
            pdf.chapter_title(f"4.{idx+1}. {key}", level=2)
            pdf.add_table(pd.DataFrame(value))

        # Correlation Matrix
        pdf.add_page()
        pdf.chapter_title('05. Correlation Matrix', level=1)
        if self.summary.data_correlation() is not None:
            fig, ax = plt.subplots(figsize=(5, 5))
            sns.heatmap(data=self.summary.data_correlation(), annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            plt.close(fig)
            buf.seek(0)
            pdf.add_image(buf)
        else:
            print("Correlation matrix isn't exist.")

        # Save PDF
        pdf.output(self.output_dir)