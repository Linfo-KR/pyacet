import io
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pyacet.data_loader import DataLoader
from pyacet.data_summary import DataSummary
from pyacet.pdf import PDF
from pyacet.utils import *

class ReportGenerator:
    def __init__(self, input, cols, output_dir, dataset_name):
        self.summary = DataSummary(input, cols)
        self.output_dir = ensure_trailing_slash(output_dir)
        self.dataset_name = dataset_name
        create_output_directory(self.output_dir)

    def generate_report(self, exclude_cols):
        pdf = PDF(self.dataset_name)
        pdf.add_page()

        self._add_data_info_section(pdf)
        self._add_numerical_summary_section(pdf)
        self._add_categorical_summary_section(pdf, exclude_cols)
        self._add_datetime_summary_section(pdf)
        self._add_correlation_matrix_section(pdf)

        pdf.output(os.path.join(self.output_dir, 'report.pdf'))
        print(f'Generating {self.dataset_name} Data Summary Report in {self.output_dir}.')

    def _add_data_info_section(self, pdf):
        info, shape, head, nulls, duplicates = self.summary.data_info()
        pdf.chapter_title('01. Data Information', level=1)
        pdf.chapter_body('1.1. Data Shape', shape, level=2, last=True)
        pdf.add_table(head, '1.2. Data Head', level=2)
        pdf.chapter_body('1.3. Data Information', info, level=2)
        pdf.chapter_body('1.4. Missing Values', nulls.to_dict(), level=2, last=True)
        pdf.chapter_body('1.5. Duplicated Rows', f"Number of duplicated rows : {duplicates} rows", level=2)
        pdf.chapter_body('', f"Number of data length : {shape[0]} rows", none_title=True, level=4)
        pdf.chapter_body('', f"Ratio of duplicated rows : {round((duplicates / shape[0]) * 100, 2)}%", none_title=True, level=4, last=True)

    def _add_numerical_summary_section(self, pdf):
        pdf.add_page()
        pdf.chapter_title('02. Numerical Columns Summary', level=1)
        numerical_summary = self.summary.data_numerical_summary()
        if numerical_summary is not None:
            pdf.add_table(numerical_summary, '2.1. Numerical Columns Statistics', level=2)
        else:
            pdf.chapter_body('', "Numerical summary isn't exist.", level=4, none_title=True, last=True)

    def _add_categorical_summary_section(self, pdf, exclude_cols):
        pdf.add_page()
        pdf.chapter_title('03. Categorical Columns Summary', level=1)
        categorical_summary = self.summary.data_categorical_summary(exclude_cols=exclude_cols)
        if categorical_summary is not None:
            categorical_summary, features_dict = categorical_summary
            pdf.add_table(categorical_summary, '3.1. Categorical Columns Statistics', level=2)
            pdf.chapter_title('3.2. Features Information', level=2)
            self._add_features_info(pdf, features_dict)
        else:
            pdf.chapter_body('', "Categorical summary isn't exist.", level=4, none_title=True, last=True)

    def _add_features_info(self, pdf, features_dict):
        for key, value in features_dict.items():
            features = value['features']
            num_features = value['num_features']
            body = f"Number of features : {num_features}\nFeatures :\n" + ", ".join(features)
            pdf.chapter_body(key, body, level=3, custom_ln=1)

    def _add_datetime_summary_section(self, pdf):
        pdf.add_page()
        pdf.chapter_title('04. Datetime Columns Summary', level=1)
        datetime_summary = self.summary.data_datetime_summary()
        if datetime_summary is not None:
            for idx, (key, value) in enumerate(datetime_summary.items()):
                if key == 'summary':
                    pdf.add_table(pd.DataFrame(value), f"4.{idx + 1}. Datetime Columns Statistics", level=2, none_title=False)
                else:
                    pdf.add_table(pd.DataFrame(value), f"4.{idx + 1}. {key}", level=2, none_main_title=True, none_title=False)
        else:
            pdf.chapter_body('', "Datetime summary isn't exist.", level=4, none_title=True, last=True)

    def _add_correlation_matrix_section(self, pdf):
        pdf.add_page()
        pdf.chapter_title('05. Correlation Matrix', level=1)
        correlation_matrix = self.summary.data_correlation()
        if correlation_matrix is not None:
            self._add_correlation_matrix_image(pdf, correlation_matrix)
        else:
            pdf.chapter_body('', "Correlation matrix isn't exist.", level=4, none_title=True, last=True)

    def _add_correlation_matrix_image(self, pdf, correlation_matrix):
        fig, ax = plt.subplots(figsize=(15, 15))
        sns.heatmap(data=correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        pdf.add_image(buf)