import datetime as dt
import numpy as np
import pandas as pd

from fpdf import FPDF
from PIL import Image

from pyacet.resources import get_font_path

class PDF(FPDF):
    def __init__(self, dataset_name):
        super().__init__()
        self.dataset_name = dataset_name
        self.generate_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.header_font_size = 18
        self.lv1_font_size = 16
        self.lv2_font_size = 14
        self.lv3_font_size = 12
        self.content_font_size = 12
        self.table_font_size = 12
        self.content_margin = 10
        self.page_padding = 3
        self.tbl_padding = 3
        self.img_padding = 5
        self.new_x = 'LMARGIN'
        self.new_y = 'NEXT'
        self.add_font('NanumGothic', '', get_font_path('NanumGothic.ttf'), uni=True)
        self.add_font('NanumGothic', 'B', get_font_path('NanumGothicBold.ttf'), uni=True)
        self.add_font('NanumGothic', 'I', get_font_path('NanumGothicExtraBold.ttf'), uni=True)

    def header(self):
        self.set_font('NanumGothic', 'B', self.header_font_size)
        self.cell(0, 10, 'Data Summary Report', new_x=self.new_x, new_y=self.new_y, align='C')
        self.set_font('NanumGothic', 'B', self.lv2_font_size)
        self.cell(0, 10, f"- {self.dataset_name} Dataset -", new_x=self.new_x, new_y=self.new_y, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('NanumGothic', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', new_x=self.new_x, new_y=self.new_y, align='C')
        self.set_y(-15)
        self.cell(0, 10, f"Generated at {self.generate_time}", new_x=self.new_x, new_y=self.new_y, align='R')

    def chapter_title(self, title, level):
        font_size = {
            1: self.lv1_font_size,
            2: self.lv2_font_size,
            3: self.lv3_font_size
        }.get(level, self.content_font_size)
        self.set_font('NanumGothic', 'B', font_size)
        self.cell(0, 10, title, new_x=self.new_x, new_y=self.new_y, align='L')
        self.ln(self.content_margin / 5)
        
    def chapter_body(self, title, body, level, none_title=False, last=False, custom_ln=None):
        if body is None:
            print('Contents are None.')
            return
        
        body = self._format_body(body)
        total_h = len(body.split('\n')) * self.font_size * 1.5
        title_h = {
            1: self.lv1_font_size,
            2: self.lv2_font_size,
            3: self.lv3_font_size
        }.get(level, self.content_font_size) * 1.5
        
        if self.get_y() + total_h + title_h > self.h - self.b_margin:
            self.add_page()
            self.chapter_title(title, level)
        elif not none_title:
            self.chapter_title(title, level)
        
        self.set_font('NanumGothic', '', self.content_font_size)
        self.multi_cell(0, 10, body)
        
        if last:
            self.ln(self.content_margin)
        elif custom_ln is not None:
            self.ln(custom_ln)
        else:
            self.ln(self.content_margin / 10)
        
    def add_table(self, df, title, level, none_main_title=False, none_title=True):
        if df is None:
            print('df is None')
            return
        
        df = self._convert_to_dataframe(df)
        self.set_font('NanumGothic', '', self.table_font_size)
        tbl_h = self.font_size + 2

        idx_width, col_widths = self._calculate_widths(df)
        max_cols_per_page = self._calculate_max_cols_per_page(idx_width, col_widths)
        
        if not none_main_title:
            self.chapter_title(title, level)
            
        for sub_col_idx in max_cols_per_page:
            sub_df, sub_col_widths = self._split_dataframe(df, col_widths, len(sub_col_idx))
            df, col_widths = df.iloc[:, len(sub_col_idx):], col_widths[len(sub_col_idx):]
            
            if self.get_y() + (len(sub_df) + 1) * tbl_h > self.h - self.b_margin:
                self.add_page()
                if not none_title:
                    self.chapter_title(title, level)

            self.set_font('NanumGothic', '', self.table_font_size)
            self._add_table_header(idx_width, sub_df, sub_col_widths, tbl_h)
            self._add_table_data(idx_width, sub_df, sub_col_widths, tbl_h)

            self.ln(self.content_margin)
        
    def add_image(self, image):
        available_width = self.epw - 2 * self.img_padding
        origin_w, origin_h = self._get_image_dims(image)
        aspect_ratio = origin_h / origin_w
        
        new_w = available_width
        new_h = new_w * aspect_ratio
        
        self.image(image, x='C', w=new_w, h=new_h)
        self.ln(self.content_margin)

    def _format_body(self, body):
        if isinstance(body, tuple):
            return ", ".join(map(str, body))
        elif isinstance(body, list):
            return "\n".join(map(str, body))
        elif isinstance(body, dict):
            return "\n".join(f"{k}: {v}" for k, v in body.items())
        elif isinstance(body, (int, float, np.integer, np.floating)):
            return str(body)
        else:
            return str(body)

    def _convert_to_dataframe(self, df):
        if isinstance(df, pd.DataFrame):
            return df
        elif isinstance(df, dict):
            return pd.DataFrame.from_dict(df, orient='columns')
        elif isinstance(df, (list, np.ndarray)):
            return pd.DataFrame(df)
        else:
            print(f"Dataset isn't appropriate type {type(df)} to convert to table.")
            return None
        
    def _calculate_widths(self, df):
        idx_header_width = self.get_string_width('No')
        idx_value_width = max(self.get_string_width(str(idx)) for idx in df.index)
        idx_width = max(idx_value_width, idx_header_width) + self.tbl_padding
        
        col_widths = []
        for col in df.columns:
            header_width = self.get_string_width(str(col))
            value_width = max(self.get_string_width(str(val)) for val in df[col].values)
            col_width = max(header_width, value_width) + self.tbl_padding
            col_widths.append(col_width)
        
        return idx_width, col_widths

    def _calculate_max_cols_per_page(self, idx_width, col_widths):
        available_width = self.epw - idx_width - 2 * self.page_padding
        max_cols_per_page = []
        current_width = 0
        current_cols = []
        for width in col_widths:
            if current_width + width > available_width:
                max_cols_per_page.append(current_cols)
                current_cols = [width]
                current_width = width
            else:
                current_cols.append(width)
                current_width += width
                
        if current_cols:
            max_cols_per_page.append(current_cols)
            
        return max_cols_per_page

    def _split_dataframe(self, df, col_widths, num_cols):
        sub_df = df.iloc[:, :num_cols]
        sub_col_widths = col_widths[:num_cols]
        return sub_df, sub_col_widths

    def _add_table_header(self, idx_width, sub_df, sub_col_widths, tbl_h):
        self.cell(idx_width, tbl_h, 'No', border=1, align='C')
        for j, col in enumerate(sub_df.columns):
            self.cell(sub_col_widths[j], tbl_h, str(col), border=1, align='C')
        self.ln()

    def _add_table_data(self, idx_width, sub_df, sub_col_widths, tbl_h):
        for row in sub_df.itertuples(index=True, name=None):
            self.cell(idx_width, tbl_h, str(row[0]), border=1, align='C')
            for j, cell in enumerate(row[1:]):
                cell_text = str(cell)
                if sub_col_widths[j] < self.get_string_width(cell_text):
                    start_x = self.get_x()
                    start_y = self.get_y()
                    self.multi_cell(sub_col_widths[j], tbl_h, cell_text, border=1, align='C')
                    end_y = self.get_y()
                    self.set_xy(start_x + sub_col_widths[j], start_y)
                    if end_y > start_y:
                        self.set_y(end_y)
                else:
                    self.cell(sub_col_widths[j], tbl_h, cell_text, border=1, align='C')
            self.ln()
            if self.get_y() > self.h - self.b_margin:
                self.add_page()
                self._add_table_header(idx_width, sub_df, sub_col_widths, tbl_h)

    def _get_image_dims(self, image):
        if isinstance(image, (str, bytes)):
            with Image.open(image) as img:
                return img.size
        else:
            img = Image.open(image)
            return img.size