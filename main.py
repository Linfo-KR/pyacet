import pandas as pd
import numpy as np
import seaborn as sns

from pyacet.data_loader import DataLoader
from pyacet.data_summary import DataSummary
from pyacet.visualization import Visualization
from pyacet.report_generator import PDF, ReportGenerator
from pyacet.utils import *

def main():
    # vessel = pd.read_csv('./test/test_data/vessel_data_04.csv', encoding='cp949')
    # vessel = vessel.drop('VVD', axis=1)
    # vessel = vessel.drop('CALL_SIGN', axis=1)
    # vessel = vessel.drop('ROUTE', axis=1)
    # for i in range(4):
    #     vessel = vessel.replace({'BTH_NO': i}, f'T{i}')
    # vessel['ATB'] = pd.to_datetime(vessel['ATB'])
    # vessel['ATD'] = pd.to_datetime(vessel['ATD'])
    # vessel['WRK_START_DTE'] = pd.to_datetime(vessel['WRK_START_DTE'])
    # vessel['WRK_END_DTE'] = pd.to_datetime(vessel['WRK_END_DTE'])
    # vessel['ATA'] = pd.to_datetime(vessel['ATA'])
    # vessel['ATG'] = pd.to_datetime(vessel['ATG'])
    # vessel['ETB'] = pd.to_datetime(vessel['ETB'])
    # vessel['ETD'] = pd.to_datetime(vessel['ETD'])
    # texts = ['A', 'B', 'C', 'D', 'E']
    # vessel['grade'] = np.random.choice(texts, size=len(vessel))
    # regions = ['NAEC', 'NAWC', 'SAEC', 'SAWC', 'ASIA', 'EUR']
    # vessel['region'] = np.random.choice(regions, size=len(vessel))
    # vsl_rp = ReportGenerator(vessel, './test/report_test/vesseldata', 'PNIT BerthPlan')
    # vsl_viz = Visualization(vessel, './test/visualize_test/vesseldata/')
    # vsl_rp.generate_report()
    # vsl_viz.visualize()
    
    port = pd.read_csv('./test/test_data/port_data.csv')
    port['TML_IN_DTE'] = pd.to_datetime(port['TML_IN_DTE'])
    port['TML_OUT_DTE'] = pd.to_datetime(port['TML_OUT_DTE'])
    port['TML_TAT_DAY'] = port['TML_TAT_DAY'].astype(float)
    port['CNTR_SIZ'] = port['CNTR_SIZ'].astype(int)
    port['VVD'] = port['VVD'].astype(str)
    port['VVD_YEAR'] = port['VVD_YEAR'].astype(str)
    port = port.drop('CARGO_TYP', axis=1)
    port_rp = ReportGenerator(port, './test/report_test/portdata', 'PNIT CNTR')
    port_viz = Visualization(port, './test/visualize_test/portdata/')
    port_rp.generate_report()
    port_viz.visualize()
    
    # weather = generate_testset()
    # weather_rp = ReportGenerator(weather, './test/report_test/weatherdata', 'Weather')
    # weather_viz = Visualization(weather, './test/visualize_test/weatherdata')
    # weather_rp.generate_report()
    # weather_viz.visualize()

if __name__ == '__main__':
    main()