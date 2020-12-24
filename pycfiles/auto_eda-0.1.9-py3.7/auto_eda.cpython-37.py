# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/src/auto_eda.py
# Compiled at: 2020-03-23 11:29:46
# Size of source mod 2**32: 5551 bytes
import pandas as pd, numpy as np, sys, os, argparse, pathlib
pd.options.display.max_columns = None
long_desc = '\n            Welcome to the auto-eda package.\n            It can help you to auto scan the dataset\n            1. head of dataset\n            2. tail of dataset \n            3. shape of dataset\n            4. number of missing values \n            5. number of duplicated rows\n            6. data type \n            7. descriptive statistics \n            8. number of unique values \n            9. unique identifies \n            10. relative frequency (precentage) of unique values or bins of numerical features\n            11. unique values for each feature\n            12. top absolute correlation among features \n            '

def main():
    parser = argparse.ArgumentParser(prog='auto-eda', usage='%(prog)s file_name num_sample[option]',
      description=long_desc,
      formatter_class=(argparse.RawDescriptionHelpFormatter),
      epilog='If you have any advice or questions, feel free to email me xiaochengjin.random@gmail.com')
    parser.add_argument(dest='file',
      type=(argparse.FileType('r')),
      help='file names')
    parser.add_argument(dest='num_sample', type=int, help='number of samples')
    args = parser.parse_args()
    args.file.close()
    print(f"Get file: {args.file.name}")
    print(args)
    df = pd.read_csv(args.file.name)
    print(f"{df.shape[0]} rows and {df.shape[1]} columns in the data frame")
    if args.num_sample > 0 and args.num_sample < 1000000:
        eda(df, min(args.num_sample, df.shape[0]))
    else:
        raise ValueError('the number of samples should be from 0 to 1000000 \ne.g. auto-eda file_name.csv 1000 \n')


def eda(df, num_sample):
    """
    the function below is a general EDA of a dataset
    to know about details about the dataset and visualize some information, we can dive deep in jupyter lab
    =================
    param
    @df: DataFrame
    """
    df = df.sample(n=num_sample, random_state=42)
    print('======= head of data =======')
    print(df.head())
    print('\n======= tail of data =======')
    print(df.tail())
    print('\n======= shape of data =======')
    print(df.shape)
    print('\n======= check missing values =======')
    print(df.isnull().sum())
    print('\n======= check duplicated rows =======')
    print(df[df.duplicated()].shape)
    print('\n======= data type =======')
    print(df.dtypes)
    print('\n======= generate descriptive statistics =======')
    print(round(df.describe(), 2))
    print(round(df.describe(include=[np.object]), 2))
    print('\n======= number of unique values =======')
    n_unique = df.nunique().tolist()
    print(df.nunique())
    print('\n======= find the unique identifier =======')
    for i in range(df.shape[1]):
        if n_unique[i] == len(df):
            print('{} is the unique identifier'.format(df.columns[i]))

    df.dropna(axis=1, inplace=True, how='all')
    print('\n======= relative frequency (precentage) of unique values or bins of numerical features =======')
    for col in df.columns:
        if df[col].dtypes.name == 'object' or df[col].dtypes.name == 'category':
            print(f"{col} -- categorical feature; top 20 categories")
            print(round(df[col].value_counts(normalize=True) * 100, 2)[:20])
        else:
            print(f"{col} -- numerical feature; 5 bins")
            print(round(df[col].value_counts(bins=5)))
        print('-----------------------------')

    print('\n======= unique values for each feature =======')
    for col in df.columns:
        if df[col].dtypes.name == 'object' or df[col].dtypes.name == 'category':
            if df[col].nunique() < 100:
                print('column name:', col)
                print(df[col].unique())
                print('-----------------------------')
            else:
                print(f"over 100 unique values in {col}...")

    print('\n======= absolute correlation among features =======')
    corr_matrix = df.corr().abs()
    sol = corr_matrix.where(np.triu((np.ones(corr_matrix.shape)), k=1).astype(np.bool)).stack().sort_values(ascending=False)
    df_corr = sol.reset_index()
    df_corr.columns = ['feat_1', 'feat_2', 'corr']
    print('Top correlated features')
    print(df_corr)


if __name__ == '__main__':
    main()