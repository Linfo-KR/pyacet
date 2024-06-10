import pandas as pd
import numpy as np

from modules.eda import EDA


def main():
    dict_data = {'Name': ['Alice', 'Bob', 'Charlie'],
             'Age': [25, 30, 35],
             'Gender': ['F', 'M', 'M']}

    list_data = [['Alice', 25, 'F'],
                ['Bob', 30, 'M'],
                ['Charlie', 35, 'M']]

    np_data = np.array([['Alice', 25, 'F'],
                        ['Bob', 30, 'M'],
                        ['Charlie', 35, 'M']])

    df_data = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie'],
                            'Age': [25, 30, 35],
                            'Gender': ['F', 'M', 'M']})
    
    test_data = pd.read_csv('./test/test_data/titanic.csv')
    vessel_data = pd.read_csv('./test/test_data/vessel_data_03.csv', encoding='cp949')
    
    test00 = EDA(test_data)
    test01 = EDA(dict_data)
    test02 = EDA(list_data)
    test03 = EDA(np_data)
    test04 = EDA(df_data)
    test05 = EDA(vessel_data)
    
    test00.save_markdown('./test/eda_test/md_test00.md')
    test01.save_markdown('./test/eda_test/md_test01.md')
    test02.save_markdown('./test/eda_test/md_test02.md')
    test03.save_markdown('./test/eda_test/md_test03.md')
    test04.save_markdown('./test/eda_test/md_test04.md')
    test05.save_markdown('./test/eda_test/md_test05.md')
    
    test00.save_pdf('./test/eda_test/pdf_test00.pdf')
    test01.save_pdf('./test/eda_test/pdf_test01.pdf')
    test02.save_pdf('./test/eda_test/pdf_test02.pdf')
    test03.save_pdf('./test/eda_test/pdf_test03.pdf')
    test04.save_pdf('./test/eda_test/pdf_test04.pdf')
    test05.save_pdf('./test/eda_test/pdf_test05.pdf')
    
    test00.visualize('./test/eda_test')
    test01.visualize('./test/eda_test/')
    test02.visualize('./test/eda_test')
    test03.visualize('./test/eda_test/')
    test04.visualize('./test/eda_test')
    test05.visualize('./test/eda_test/')


if __name__ == '__main__':
    main()