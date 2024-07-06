import numpy as np
import matplotlib.pyplot as plt

from pyacet.graph_settings import GraphSettings
from pyacet.utils import *


class GraphGenerator(GraphSettings):
    def __init__(self, input, output_dir):
        super().__init__(input, output_dir)
        self.input = input
        self.output_dir = output_dir
    
    def _create_subplots(self, nrows, ncols):
        fig, axes = plt.subplots(nrows, ncols, figsize=(5*nrows, 5*ncols))
        if nrows == 1 and ncols == 1:
            axes = np.array([[axes]])
        elif nrows == 1 or ncols == 1:
            axes = np.array([axes]).reshape(nrows, ncols)
            
        return fig, axes.flatten()
    
    def _generate_single(self, plot_func, plot_name, *args, **kwargs):
        fig, ax = plt.subplots(figsize=(20, 20))
        plot_func(*args, ax=ax, **kwargs)
        ax.set_title(plot_name)
        self.save_plot(fig, [ax], plot_name)
    
    def _generate_sub(self, plot_func, plot_name, *args, **kwargs):
        src = self.input
        nrows, ncols = self.calculate_ndim(kwargs, 'sub')
        fig, axes = self._create_subplots(nrows, ncols)
        
        mains = kwargs.pop('x', None) if 'x' in kwargs else kwargs.pop('y', None)
        for i, main in enumerate(mains):
            if i >= len(axes):
                break
            plot_func(data=src[main], ax=axes[i], *args, **kwargs)
        self.save_plot(fig, axes, plot_name, len(mains))
    
    def _generate_multi(self, plot_func, plot_name, *args, **kwargs):
        plot_types = {
            'numerical' : ('boxplot', 'violinplot', 'scatterplot'),
            'categorical' : ('barplot', 'countplot'),
            'datetime' : ('lineplot',)
        }
        plot_type = next(key for key, value in plot_types.items() if plot_func.__name__ in value)
        
        src = self.input
        if plot_type == 'numerical':
            self._generate_numerical(plot_func, plot_name, src, *args, **kwargs)
        elif plot_type == 'categorical':
            self._generate_categorical(plot_func, plot_name, src, *args, **kwargs)
        elif plot_type == 'datetime':
            self._generate_datetime(plot_func, plot_name, src, *args, **kwargs)
    
    def _generate_numerical(self, plot_func, plot_name, src, *args, **kwargs):
        mains, subs = kwargs.get('y'), kwargs.get('x')
        for main in mains:
            kwargs_clone = kwargs.copy()
            kwargs_clone['x'], kwargs_clone['y'] = main, subs
            nrows, ncols = self.calculate_ndim(kwargs_clone, 'multi')
            fig, axes = self._create_subplots(nrows, ncols)
            
            for j, sub in enumerate(subs):
                if j >= len(axes):
                    break
                kwargs_clone['y'] = sub
                plot_func(src, ax=axes[j], *args, **kwargs_clone)
            
            self.save_plot(fig, axes, f"{plot_name}_{main}", len(subs))
            
    def _generate_categorical(self, plot_func, plot_name, src, *args, **kwargs):
        mains, subs = kwargs.get('x'), kwargs.get('y')
        hues = mains.copy()
        
        for main in mains:
            kwargs_clone = kwargs.copy()
            kwargs_clone['x'], kwargs_clone['y'] = main, subs
            hues = hues[hues != main]
            if hues is None:
                print('Any hues are available.')
                pass
            else:
                kwargs_clone['hue'] = hues.copy()
                
                nrows, ncols = self.calculate_ndim(kwargs_clone, 'multi')
                fig, axes = self._create_subplots(nrows, ncols) 
                
                if subs is None:
                    self._plot_without_subs(plot_func, src, axes, hues, main, kwargs_clone, *args)
                    self.save_plot(fig, axes, f"{plot_name}_{main}", len(hues))
                else:
                    self._plot_with_subs(plot_func, src, axes, subs, hues, main, kwargs_clone, *args)
                    self.save_plot(fig, axes, f"{plot_name}_{main}", n=len(subs) * len(hues))
                    
                hues = mains.copy()
                
    def _plot_without_subs(self, plot_func, src, axes, hues, main, kwargs_clone, *args):
        for k, hue in enumerate(hues):
            if k >= len(axes):
                break
            kwargs_clone['hue'] = hue
            ax = axes[k]
            plot_func(src, ax=axes[k], *args, **kwargs_clone)
            kwargs_clone['hue'] = hues
            title = f"{main} by {hue}"
            self.set_axis_properties(title, ax, hue, main, src=src)

    def _plot_with_subs(self, plot_func, src, axes, subs, hues, main, kwargs_clone, *args):
        for j, sub in enumerate(subs):
            for k, hue in enumerate(hues):
                if j * len(hues) + k >= len(axes):
                    break
                kwargs_clone['y'], kwargs_clone['hue'] = sub, hue
                ax = axes[j * len(hues) + k]
                plot_func(src, ax=ax, *args, **kwargs_clone)
                title = f"{sub} by {main} (hue : {hue})"
                self.set_axis_properties(title, ax, sub, main, hue=hue, src=src)
    
    def _generate_datetime(self, plot_func, plot_name, src, *args, **kwargs):
        mains, subs, mode = kwargs.get('x'), kwargs.get('y'), kwargs.get('mode')
    
        mode_group = {
            'year': lambda x: x.dt.year,
            'quarter': lambda x: x.dt.to_period('Q').astype('period[Q]'),
            'month': lambda x: x.dt.to_period('M').astype('period[M]'),
            'day': lambda x: x.dt.date,
            'hour': lambda x: x.dt.floor('H'),
            'all': lambda x: x
        }
        
        if mode not in mode_group:
            raise ValueError(f"Selected mode({mode}) is invalid. Use 'year' or 'quarter' or 'month' or 'day' or 'hour'.")
        
        for main in mains:
            kwargs_clone = kwargs.copy()
            kwargs_clone['x'], kwargs_clone['y'] = main, subs
            kwargs_clone.pop('mode', None)
            nrows, ncols = self.calculate_ndim(kwargs_clone, 'multi')
            
            for agg_func in ['mean', 'median']:
                fig, axes = self._create_subplots(nrows, ncols)
                for j, sub in enumerate(subs):
                    if j >= len(axes):
                        break
                    
                    if mode == 'all':
                        src_group = src[[main, sub]].copy()
                    else:
                        group = src.groupby(mode_group[mode](src[main]))
                        if agg_func == 'mean':
                            src_group = group[sub].mean().reset_index()
                        else:
                            src_group = group[sub].median().reset_index()
                    src_group[main] = src_group[main].astype(str)
                    
                    kwargs_clone['y'] = sub
                    plot_func(src_group, ax=axes[j], *args, **kwargs_clone)
                    axes[j].tick_params(axis='x', rotation=45)
                    
                    title = f"{sub} by {main}"
                    if mode is not None:
                        title += f" (mode: {mode}, agg_func: {agg_func})"
                    self.set_axis_properties(title, axes[j], sub, main, src=src_group, mode=mode)
                
                plot_name_suffix = f"_{mode}" if mode is not None else ""
                self.save_plot(fig, axes, f"{plot_name}_{main}{plot_name_suffix}_{agg_func}", len(subs))
    
    def generate_logic(self, plot_func, plot_name, kind, *args, **kwargs):
        if kind == 'single':
            self._generate_single(plot_func, plot_name, *args, **kwargs)
        elif kind == 'sub':
            self._generate_sub(plot_func, plot_name, *args, **kwargs)
        elif kind == 'multi':
            self._generate_multi(plot_func, plot_name, *args, **kwargs)