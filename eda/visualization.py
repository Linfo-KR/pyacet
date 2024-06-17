import os

import matplotlib.pyplot as plt
import seaborn as sns

from data_loader import DataLoader
from utils import *

class Visualization:
    def __init__(self, input, output_dir, style='seaborn', font_scale=1.2, palette='deep', rc_params=None):
        """
        데이터 시각화 클래스
        
        Parameters:
        -----------
        input : pandas.DataFrame
            시각화할 데이터프레임
        output_dir : str, optional
            시각화 결과를 저장할 디렉토리 경로 (기본값: 'output')
        style : str, optional
            시각화 스타일 (기본값: 'seaborn')
        font_scale : float, optional
            폰트 크기 조절 (기본값: 1.2)
        palette : str, optional
            색상 팔레트 (기본값: 'deep')
        rc_params : dict, optional
            rcParams 설정을 위한 딕셔너리 (기본값: None)
        """
        self.input = DataLoader(input).load_data()
        self.num_cols = DataLoader(input).get_numerical_cols()
        self.cat_cols = DataLoader(input).get_categorical_cols()
        self.dt_cols = DataLoader(input).get_datetime_cols()
        self.output_dir = output_dir
        
        if not self.output_dir.endswith('/'):
            self.output_dir += '/'
            
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
            
        if rc_params:
            plt.rcParams.update(rc_params)
        plt.ioff()
        
        sns.set_theme(style=style, font_scale=font_scale, palette=palette)
        
    def _clear_plot(self):
        plt.cla()
        plt.clf()
        plt.close()
        
    def _generate_logic(self, plot_func, plot_name, *args, single_plot=True, subplots=False, cols=None, multi_plot=False, **kwargs):
        """
        Plot을 생성하는 Logic 메소드
        
        Parameters:
        -----------
        plot_func : function
            플롯 함수
        plot_name : str
            저장할 플롯 파일 이름
        *args : tuple
            플롯 함수에 전달할 위치 인자
        single_plot : boolean
            single plot의 생성 여부 (default=True)
        subplots : boolean
            subplot의 사용 여부 (default=False)    
        cols : list, optional
            subplot에 전달할 열
        multi_plot : boolean
            multi plot(multi hues)의 사용 여부 (default=False)
        **kwargs : dict
            플롯 함수에 전달할 키워드 인자
        """
        if single_plot:
            fig, ax = plt.subplots()
            plot_func(*args, ax=ax, **kwargs)
            ax.set_title(plot_name)
            self._save_plot(fig, [ax], plot_name)
        
        elif subplots:
            if multi_plot:
                for idx, col in enumerate(cols):
                    n = calculate_ndim(col_length=len(kwargs['x']))
                    fig, axes = plt.subplots(n, n, figsize=(20, 20))
                    axes = axes.flatten()
                    if 'x' in kwargs:
                        hues = kwargs['x']
                        if not isinstance(hues, list):
                            hues = [hues]
                        for idx_h, hue in enumerate(hues):
                            if idx_h >= n * n:
                                break
                            kwargs['x'] = hue
                            kwargs['y'] = col
                            plot_func(data=self.input, ax=axes[idx_h], *args, **kwargs)
                            axes[idx_h].set_xlabel(hue)
                            axes[idx_h].set_ylabel(col)
                            
                        kwargs['x'] = hues
                        self._save_plot(fig, axes, f"{plot_name}_{col}", len(hues))
            else:
                n = calculate_ndim(col_length=len(cols))
                fig, axes = plt.subplots(n, n, figsize=(20, 20))
                axes = axes.flatten()
                
                for idx, col in enumerate(cols):
                    if idx >= n * n:
                        break
                    plot_func(self.input[col], ax=axes[idx], *args, **kwargs)
                    
                self._save_plot(fig, axes, plot_name, len(cols))
            
    def _save_plot(self, fig=None, axes=None, plot_name=str, n=None):
        """
        Plot을 저장하는 메서드
        
        Parameters:
        -----------
        fig : matplotlib.figure.Figure
            _generate_logic()으로 부터 전달받은 fig 객체
        axes : list of matplotlib.axes._subplots.AxesSubplot
            _generate_logic()으로 부터 전달받은 axes 객체
        file_name : str
            저장할 Plot의 file name
        n : int
            subplot 내 생성되는 plot의 수(len(cols) or len(hues))
        """
        if axes is not None and n and len(axes) > n:
            for ax in axes[n:]:
                fig.delaxes(ax)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f"{plot_name}.png"))
        self._clear_plot()
        print(f"Generating Plot : {plot_name} in {self.output_dir}")
    
    def visualize_numerical(self, bins=30, hue_list=list):
        """
        Numerical Data를 시각화하는 메서드
        
        Parameters:
        -----------
        bins : int, optional
            histogram의 bin 수 (default=30)
        hue : list
            Group화할 열의 list
        y_hue_none : boolean
            box_violin_y와 hue의 None 여부
        """
        # histogram / histogram_kde / kde
        self._generate_logic(sns.histplot, 'histogram', single_plot=False, subplots=True, cols=self.num_cols, multi_plot=False, bins=bins, kde=False)
        self._generate_logic(sns.histplot, 'histogram_kde', single_plot=False, subplots=True, cols=self.num_cols, multi_plot=False, bins=bins, kde=True)
        self._generate_logic(sns.kdeplot, 'kde', single_plot=False, subplots=True, cols=self.num_cols, multi_plot=False, fill=True)
        
        # boxplot / violinplot
        if hue is not None and isinstance(hue, list):
        # if hue is exist
            self._generate_logic(sns.boxplot, 'boxplot', single_plot=False, subplots=True, cols=self.num_cols, multi_plot=True, x=hue_list)
            self._generate_logic(sns.violinplot, 'violinplot', single_plot=False, subplots=True, cols=self.num_cols, multi_plot=True, x=hue_list)
        else:
            print('hue_list is Empty.')
            
        # if hue isn't exist
        self._generate_logic(sns.boxplot, 'boxplot', single_plot=False, subplots=True, cols=self.num_cols, multi_plot=False)
        self._generate_logic(sns.violinplot, 'violinplot', single_plot=False, subplots=True, cols=self.num_cols, multi_plot=False)
            
        def visualize_categorical(self):
            """
            Categorical Data를 시각화하는 메서드
            
            Parameters:
            -----------
            bins : int, optional
                histogram의 bin 수 (default=30)
            box_violin_y : str, optional
                boxplot & violinplot의 y축 데이터
            hue : str, optional
                Group화할 열 이름
            """
            # barplot
            
            # pieplot
            
            # countplot
            
df = sns.load_dataset('titanic')
rc_params = {
    'figure.figsize': (16, 12),
    'axes.titlesize': 15,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 12,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.unicode_minus': False,
    'font.family': 'Malgun Gothic'
}
viz = Visualization(df, output_dir='./test/visualize_test/', style='whitegrid', font_scale=1.2, palette='deep', rc_params=rc_params)
hue = ['survived', 'pclass', 'sex', 'embarked']
viz.visualize_numerical(bins=15, hue_list=hue)