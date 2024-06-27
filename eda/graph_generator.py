import os

import numpy as np
import matplotlib.pyplot as plt

from functools import wraps


class GraphGenerator:
    def __init__(self, input, output_dir):
        self.input = input
        self.output_dir = self._ensure_trailing_slash(output_dir)
        self._create_output_directory()
        
    def _ensure_trailing_slash(self, path):
        return path if path.endswith('/') else path + '/'

    def _create_output_directory(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
        
    def _clear_plot(self):
        plt.cla()
        plt.clf()
        plt.close()
        
    def _save_plot(self, fig=None, axes=None, plot_name=str, n=None):
        if axes is not None and n and len(axes) > n:
            for ax in axes[n:]:
                fig.delaxes(ax)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f"{plot_name}.png"))
        self._clear_plot()
        print(f"Generating Plot : {plot_name}")
        
    def save_plot(func):
        @wraps(func)
        def wrapper(self, plot_func, plot_name, kind, *args, **kwargs):
            result = func(self, plot_func, plot_name, kind, *args, **kwargs)
            
            if result is None:
                print(f"Warning: {func.__name__} returned None")
                return
            
            if isinstance(result, tuple) and len(result) == 3:
                fig, axes, updated_plot_name = result
            elif isinstance(result, tuple) and len(result) == 2:
                fig, axes = result
                updated_plot_name = plot_name
            else:
                fig, axes = result, None
                updated_plot_name = plot_name
            
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, f"{updated_plot_name}.png"))
            plt.close(fig)
            print(f"Generating Plot : {updated_plot_name}")
            
            return fig, axes

        return wrapper
    
    def _calculate_ndim(self, kwargs, plot_type):
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
            raise ValueError("Invalid plot_type. Use 'sub' or 'multi'.")

        ncols = int(np.ceil(np.sqrt(nplots)))
        nrows = int(np.ceil(nplots / ncols))
        
        return nrows, ncols
    
    def _create_subplots(self, nrows, ncols):
        fig, axes = plt.subplots(nrows, ncols, figsize=(5*nrows, 5*ncols))
        if nrows == 1 and ncols == 1:
            axes = np.array([[axes]])
        elif nrows == 1 or ncols == 1:
            axes = np.array([axes]).reshape(nrows, ncols)
            
        return fig, axes.flatten()
    
    def _generate_single(self, plot_func, plot_name, *args, **kwargs):
        fig, ax = plt.subplots()
        plot_func(*args, ax=ax, **kwargs)
        ax.set_title(plot_name)
        self._save_plot(fig, [ax], plot_name)
        
    def _generate_sub(self, plot_func, plot_name, *args, **kwargs):
        src = self.input
        nrows, ncols = self._calculate_ndim(kwargs, 'sub')
        fig, axes = self._create_subplots(nrows, ncols)
        
        mains = kwargs.pop('x', None) if 'x' in kwargs else kwargs.pop('y', None)
        for i, main in enumerate(mains):
            if i >= len(axes):
                break
            plot_func(data=src[main], ax=axes[i], *args, **kwargs)
        self._save_plot(fig, axes, plot_name, len(mains))
        
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
            nrows, ncols = self._calculate_ndim(kwargs_clone, 'multi')
            fig, axes = self._create_subplots(nrows, ncols)
            
            for j, sub in enumerate(subs):
                if j >= len(axes):
                    break
                kwargs_clone['y'] = sub
                plot_func(src, ax=axes[j], *args, **kwargs_clone)
            
            self._save_plot(fig, axes, f"{plot_name}_{main}", len(subs))

    def _generate_categorical(self, plot_func, plot_name, src, *args, **kwargs):
        mains, subs = kwargs.get('x'), kwargs.get('y')
        hues = mains.copy()
        
        for main in mains:
            kwargs_clone = kwargs.copy()
            kwargs_clone['x'], kwargs_clone['y'] = main, subs
            hues = hues[hues != main]
            if hues is None:
                print('No hues are available.')
                pass
            else:
                kwargs_clone['hue'] = hues.copy()
                hues = mains.copy()

                nrows, ncols = self._calculate_ndim(kwargs_clone, 'multi')
                fig, axes = self._create_subplots(nrows, ncols)
                
                if subs is None:
                    self._plot_without_subs(plot_func, src, axes, hues, kwargs_clone, *args)
                else:
                    self._plot_with_subs(plot_func, src, axes, subs, hues, main, kwargs_clone, *args)
                
                self._save_plot(fig, axes, f"{plot_name}_{main}", len(hues))

    def _plot_without_subs(self, plot_func, src, axes, hues, kwargs_clone, *args):
        for k, hue in enumerate(hues):
            if k >= len(axes):
                break
            kwargs_clone['hue'] = hue
            plot_func(src, ax=axes[k], *args, **kwargs_clone)
            kwargs_clone['hue'] = hues

    def _plot_with_subs(self, plot_func, src, axes, subs, hues, main, kwargs_clone, *args):
        for j, sub in enumerate(subs):
            for k, hue in enumerate(hues):
                if j * len(hues) + k >= len(axes):
                    break
                kwargs_clone['y'], kwargs_clone['hue'] = sub, hue
                ax = axes[j * len(hues) + k]
                plot_func(src, ax=ax, *args, **kwargs_clone)
                self._set_axis_properties(ax, sub, main, hue)
            kwargs_clone['y'] = subs

    def _set_axis_properties(self, ax, sub, main, hue):
        ax.set_title(f"{sub} by {main} (hue : {hue})")
        if ax.get_legend():
            ax.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='best')
        ax.set_xlabel(main)
        ax.set_ylabel(sub)

    def _generate_datetime(self, plot_func, plot_name, src, *args, **kwargs):
        mains, subs = kwargs.get('x'), kwargs.get('y')
        for main in mains:
            kwargs_clone = kwargs.copy()
            kwargs_clone['x'], kwargs_clone['y'] = main, subs
            nrows, ncols = self._calculate_ndim(kwargs_clone, 'multi')
            fig, axes = self._create_subplots(nrows, ncols)
            
            for j, sub in enumerate(subs):
                if j >= len(axes):
                    break
                kwargs_clone['y'] = sub
                plot_func(src, ax=axes[j], *args, **kwargs_clone)
            
            self._save_plot(fig, axes, f"{plot_name}_{main}", len(subs))

    def generate_logic(self, plot_func, plot_name, kind, *args, **kwargs):
        if kind == 'single':
            self._generate_single(plot_func, plot_name, *args, **kwargs)
        elif kind == 'sub':
            self._generate_sub(plot_func, plot_name, *args, **kwargs)
        elif kind == 'multi':
            self._generate_multi(plot_func, plot_name, *args, **kwargs)