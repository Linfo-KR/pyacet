import pandas as pd
import numpy as np
import seaborn as sns

from eda.data_loader import DataLoader
from eda.data_summary import DataSummary
from eda.visualization import Visualization
from eda.report_generator import PDF, ReportGenerator
from eda.utils import *

def main():
    vessel = pd.read_csv('./test/test_data/vessel_data_04.csv', encoding='cp949')
    vessel = vessel.drop('VVD', axis=1)
    vessel = vessel.drop('CALL_SIGN', axis=1)
    vessel = vessel.drop('ROUTE', axis=1)
    for i in range(4):
        vessel = vessel.replace({'BTH_NO': i}, f'T{i}')
    vessel['ATB'] = pd.to_datetime(vessel['ATB'])
    vessel['ATD'] = pd.to_datetime(vessel['ATD'])
    vessel['WRK_START_DTE'] = pd.to_datetime(vessel['WRK_START_DTE'])
    vessel['WRK_END_DTE'] = pd.to_datetime(vessel['WRK_END_DTE'])
    vessel['ATA'] = pd.to_datetime(vessel['ATA'])
    vessel['ATG'] = pd.to_datetime(vessel['ATG'])
    vessel['ETB'] = pd.to_datetime(vessel['ETB'])
    vessel['ETD'] = pd.to_datetime(vessel['ETD'])
    texts = ['A', 'B', 'C', 'D', 'E']
    vessel['grade'] = np.random.choice(texts, size=len(vessel))
    regions = ['NAEC', 'NAWC', 'SAEC', 'SAWC', 'ASIA', 'EUR']
    vessel['region'] = np.random.choice(regions, size=len(vessel))
    
    
    rp01 = ReportGenerator(vessel, './test/report_test/vesseldata', 'PNIT BerthPlan')
    viz01 = Visualization(vessel, './test/visualize_test/vesseldata/')
    rp01.generate_report()
    viz01.visualize()
    
    # weather = generate_testset()
    # rp02 = ReportGenerator(weather, './test/report_test/weatherdata', 'Weather Data')
    # viz02 = Visualization(weather, './test/visualize_test/weatherdata')
    # rp02.generate_report()
    # viz02.visualize()

if __name__ == '__main__':
    main()