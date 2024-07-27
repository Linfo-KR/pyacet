import seaborn as sns

from pyacet.data_loader import DataLoader
from pyacet.data_summary import DataSummary
from pyacet.graph_generator import GraphGenerator

class Visualization(GraphGenerator):
    def __init__(self, input, cols, output_dir):
        super().__init__(input, output_dir)
        self.input = DataLoader(input, cols).load_data()
        self.num_cols = DataLoader(input, cols).get_numerical_cols()
        self.cat_cols = DataLoader(input, cols).get_categorical_cols()
        self.dt_cols = DataLoader(input, cols).get_datetime_cols()
        self.corr_matrix = DataSummary(input, cols).data_correlation()
        self.output_dir = output_dir
        
        sns.set_theme(style='whitegrid', palette='deep')
        
    def visualize(self, exclude_cols=None):
        if exclude_cols is not None:
            self.input.columns = [cols for cols in self.input.columns if cols not in exclude_cols]
            self.cat_cols = [cols for cols in self.cat_cols if cols not in exclude_cols]
        else:
            self.input.columns = self.input.columns
            self.cat_cols = self.cat_cols
        
        if self.num_cols is not None:
            self.generate_logic(sns.histplot, 'histogram', kind='sub', x=self.num_cols, bins=15, kde=False)
            self.generate_logic(sns.histplot, 'histogram_kde', kind='sub', x=self.num_cols, bins=15, kde=True)
            self.generate_logic(sns.kdeplot, 'kde', kind='sub', x=self.num_cols, fill=True)
            self.generate_logic(sns.boxplot, 'box', kind='sub', y=self.num_cols)
            self.generate_logic(sns.violinplot, 'violin', kind='sub', y=self.num_cols)
            self.generate_logic(sns.heatmap, 'heatmap', kind='single', data=self.corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
            self.generate_logic(sns.boxplot, 'box', kind='multi', x=self.cat_cols, y=self.num_cols)
            self.generate_logic(sns.violinplot, 'violin', kind='multi', x=self.cat_cols, y=self.num_cols)
            self.generate_logic(sns.scatterplot, 'scatter', kind='multi', x=self.input.columns, y=self.num_cols)
        else:
            pass
        
        if self.cat_cols is not None:
            self.generate_logic(sns.barplot, 'bar', kind='multi', x=self.cat_cols, y=self.num_cols)
            self.generate_logic(sns.countplot, 'count', kind='multi', x=self.cat_cols)
        else:
            pass
        
        if self.dt_cols is not None:
            modes = ['all', 'year', 'quarter', 'month', 'day', 'hour']
            for mode in modes:
                self.generate_logic(sns.lineplot, 'line', kind='multi', x=self.dt_cols, y=self.num_cols, mode=mode)
        else:
            pass