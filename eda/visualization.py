import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_loader import DataLoader

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
        
    def _save_plot(self, plot_func, plot_name, *args, cols=None, subplots=True, col_length=None, subplot_name=None, **kwargs):
        """
        플롯을 저장하는 메서드
        
        Parameters:
        -----------
        plot_func : function
            플롯 함수
        plot_name : str
            저장할 플롯 파일 이름
        *args : tuple
            플롯 함수에 전달할 위치 인자
        cols : list, optional
            subplot에 전달할 열
        subplots : boolean
            subplot의 사용 여부 (default=True)
        col_length : int
            subplot에 전달할 열의 길이
        subplot_name : str
            subplot에 전달할 타이틀 이름
        **kwargs : dict
            플롯 함수에 전달할 키워드 인자
        """
        if subplots:
            n = None
            max_n = 20
            for i in range(1, (max_n+1)):
                if (i-1)**2 < col_length < i**2:
                    n = i
                    break
            else:
                raise ValueError(f'col_length({col_length}) is larger than max_n({max_n}).')
            
            fig, axes = plt.subplots(n, n, figsize=(20, 20))
            axes = axes.flatten()
            
            for idx, col in enumerate(cols):
                if idx >= n * n:
                    break
                plot_func(self.input[col], ax=axes[idx], *args, **kwargs)
                axes[idx].set_title(subplot_name)
                
            for ax in axes[len(cols):]:
                fig.delaxes(ax)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, f"{plot_name}.png"))
            
        else:
            plt.figure()
            plot_func(*args, **kwargs)
            plt.title(plot_name)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, f"{plot_name}.png"))
                    
        self._clear_plot()
        print(f"Generating Plot : {plot_name} in {self.output_dir}")
        
    def visualize_numerical(self, bins=30, box_violin_y=None, hue=None):
        """
        Numerical Data를 시각화하는 메서드
        
        Parameters:
        -----------
        bins : int, optional
            histogram의 bin 수 (default=30)
        box_violin_y : str, optional
            boxplot & violinplot의 y축 데이터
        hue : str, optional
            Group화할 열 이름
        """
        # histogram / histogram_kde / kde
        self._save_plot(sns.histplot, 'histogram', cols=self.num_cols, subplots=True, col_length=len(self.num_cols), bins=bins, kde=False)
        self._save_plot(sns.histplot, 'histogram_kde', cols=self.num_cols, subplots=True, col_length=len(self.num_cols), bins=bins, kde=True)
        self._save_plot(sns.kdeplot, 'kde', cols=self.num_cols, subplots=True, col_length=len(self.num_cols), fill=True)
        
        # boxplot / violinplot
        if box_violin_y:
            if hue is not None and hue in self.num_cols:
                self._save_plot(sns.boxplot, f"boxplot_{box_violin_y}_{hue}", subplots=False, x=hue, y=box_violin_y, data=self.input)
                self._save_plot(sns.violinplot, f"violinplot_{box_violin_y}_{hue}", subplots=False, x=hue, y=box_violin_y, data=self.input)
            else:
                self._save_plot(sns.boxplot, f"boxplot_{box_violin_y}", subplots=False, y=self.input[box_violin_y])
                self._save_plot(sns.violinplot, f"violinplot_{box_violin_y}", subplots=False, y=self.input[box_violin_y])
        else:
            print(f"Any box_violin_y column specified for boxplot and violinplot.")
            
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
            
# df = sns.load_dataset('titanic')
# rc_params = {
#     'figure.figsize': (16, 12),
#     'axes.titlesize': 15,
#     'axes.labelsize': 12,
#     'xtick.labelsize': 10,
#     'ytick.labelsize': 10,
#     'legend.fontsize': 12,
#     'axes.grid': True,
#     'grid.alpha': 0.3,
#     'axes.unicode_minus': False,
#     'font.family': 'Malgun Gothic'
# }
# viz = Visualization(df, output_dir='./test/visualize_test/', style='whitegrid', font_scale=1.2, palette='deep', rc_params=rc_params)
# viz.visualize_numerical(bins=15, box_violin_y='fare', hue='pclass')