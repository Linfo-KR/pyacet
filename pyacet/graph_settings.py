import os
import matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib import font_manager, rcParams
from functools import wraps

from pyacet.resources import get_font_path
from pyacet.utils import *

class GraphSettings:
    def __init__(self, input, output_dir):
        self.input = input
        self.output_dir = ensure_trailing_slash(output_dir)
        self._set_font()
        create_output_directory(self.output_dir)
        matplotlib.use('Agg')
        plt.style.use('fast')
        
    def _clear_plot(self):
        plt.cla()
        plt.clf()
        plt.close()
        
    def _set_font(self):
        font_path = get_font_path('NanumGothic.ttf')
        font_property = font_manager.FontProperties(fname=font_path)
        rcParams['font.family'] = font_property.get_name()
        rcParams['axes.unicode_minus'] = False
        
    def save_plot(self, fig=None, axes=None, plot_name=str, n=None):
        if axes is not None and n and len(axes) > n:
            for ax in axes[n:]:
                fig.delaxes(ax)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f"{plot_name}.png"))
        self._clear_plot()
        print(f"Generating Plot : {plot_name}")
        
    # def save_plot(func):
    #     @wraps(func)
    #     def wrapper(self, plot_func, plot_name, kind, *args, **kwargs):
    #         result = func(self, plot_func, plot_name, kind, *args, **kwargs)
            
    #         if result is None:
    #             print(f"Warning: {func.__name__} returned None")
    #             return
            
    #         if isinstance(result, tuple) and len(result) == 3:
    #             fig, axes, updated_plot_name = result
    #         elif isinstance(result, tuple) and len(result) == 2:
    #             fig, axes = result
    #             updated_plot_name = plot_name
    #         else:
    #             fig, axes = result, None
    #             updated_plot_name = plot_name
            
    #         plt.tight_layout()
    #         plt.savefig(os.path.join(self.output_dir, f"{updated_plot_name}.png"))
    #         plt.close(fig)
    #         print(f"Generating Plot : {updated_plot_name}")
            
    #         return fig, axes

    #     return wrapper
    
    def calculate_ndim(self, kwargs, plot_type):
        def get_length(value):
            if value is not None:
                return len(value)
            else:
                return 1
        x = get_length(kwargs.get('x'))
        y = get_length(kwargs.get('y'))
        hue = get_length(kwargs.get('hue'))

        if plot_type == 'sub':
            nplots = x * y * hue
        elif plot_type == 'multi':
            if 'x' in kwargs and 'y' in kwargs and 'hue' in kwargs:
                nplots = y * hue
                if y > hue:
                    return y, hue
                else:
                    return hue, y
            elif 'x' in kwargs and 'y' in kwargs and 'hue' not in kwargs:
                nplots = max(x, y)
            elif ('x' in kwargs and 'y' not in kwargs and hue in kwargs) or ('x' not in kwargs and 'y' in kwargs and hue in kwargs):
                nplots = hue
        else:
            raise ValueError(f"Selected plot type({plot_type}) is invalid. Use 'sub' or 'multi'.")

        ncols = int(np.ceil(np.sqrt(nplots)))
        nrows = int(np.ceil(nplots / ncols))
        
        return nrows, ncols
    
    def set_axis_properties(self, subtitle, ax, sub, main, hue=None, src=None, mode=None):
        ax.tick_params(axis='x', rotation=45)
    
        if pd.api.types.is_datetime64_any_dtype(src[main]):
            self._set_datetime_axis(ax, src[main], mode)
        else:
            self._set_non_datetime_axis(ax, src[main])

        ax.set_title(subtitle)
        if ax.get_legend():
            handles, labels = ax.get_legend_handles_labels()
            reduce_labels = []
            if len(labels) > 10:
                handles = handles[:5] + handles[-5:]
                reduce_labels.append(labels[:5])
                reduce_labels.append(['...'])
                reduce_labels.append(labels[-5:])
            ax.legend().remove()
            ax.legend(handles, labels, title=hue, bbox_to_anchor=(1.05, 1), loc='best', ncol=2, fontsize=8)
        ax.set_xlabel(main)
        ax.set_ylabel(sub)

    def _set_datetime_axis(self, ax, date_series, mode):
        date_range = date_series.max() - date_series.min()
        
        if mode == 'hour':
            self._set_hour_axis(ax, date_range)
        elif date_range.days > 365 * 2:
            self._set_year_axis(ax)
        elif date_range.days > 30 * 6:
            self._set_month_axis(ax, interval=3)
        else:
            self._set_month_axis(ax)

    def _set_hour_axis(self, ax, date_range):
        if date_range.total_seconds() / 3600 > 24 * 7:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_minor_locator(mdates.HourLocator(interval=6))
            ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:00'))
        else:
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:00'))

    def _set_year_axis(self, ax):
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    def _set_month_axis(self, ax, interval=1):
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    def _set_non_datetime_axis(self, ax, data):
        if len(data) > 20:
            ax.xaxis.set_major_locator(plt.MaxNLocator(10))